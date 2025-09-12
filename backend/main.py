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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)