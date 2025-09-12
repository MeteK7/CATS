from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SAP Portal API", version="1.0.0")

# Configure CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class SAPRecord(BaseModel):
    id: Optional[str] = None
    data: Dict[str, Any]

class SAPResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

# Work Order Search Models
class WorkOrderSearchRequest(BaseModel):
    """Search criteria for Zcatsv2_Wo_Get_List RFC"""
    # User context
    i_lang: str = "EN"
    i_usercode: str
    
    # Simplified search criteria
    vin: Optional[str] = None
    dealer_code: Optional[str] = None
    wo_no: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    
    # Strategy checkboxes
    temsa_global: Optional[bool] = None
    temsa_global_gwk: Optional[bool] = None
    germany: Optional[bool] = None
    france: Optional[bool] = None
    north_america: Optional[bool] = None

class WorkOrderItem(BaseModel):
    """Work order item from search results"""
    credate: Optional[str] = None
    dealer_code: Optional[str] = None
    vin: Optional[str] = None
    wo_status: Optional[str] = None
    wo_status_text: Optional[str] = None
    wo_type: Optional[str] = None
    wo_type_text: Optional[str] = None
    fg_status_text: Optional[str] = None
    pds: Optional[str] = None
    demo: Optional[str] = None
    wono: Optional[str] = None  # Work order number
    creuser: Optional[str] = None
    ra_country_text: Optional[str] = None
    wo_onay_text: Optional[str] = None  # Approval status text
    reject_note: Optional[str] = None
    enability_button: bool = False

class WorkOrderSearchResponse(BaseModel):
    """Response from work order search"""
    success: bool
    message: str
    work_orders: List[WorkOrderItem] = []
    error_type: Optional[str] = None
    error_message: Optional[str] = None

# Dropdown data models for search form
class DropdownOption(BaseModel):
    value: str
    text: str

class SearchFormData(BaseModel):
    """Dropdown options for search form"""
    wo_types: List[DropdownOption] = []
    wo_statuses: List[DropdownOption] = []
    fg_statuses: List[DropdownOption] = []
    countries: List[DropdownOption] = []
    approval_statuses: List[DropdownOption] = []
    ra_countries: List[DropdownOption] = []
    strategies: List[DropdownOption] = []

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "SAP Portal API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SAP Portal API"}

