"""
SAP OData Client for ZTEM_TEST_CATS_SRV service
Handles connections to SAP backend and data transformation
"""

import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from datetime import datetime
import os
from urllib.parse import quote


class SAPODataClient:
    """Client for SAP OData service ZTEM_TEST_CATS_SRV"""
    
    def __init__(self):
        self.base_url = os.getenv("SAP_BASE_URL", "http://10.90.13.15:8000")
        self.service_path = "/sap/opu/odata/sap/ZTEM_TEST_CATS_SRV"
        self.entity_set = "WOHeaderSet"
        
        # XML namespaces for parsing
        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
            'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
        }
    
    def _build_filter(self, search_criteria: Dict) -> str:
        """Build OData $filter parameter from search criteria"""
        filters = []
        
        # VIN filter
        if search_criteria.get('vin'):
            vin_filter = f"substringof('{search_criteria['vin']}', Vin)"
            filters.append(vin_filter)
        
        # Dealer Code filter  
        if search_criteria.get('dealer_code'):
            dealer_filter = f"substringof('{search_criteria['dealer_code']}', DealerCode)"
            filters.append(dealer_filter)
        
        # Work Order Number filter
        if search_criteria.get('wo_no'):
            wo_filter = f"substringof('{search_criteria['wo_no']}', Wono)"
            filters.append(wo_filter)
        
        # Date range filters
        if search_criteria.get('date_from'):
            try:
                date_from = datetime.fromisoformat(search_criteria['date_from']).strftime('%Y-%m-%dT%H:%M:%S')
                filters.append(f"Credate ge datetime'{date_from}'")
            except ValueError:
                pass  # Skip invalid date format
        
        if search_criteria.get('date_to'):
            try:
                date_to = datetime.fromisoformat(search_criteria['date_to']).strftime('%Y-%m-%dT%H:%M:%S')
                filters.append(f"Credate le datetime'{date_to}'")
            except ValueError:
                pass  # Skip invalid date format
        
        return ' and '.join(filters) if filters else ""
    
    def _build_strategy_filter(self, search_criteria: Dict) -> str:
        """Build strategy-based country filters"""
        strategy_filters = []
        
        # Map strategies to countries based on business logic
        if search_criteria.get('temsa_global') or search_criteria.get('temsa_global_gwk'):
            strategy_filters.append("Landx eq 'Turkey'")
        
        if search_criteria.get('germany'):
            strategy_filters.append("Landx eq 'Germany'")
        
        if search_criteria.get('france'):
            strategy_filters.append("Landx eq 'France'")
        
        if search_criteria.get('north_america'):
            strategy_filters.extend(["Landx eq 'United States'", "Landx eq 'Canada'"])
        
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
            raise Exception(f"Failed to parse SAP OData response: {e}")
    
    def _map_to_work_order_item(self, sap_data: Dict) -> Dict:
        """Map SAP OData fields to our WorkOrderItem structure"""
        return {
            "credate": sap_data.get('Credate', '').split('T')[0] if sap_data.get('Credate') else "",
            "dealer_code": sap_data.get('DealerCode', ''),
            "vin": sap_data.get('Vin', ''),
            "wo_status": sap_data.get('WoStatus', ''),
            "wo_status_text": sap_data.get('WoStatusText', ''),
            "wo_type": sap_data.get('WoType', ''),
            "wo_type_text": sap_data.get('WoTypeText', ''),
            "fg_status_text": "",  # Not available in SAP response
            "pds": "",  # Not available in SAP response
            "demo": "",  # Not available in SAP response
            "wono": sap_data.get('Wono', ''),
            "creuser": sap_data.get('Creuser', ''),
            "ra_country_text": sap_data.get('Landx', ''),
            "wo_onay_text": sap_data.get('Wonaytext', ''),
            "reject_note": sap_data.get('Wonot', ''),
            "enability_button": sap_data.get('Wonay') == 'X'
        }
    
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
            
            # Set reasonable limit
            params['$top'] = '100'
            
            # Make HTTP request to SAP
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                # Parse XML response
                sap_work_orders = self._parse_xml_response(response.text)
                
                # Map to our data structure
                work_orders = []
                for sap_wo in sap_work_orders:
                    mapped_wo = self._map_to_work_order_item(sap_wo)
                    work_orders.append(mapped_wo)
                
                return work_orders
                
        except httpx.ConnectError:
            # SAP backend not available - return empty list with descriptive error
            raise Exception("SAP backend is not accessible. Please check your network connection and SAP server status.")
        except httpx.TimeoutException:
            # Request timed out
            raise Exception("SAP request timed out. The SAP server may be experiencing high load.")
        except httpx.HTTPStatusError as e:
            # HTTP error from SAP
            raise Exception(f"SAP server returned error {e.response.status_code}: {e.response.text}")
        except ET.ParseError as e:
            # XML parsing error
            raise Exception(f"Invalid response format from SAP server: {e}")
        except Exception as e:
            # General error
            raise Exception(f"Unexpected error connecting to SAP: {str(e)}")