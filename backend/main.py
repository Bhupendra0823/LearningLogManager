from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from backend.db import logs_collection
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Learner Log Manager", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bkumar0823.space",
        "https://bkumar-portfolio.onrender.com",
        "http://localhost:5173",
        "all"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Log(BaseModel):
    title: str
    category: str
    why: str
    applied: str
    capability: str
    next_step: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
 
def serialize(log):
    return {
        "id": str(log["_id"]),
        "title": log["title"],
        "category": log["category"],
        "why": log["why"],
        "applied": log["applied"],
        "capability": log["capability"],
        "next_step": log["next_step"],
        "is_active": log["is_active"],
        "created_at": log["created_at"],
        "updated_at": log["updated_at"]
    }
    
    
@app.post("/addlogs")
def create_log(log:Log):
    result = logs_collection.insert_one(log.model_dump())
    return {"message": "Log added successfully", "log_id": str(result.inserted_id)}

@app.get("/logs")
def get_logs():
    logs = logs_collection.find()
    return [serialize(log) for log in logs]

@app.get("/logs/{log_id}")
def get_log(log_id: str):
    log = logs_collection.find_one({"_id": ObjectId(log_id)})
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return serialize(log)


@app.put("/edit-logs/{log_id}")
def update_log(log_id: str, update_log: Log):
    try:
        oid = ObjectId(log_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid log ID format")
    existing_log = logs_collection.find_one({"_id": oid})
    if not existing_log:
        raise HTTPException(status_code=404, detail="Log not found")
    payload = update_log.model_dump()
    logs_collection.update_one({"_id": oid}, {"$set": payload})
    return serialize(logs_collection.find_one({"_id": oid}))


@app.delete("/delete-logs/{log_id}")
def delete_log(log_id: str):
    try:
        oid = ObjectId(log_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid log ID format")
    result = logs_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log deleted successfully"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Learner Log Manager"
    }
