from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator

from app import models, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EquipTrack API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "equiptrack-backend"}

# 1. GET all assets
@app.get("/api/assets", response_model=List[schemas.AssetResponse])
def list_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()

# 2. POST create asset
@app.post("/api/assets", response_model=schemas.AssetResponse, status_code=201)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Asset).filter(models.Asset.serial_number == asset.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Serial number already registered")
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# 3. PUT update asset
@app.put("/api/assets/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(asset_id: int, update_data: schemas.AssetUpdate, db: Session = Depends(get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# 4. DELETE asset
@app.delete("/api/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return None