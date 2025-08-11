from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="Automotive Parts Pricing API",
    description="API for fetching automotive parts pricing information including installation costs, SRP, and insurance values. Supports both thinsmith parts and body & paint services.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Function to load automotive parts data from JSON file
def load_auto_parts_data():
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_dir, "auto_parts_data.json")
        
        # Check if file exists, if not create it with default data
        if not os.path.exists(json_file_path):
            print("JSON file not found, creating default data...")
            create_default_json_file(json_file_path)
        
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Warning: auto_parts_data.json file not found. Using empty database.")
        return {"thinsmith": [], "body_and_paint": []}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}. Using empty database.")
        return {"thinsmith": [], "body_and_paint": []}

# Function to create default JSON file if it doesn't exist
def create_default_json_file(file_path):
    default_data = {
        "thinsmith": [
            {"id": 1, "part_name": "Back Door", "cost_installation_personal": 2000.00, "srp": 5500.00, "insurance": 8800.00},
            {"id": 2, "part_name": "Cargo", "cost_installation_personal": 5500.00, "srp": 11000.00, "insurance": 17800.00},
            {"id": 3, "part_name": "Door", "cost_installation_personal": 2000.00, "srp": 5500.00, "insurance": 8800.00}
        ],
        "body_and_paint": [
            {"id": 1, "part_name": "Back Door", "small_damage": 800.00, "medium_damage": 1500.00, "large_damage": 2500.00, "full_repaint": 3500.00},
            {"id": 2, "part_name": "Cargo", "small_damage": 1200.00, "medium_damage": 2000.00, "large_damage": 3500.00, "full_repaint": 5000.00},
            {"id": 3, "part_name": "Door", "small_damage": 600.00, "medium_damage": 1200.00, "large_damage": 2000.00, "full_repaint": 2800.00}
        ]
    }
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(default_data, file, indent=2, ensure_ascii=False)
        print("Default JSON file created successfully")
    except Exception as e:
        print(f"Error creating default JSON file: {e}")

# Function to save automotive parts data to JSON file
def save_auto_parts_data():
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_dir, "auto_parts_data.json")
        
        data = {
            "thinsmith": thinsmith_db,
            "body_and_paint": body_paint_db
        }
        
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving data to JSON: {e}")
        return False

# Pydantic models for request/response
class ThinsmithPart(BaseModel):
    id: int
    part_name: str
    cost_installation_personal: float
    srp: float
    insurance: float

class ThinsmithPartCreate(BaseModel):
    part_name: str
    cost_installation_personal: float
    srp: float
    insurance: float

class ThinsmithPartUpdate(BaseModel):
    part_name: Optional[str] = None
    cost_installation_personal: Optional[float] = None
    srp: Optional[float] = None
    insurance: Optional[float] = None

class BodyPaintPart(BaseModel):
    id: int
    part_name: str
    small_damage: float
    medium_damage: float
    large_damage: float
    full_repaint: float

class BodyPaintPartCreate(BaseModel):
    part_name: str
    small_damage: float
    medium_damage: float
    large_damage: float
    full_repaint: float

class BodyPaintPartUpdate(BaseModel):
    part_name: Optional[str] = None
    small_damage: Optional[float] = None
    medium_damage: Optional[float] = None
    large_damage: Optional[float] = None
    full_repaint: Optional[float] = None

# In-memory databases with automotive parts data loaded from JSON
data = load_auto_parts_data()
thinsmith_db = data.get("thinsmith", [])
body_paint_db = data.get("body_and_paint", [])

# Calculate next IDs for both databases
thinsmith_next_id = max([part["id"] for part in thinsmith_db], default=0) + 1
body_paint_next_id = max([part["id"] for part in body_paint_db], default=0) + 1

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Automotive Parts Pricing API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "thinsmith": "/thinsmith",
            "body_paint": "/body-paint",
            "health": "/health"
        },
        "total_parts": {
            "thinsmith": len(thinsmith_db),
            "body_paint": len(body_paint_db)
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "Automotive Parts Pricing API is running",
        "thinsmith_parts": len(thinsmith_db),
        "body_paint_parts": len(body_paint_db),
        "version": "1.0.0"
    }

# Reload data from JSON file
@app.post("/reload-data")
async def reload_data():
    global thinsmith_db, body_paint_db, thinsmith_next_id, body_paint_next_id
    data = load_auto_parts_data()
    thinsmith_db = data.get("thinsmith", [])
    body_paint_db = data.get("body_and_paint", [])
    thinsmith_next_id = max([part["id"] for part in thinsmith_db], default=0) + 1
    body_paint_next_id = max([part["id"] for part in body_paint_db], default=0) + 1
    return {
        "message": "Data reloaded successfully", 
        "thinsmith_parts": len(thinsmith_db),
        "body_paint_parts": len(body_paint_db)
    }

# Save current data to JSON file
@app.post("/save-data")
async def save_data():
    if save_auto_parts_data():
        return {"message": "Data saved successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save data to JSON file"
        )

# GET all thinsmith parts
@app.get("/thinsmith", response_model=List[ThinsmithPart])
async def get_all_thinsmith_parts():
    return thinsmith_db

