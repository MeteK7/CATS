"""
SAP OData Client for ZTEM_TEST_CATS_SRV service
Handles connections to SAP backend and data transformation
"""

import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from datetime import datetime
import os
import json
from urllib.parse import quote
import base64


class SAPODataClient:
    """Client for SAP OData service ZTEM_TEST_CATS_SRV"""

    def __init__(self):
        # Ensure HTTPS for production security
        self.base_url = os.getenv("SAP_BASE_URL",
                                  "http://tuafioridev.temsa.pvt:8000")
        if not self.base_url.startswith("http://"):
            if os.getenv("SAP_FORCE_HTTPS", "true").lower() == "true":
                raise ValueError(
                    "SAP_BASE_URL must use HTTPS for security. Set SAP_FORCE_HTTPS=false to override."
                )

        self.service_path = "/sap/opu/odata/sap/ZTEM_TEST_CATS_SRV"
        self.entity_set = "WOHeaderSet"

        # Authentication configuration
        self.sap_user = os.getenv("SAP_USER")
        self.sap_password = os.getenv("SAP_PASSWD")
        self.auth_mode = os.getenv("SAP_AUTH_MODE", "basic").lower()

        # Request timeout and retry configuration
        self.timeout = float(os.getenv("SAP_TIMEOUT", "30.0"))
        self.max_results = int(os.getenv("SAP_MAX_RESULTS", "100"))

        # XML namespaces for parsing
        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
            'm':
            'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
        }

    def _escape_odata_string(self, value: str) -> str:
        """Escape string value for OData $filter to prevent injection"""
        if not value:
            return ""
        # Escape single quotes by doubling them (OData standard)
        return str(value).replace("'", "''")

    def _build_filter(self, search_criteria: Dict) -> str:
        """Build OData $filter parameter from search criteria"""
        filters = []

        # VIN filter (escaped)
        if search_criteria.get('vin'):
            escaped_vin = self._escape_odata_string(search_criteria['vin'])
            vin_filter = f"Vin eq '{escaped_vin}'"
            filters.append(vin_filter)

        # Dealer Code filter (escaped)
        if search_criteria.get('dealer_code'):
            escaped_dealer = self._escape_odata_string(
                search_criteria['dealer_code'])
            dealer_filter = f"DealerCode eq '{escaped_dealer}'"
            filters.append(dealer_filter)

        # Work Order Number filter (escaped)
        if search_criteria.get('wo_no'):
            escaped_wo = self._escape_odata_string(search_criteria['wo_no'])
            wo_filter = f"Wono eq '{escaped_wo}'"
            filters.append(wo_filter)

        # Date range filters
        if search_criteria.get('date_from'):
            try:
                date_from = datetime.fromisoformat(
                    search_criteria['date_from']).strftime('%Y-%m-%dT%H:%M:%S')
                filters.append(f"Credate ge datetime'{date_from}'")
            except ValueError:
                pass  # Skip invalid date format

        if search_criteria.get('date_to'):
            try:
                date_to = datetime.fromisoformat(
                    search_criteria['date_to']).strftime('%Y-%m-%dT%H:%M:%S')
                filters.append(f"Credate le datetime'{date_to}'")
            except ValueError:
                pass  # Skip invalid date format

        return ' and '.join(filters) if filters else ""

    def _build_strategy_filter(self, search_criteria: Dict) -> str:
        """Build strategy-based country filters"""
        strategy_filters = []

        # Map strategies to countries based on business logic
        if search_criteria.get('temsa_global') or search_criteria.get(
                'temsa_global_gwk'):
            strategy_filters.append("Landx eq 'Turkey'")

        if search_criteria.get('germany'):
            strategy_filters.append("Landx eq 'Germany'")

        if search_criteria.get('france'):
            strategy_filters.append("Landx eq 'France'")

        if search_criteria.get('north_america'):
            strategy_filters.extend(
                ["Landx eq 'United States'", "Landx eq 'Canada'"])

        if strategy_filters:
            return '(' + ' or '.join(strategy_filters) + ')'

        return ""

    def _parse_xml_response(self, xml_content: str) -> List[Dict]:
        """Parse SAP OData XML response into list of work orders"""
        try:
            root = ET.fromstring(xml_content)
            work_orders = []

            # Find all entry elements
            entries = root.findall('.//atom:entry', self.namespaces)

            for entry in entries:
                properties = entry.find('.//m:properties', self.namespaces)
                if properties is not None:
                    wo_data = {}

                    # Extract all property values
                    for prop in properties:
                        tag_name = prop.tag.split('}')[-1]  # Remove namespace
                        value = prop.text if prop.text else ""
                        wo_data[tag_name] = value

                    work_orders.append(wo_data)

            return work_orders

        except ET.ParseError as e:
            # Let ET.ParseError propagate for proper fallback handling
            raise e

    def _map_to_work_order_item(self, sap_data: Dict) -> Dict:
        """Map SAP OData fields to our WorkOrderItem structure"""
        return {
            "credate":
            sap_data.get('Credate', '').split('T')[0]
            if sap_data.get('Credate') else "",
            "dealer_code":
            sap_data.get('DealerCode', ''),
            "vin":
            sap_data.get('Vin', ''),
            "wo_status":
            sap_data.get('WoStatus', ''),
            "wo_status_text":
            sap_data.get('WoStatusText', ''),
            "wo_type":
            sap_data.get('WoType', ''),
            "wo_type_text":
            sap_data.get('WoTypeText', ''),
            "fg_status_text":
            "",  # Not available in SAP response
            "pds":
            "",  # Not available in SAP response
            "demo":
            "",  # Not available in SAP response
            "wono":
            sap_data.get('Wono', ''),
            "creuser":
            sap_data.get('Creuser', ''),
            "ra_country_text":
            sap_data.get('Landx', ''),
            "wo_onay_text":
            sap_data.get('Wonaytext', ''),
            "reject_note":
            sap_data.get('Wonot', ''),
            "enability_button":
            sap_data.get('Wonay') == 'X'
        }

    def _get_auth(self) -> Optional[httpx.Auth]:
        """Get authentication object based on configuration"""
        if self.auth_mode == "basic" and self.sap_user and self.sap_password:
            return httpx.BasicAuth(self.sap_user, self.sap_password)
        return None

    def _get_headers(self, format_type: str = "xml") -> Dict[str, str]:
        """Get request headers with proper content negotiation"""
        headers = {
            "User-Agent": "SAP-Portal-Modernization/1.0",
            "Cache-Control": "no-cache"
        }

        if format_type == "xml":
            headers["Accept"] = "application/atom+xml"
        elif format_type == "json":
            headers["Accept"] = "application/json"

        return headers

    def _parse_json_response(self, json_content: str) -> List[Dict]:
        """Parse SAP OData JSON response into list of work orders"""
        try:
            data = json.loads(json_content)
            work_orders = []

            # Handle OData v2 JSON format
            if "d" in data and "results" in data["d"]:
                for result in data["d"]["results"]:
                    work_orders.append(result)
            elif "value" in data:  # OData v4 format
                work_orders = data["value"]

            return work_orders

        except json.JSONDecodeError as e:
            # Let JSONDecodeError propagate for proper fallback handling
            raise e

    async def search_work_orders(self, search_criteria: Dict) -> List[Dict]:
        """Search work orders using SAP OData service"""
        try:
            # Build OData query
            url = f"{self.base_url}{self.service_path}/{self.entity_set}"

            # Build filters
            main_filter = self._build_filter(search_criteria)
            strategy_filter = self._build_strategy_filter(search_criteria)

            # Combine filters
            combined_filters = []
            if main_filter:
                combined_filters.append(main_filter)
            if strategy_filter:
                combined_filters.append(strategy_filter)

            # Add query parameters
            params = {}
            if combined_filters:
                params['$filter'] = ' and '.join(combined_filters)

            # Set configurable limit
            params['$top'] = str(self.max_results)

            # Get authentication and headers
            auth = self._get_auth()
            headers = self._get_headers(
                "xml")  # Try XML first, fallback to JSON if needed

            # Make HTTP request to SAP with authentication and proper headers
            async with httpx.AsyncClient(
                timeout=self.timeout,
                verify=True  # Enforce SSL certificate verification
            ) as client:
                response = await client.get(url,
                                            params=params,
                                            auth=auth,
                                            headers=headers)

                # Handle 406/415 status codes by retrying with JSON Accept header
                if response.status_code in [406, 415]:
                    # Server doesn't support XML format, try JSON
                    json_headers = self._get_headers("json")
                    response = await client.get(url,
                                                params=params,
                                                auth=auth,
                                                headers=json_headers)

                # Now check for other HTTP errors
                response.raise_for_status()

                # Try to parse based on Content-Type or fallback
                content_type = response.headers.get("content-type", "").lower()

                if "application/json" in content_type:
                    # Response is JSON, parse directly
                    sap_work_orders = self._parse_json_response(response.text)
                else:
                    # Try to parse as XML first, fallback to JSON on parsing failure
                    try:
                        sap_work_orders = self._parse_xml_response(
                            response.text)
                    except ET.ParseError:
                        # XML parsing failed, try JSON parsing of same response
                        try:
                            sap_work_orders = self._parse_json_response(
                                response.text)
                        except json.JSONDecodeError as e:
                            raise Exception(
                                f"SAP server returned invalid data format: {e}"
                            )

                # Map to our data structure
                work_orders = []
                for sap_wo in sap_work_orders:
                    mapped_wo = self._map_to_work_order_item(sap_wo)
                    work_orders.append(mapped_wo)

                return work_orders

        except httpx.ConnectError:
            # SAP backend not available - return empty list with descriptive error
            raise Exception(
                "SAP backend is not accessible. Please check your network connection and SAP server status."
            )
        except httpx.TimeoutException:
            # Request timed out
            raise Exception(
                "SAP request timed out. The SAP server may be experiencing high load."
            )
        except httpx.HTTPStatusError as e:
            # Handle authentication errors specifically
            if e.response.status_code in [401, 403]:
                raise Exception(
                    "SAP authentication failed. Please check your SAP credentials and permissions."
                )
            elif e.response.status_code in [406, 415]:
                # This should be handled by the retry logic above, but just in case
                raise Exception(
                    "SAP server does not support the requested data format. Please contact system administrator."
                )
            else:
                # Don't expose SAP internals to clients, log full details server-side
                import logging
                logging.error(
                    f"SAP HTTP Error {e.response.status_code}: {e.response.text}"
                )
                raise Exception(
                    f"SAP server returned error {e.response.status_code}. Please contact system administrator."
                )
        except (ET.ParseError, json.JSONDecodeError) as e:
            # Parsing error (XML or JSON)
            raise Exception(f"Invalid response format from SAP server: {e}")
        except Exception as e:
            # General error
            raise Exception(f"Unexpected error connecting to SAP: {str(e)}")