# SAP CRUD endpoints
@app.get("/api/sap/records", response_model=List[SAPRecord])
async def get_records():
    """Get all SAP records"""
    try:
        # TODO: Implement SAP RFC call to fetch records
        # For now, return mock data structure
        return [
            SAPRecord(id="1", data={"name": "Sample Record 1", "status": "Active"}),
            SAPRecord(id="2", data={"name": "Sample Record 2", "status": "Inactive"})
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching records: {str(e)}")

@app.get("/api/sap/records/{record_id}", response_model=SAPRecord)
async def get_record(record_id: str):
    """Get a specific SAP record by ID"""
    try:
        # TODO: Implement SAP RFC call to fetch specific record
        return SAPRecord(id=record_id, data={"name": f"Record {record_id}", "status": "Active"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching record: {str(e)}")

@app.post("/api/sap/records", response_model=SAPResponse)
async def create_record(record: SAPRecord):
    """Create a new SAP record"""
    try:
        # TODO: Implement SAP RFC call to create record
        return SAPResponse(success=True, message="Record created successfully", data={"id": "new_id"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating record: {str(e)}")

@app.put("/api/sap/records/{record_id}", response_model=SAPResponse)
async def update_record(record_id: str, record: SAPRecord):
    """Update an existing SAP record"""
    try:
        # TODO: Implement SAP RFC call to update record
        return SAPResponse(success=True, message="Record updated successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating record: {str(e)}")

@app.delete("/api/sap/records/{record_id}", response_model=SAPResponse)
async def delete_record(record_id: str):
    """Delete a SAP record"""
    try:
        # TODO: Implement SAP RFC call to delete record
        return SAPResponse(success=True, message="Record deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting record: {str(e)}")

# Work Order Search Endpoints
@app.get("/api/sap/work-orders/form-data", response_model=SearchFormData)
async def get_search_form_data():
    """Get dropdown options for work order search form"""
    try:
        # TODO: Implement RFC calls to get actual dropdown data
        # For now, return mock data based on common SAP work order values
        return SearchFormData(
            wo_types=[
                DropdownOption(value="10", text="Warranty Repair"),
                DropdownOption(value="20", text="Customer Paid Repair"),
                DropdownOption(value="30", text="Internal Repair"),
                DropdownOption(value="40", text="Recall")
            ],
            wo_statuses=[
                DropdownOption(value="10", text="Created"),
                DropdownOption(value="20", text="Released"),
                DropdownOption(value="30", text="In Progress"),
                DropdownOption(value="40", text="Completed"),
                DropdownOption(value="41", text="Pending Approval"),
                DropdownOption(value="50", text="Closed")
            ],
            fg_statuses=[
                DropdownOption(value="10", text="Not Started"),
                DropdownOption(value="20", text="In Progress"),
                DropdownOption(value="30", text="Completed")
            ],
            countries=[
                DropdownOption(value="TR", text="Turkey"),
                DropdownOption(value="DE", text="Germany"),
                DropdownOption(value="FR", text="France"),
                DropdownOption(value="EG", text="Egypt"),
                DropdownOption(value="US", text="United States")
            ],
            approval_statuses=[
                DropdownOption(value="A", text="Approved"),
                DropdownOption(value="R", text="Rejected"),
                DropdownOption(value="P", text="Pending")
            ],
            ra_countries=[
                DropdownOption(value="TR", text="Turkey"),
                DropdownOption(value="DE", text="Germany"),
                DropdownOption(value="EG", text="Egypt")
            ],
            strategies=[
                DropdownOption(value="TG", text="TG Strategy"),
                DropdownOption(value="TI", text="TI Strategy"),
                DropdownOption(value="TD", text="TD Strategy"),
                DropdownOption(value="TF", text="TF Strategy"),
                DropdownOption(value="TU", text="TU Strategy"),
                DropdownOption(value="TX", text="TX Strategy"),
                DropdownOption(value="TY", text="TY Strategy"),
                DropdownOption(value="TZ", text="TZ Strategy")
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching form data: {str(e)}")

@app.post("/api/sap/work-orders/search", response_model=WorkOrderSearchResponse)
async def search_work_orders(search_request: WorkOrderSearchRequest):
    """Search work orders using Zcatsv2_Wo_Get_List RFC"""
    try:
        # TODO: Implement actual SAP RFC call to Zcatsv2_Wo_Get_List
        # For now, return mock data that matches the expected structure
        
        # Generate realistic mock data with proper filtering based on search criteria
        from datetime import datetime
        
        # Create comprehensive mock data that reflects different strategies and scenarios
        base_work_orders = [
            {
                "credate": "2024-01-15",
                "dealer_code": "TG001",
                "vin": "1HGBH41JXMN109186",
                "wo_status": "41",
                "wo_status_text": "Pending Approval",
                "wo_type": "10",
                "wo_type_text": "Warranty Repair",
                "fg_status_text": "Completed",
                "pds": "",
                "demo": "",
                "wono": "WO001001",
                "creuser": "TESTUSER",
                "ra_country_text": "Turkey",
                "wo_onay_text": "Pending",
                "reject_note": "",
                "enability_button": True,
                "strategy": "temsa_global"
            },
            {
                "credate": "2024-01-16",
                "dealer_code": "TG002",
                "vin": "1HGBH41JXMN109187",
                "wo_status": "30",
                "wo_status_text": "In Progress",
                "wo_type": "20",
                "wo_type_text": "Customer Paid Repair",
                "fg_status_text": "In Progress",
                "pds": "",
                "demo": "",
                "wono": "WO001002",
                "creuser": "TESTUSER",
                "ra_country_text": "Turkey",
                "wo_onay_text": "Approved",
                "reject_note": "",
                "enability_button": False,
                "strategy": "temsa_global_gwk"
            },
            {
                "credate": "2024-01-14",
                "dealer_code": "DE002",
                "vin": "2T1BURHE0KC123456",
                "wo_status": "30",
                "wo_status_text": "In Progress",
                "wo_type": "20",
                "wo_type_text": "Customer Paid Repair",
                "fg_status_text": "In Progress",
                "pds": "",
                "demo": "",
                "wono": "WO002001",
                "creuser": "TESTUSER",
                "ra_country_text": "Germany",
                "wo_onay_text": "Approved",
                "reject_note": "",
                "enability_button": False,
                "strategy": "germany"
            },
            {
                "credate": "2024-01-13",
                "dealer_code": "FR003",
                "vin": "3FA6P0HD9DR123789",
                "wo_status": "50",
                "wo_status_text": "Closed",
                "wo_type": "40",
                "wo_type_text": "Recall",
                "fg_status_text": "Completed",
                "pds": "X",
                "demo": "",
                "wono": "WO003001",
                "creuser": "ADMIN",
                "ra_country_text": "France",
                "wo_onay_text": "Approved",
                "reject_note": "Quality check completed",
                "enability_button": False,
                "strategy": "france"
            },
            {
                "credate": "2024-01-12",
                "dealer_code": "NA004",
                "vin": "5NPE34AF6DH123456",
                "wo_status": "20",
                "wo_status_text": "Released",
                "wo_type": "10",
                "wo_type_text": "Warranty Repair",
                "fg_status_text": "Not Started",
                "pds": "",
                "demo": "",
                "wono": "WO004001",
                "creuser": "USUSER",
                "ra_country_text": "United States",
                "wo_onay_text": "Approved",
                "reject_note": "",
                "enability_button": True,
                "strategy": "north_america"
            }
        ]
        
        # Filter mock data based on search criteria
        filtered_work_orders = []
        for wo_data in base_work_orders:
            # Apply text filters (case-insensitive partial matching)
            if search_request.vin and search_request.vin.upper() not in wo_data["vin"].upper():
                continue
            if search_request.dealer_code and search_request.dealer_code.upper() not in wo_data["dealer_code"].upper():
                continue
            if search_request.wo_no and search_request.wo_no.upper() not in wo_data["wono"].upper():
                continue
                
            # Date range filter
            wo_date = datetime.strptime(wo_data["credate"], "%Y-%m-%d")
            if search_request.date_from:
                try:
                    from_date = datetime.strptime(search_request.date_from, "%Y-%m-%d")
                    if wo_date < from_date:
                        continue
                except ValueError:
                    pass  # Ignore invalid date format
                    
            if search_request.date_to:
                try:
                    to_date = datetime.strptime(search_request.date_to, "%Y-%m-%d")
                    if wo_date > to_date:
                        continue
                except ValueError:
                    pass  # Ignore invalid date format
                
            # Strategy filter - if no strategies selected, show all
            strategy_selected = any([
                search_request.temsa_global, 
                search_request.temsa_global_gwk,
                search_request.germany, 
                search_request.france, 
                search_request.north_america
            ])
            
            if strategy_selected:
                strategy_match = False
                if search_request.temsa_global and wo_data["strategy"] == "temsa_global":
                    strategy_match = True
                elif search_request.temsa_global_gwk and wo_data["strategy"] == "temsa_global_gwk":
                    strategy_match = True
                elif search_request.germany and wo_data["strategy"] == "germany":
                    strategy_match = True
                elif search_request.france and wo_data["strategy"] == "france":
                    strategy_match = True
                elif search_request.north_america and wo_data["strategy"] == "north_america":
                    strategy_match = True
                    
                if not strategy_match:
                    continue
                
            # Create WorkOrderItem (remove strategy field as it's not part of the API response)
            filtered_work_orders.append(WorkOrderItem(**{k: v for k, v in wo_data.items() if k != "strategy"}))
        
        mock_work_orders = filtered_work_orders
        
        return WorkOrderSearchResponse(
            success=True,
            message="Search completed successfully",
            work_orders=mock_work_orders
        )
        
    except Exception as e:
        return WorkOrderSearchResponse(
            success=False,
            message=f"Search failed: {str(e)}",
            work_orders=[],
            error_type="E",
            error_message=str(e)
        )

# Health check endpoint for proxy
@app.get("/api")
@app.head("/api")
async def api_root():
    """API health check endpoint to reduce proxy 404 noise"""
    return {"message": "SAP Portal API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)