# GET all body and paint parts
@app.get("/body-paint", response_model=List[BodyPaintPart])
async def get_all_body_paint_parts():
    return body_paint_db

# GET thinsmith part by ID
@app.get("/thinsmith/{part_id}", response_model=ThinsmithPart)
async def get_thinsmith_part(part_id: int):
    part = next((part for part in thinsmith_db if part["id"] == part_id), None)
    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thinsmith part with id {part_id} not found"
        )
    return part

# GET body and paint part by ID
@app.get("/body-paint/{part_id}", response_model=BodyPaintPart)
async def get_body_paint_part(part_id: int):
    part = next((part for part in body_paint_db if part["id"] == part_id), None)
    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Body and paint part with id {part_id} not found"
        )
    return part

# GET thinsmith parts by name
@app.get("/thinsmith/name/{part_name}", response_model=List[ThinsmithPart])
async def get_thinsmith_parts_by_name(part_name: str):
    matching_parts = [part for part in thinsmith_db if part_name.lower() in part["part_name"].lower()]
    if not matching_parts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No thinsmith parts found matching '{part_name}'"
        )
    return matching_parts

# GET body and paint parts by name
@app.get("/body-paint/name/{part_name}", response_model=List[BodyPaintPart])
async def get_body_paint_parts_by_name(part_name: str):
    matching_parts = [part for part in body_paint_db if part_name.lower() in part["part_name"].lower()]
    if not matching_parts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No body and paint parts found matching '{part_name}'"
        )
    return matching_parts

# POST create new thinsmith part
@app.post("/thinsmith", response_model=ThinsmithPart, status_code=status.HTTP_201_CREATED)
async def create_thinsmith_part(part: ThinsmithPartCreate):
    global thinsmith_next_id
    new_part = {
        "id": thinsmith_next_id,
        "part_name": part.part_name,
        "cost_installation_personal": part.cost_installation_personal,
        "srp": part.srp,
        "insurance": part.insurance
    }
    thinsmith_db.append(new_part)
    thinsmith_next_id += 1
    
    # Save changes to JSON file
    save_auto_parts_data()
    
    return new_part

# POST create new body and paint part
@app.post("/body-paint", response_model=BodyPaintPart, status_code=status.HTTP_201_CREATED)
async def create_body_paint_part(part: BodyPaintPartCreate):
    global body_paint_next_id
    new_part = {
        "id": body_paint_next_id,
        "part_name": part.part_name,
        "small_damage": part.small_damage,
        "medium_damage": part.medium_damage,
        "large_damage": part.large_damage,
        "full_repaint": part.full_repaint
    }
    body_paint_db.append(new_part)
    body_paint_next_id += 1
    
    # Save changes to JSON file
    save_auto_parts_data()
    
    return new_part

# PUT update thinsmith part by ID
@app.put("/thinsmith/{part_id}", response_model=ThinsmithPart)
async def update_thinsmith_part(part_id: int, part_update: ThinsmithPartUpdate):
    part_index = next((index for index, part in enumerate(thinsmith_db) if part["id"] == part_id), None)
    if part_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thinsmith part with id {part_id} not found"
        )
    
    # Update only provided fields
    existing_part = thinsmith_db[part_index]
    update_data = part_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        existing_part[field] = value
    
    # Save changes to JSON file
    save_auto_parts_data()
    
    return existing_part

# PUT update body and paint part by ID
@app.put("/body-paint/{part_id}", response_model=BodyPaintPart)
async def update_body_paint_part(part_id: int, part_update: BodyPaintPartUpdate):
    part_index = next((index for index, part in enumerate(body_paint_db) if part["id"] == part_id), None)
    if part_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Body and paint part with id {part_id} not found"
        )
    
    # Update only provided fields
    existing_part = body_paint_db[part_index]
    update_data = part_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        existing_part[field] = value
    
    # Save changes to JSON file
    save_auto_parts_data()
    
    return existing_part

# DELETE thinsmith part by ID
@app.delete("/thinsmith/{part_id}")
async def delete_thinsmith_part(part_id: int):
    part_index = next((index for index, part in enumerate(thinsmith_db) if part["id"] == part_id), None)
    if part_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thinsmith part with id {part_id} not found"
        )
    
    deleted_part = thinsmith_db.pop(part_index)
    
    # Save changes to JSON file
    save_auto_parts_data()
    
    return {"message": f"Thinsmith part with id {part_id} deleted successfully", "deleted_part": deleted_part}

# DELETE body and paint part by ID
@app.delete("/body-paint/{part_id}")
async def delete_body_paint_part(part_id: int):
    part_index = next((index for index, part in enumerate(body_paint_db) if part["id"] == part_id), None)
    if part_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Body and paint part with id {part_id} not found"
        )
    
    deleted_part = body_paint_db.pop(part_index)
    
    # Save changes to JSON file
    save_auto_parts_data()
    
    return {"message": f"Body and paint part with id {part_id} deleted successfully", "deleted_part": deleted_part}

# Custom exception handler
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# Run the application
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
