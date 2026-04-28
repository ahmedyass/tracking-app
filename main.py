from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
import os
from pydantic import BaseModel
from typing import List

# --- Database Setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ListModel(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    items = relationship("ItemModel", back_populates="parent_list", cascade="all, delete-orphan", order_by="ItemModel.order_index")

class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    list_id = Column(Integer, ForeignKey("lists.id"))
    order_index = Column(Integer, default=0)
    parent_list = relationship("ListModel", back_populates="items")
    increments = relationship("IncrementModel", back_populates="item", cascade="all, delete-orphan")

class IncrementModel(Base):
    __tablename__ = "increments"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    item = relationship("ItemModel", back_populates="increments")

Base.metadata.create_all(bind=engine)

# --- FastAPI App ---
app = FastAPI(title="Tracker API")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Schemas ---
class ListCreate(BaseModel): name: str
class ItemCreate(BaseModel): name: str
class ReorderRequest(BaseModel): item_ids: List[int]

# --- Endpoints ---
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/lists")
def get_lists(db: Session = Depends(get_db)):
    return db.query(ListModel).all()

@app.post("/api/lists")
def create_list(list_data: ListCreate, db: Session = Depends(get_db)):
    new_list = ListModel(name=list_data.name)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@app.delete("/api/lists/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db)):
    db_list = db.query(ListModel).filter(ListModel.id == list_id).first()
    if not db_list: raise HTTPException(status_code=404)
    db.delete(db_list)
    db.commit()
    return {"status": "deleted"}

@app.get("/api/lists/{list_id}/items")
def get_items(list_id: int, db: Session = Depends(get_db)):
    items = db.query(ItemModel).filter(ItemModel.list_id == list_id).order_by(ItemModel.order_index).all()
    # Count increments for each item
    result = []
    for item in items:
        count = db.query(func.count(IncrementModel.id)).filter(IncrementModel.item_id == item.id).scalar()
        result.append({"id": item.id, "name": item.name, "count": count})
    return result

@app.post("/api/lists/{list_id}/items")
def create_item(list_id: int, item_data: ItemCreate, db: Session = Depends(get_db)):
    max_order = db.query(func.max(ItemModel.order_index)).filter(ItemModel.list_id == list_id).scalar() or 0
    new_item = ItemModel(name=item_data.name, list_id=list_id, order_index=max_order + 1)
    db.add(new_item)
    db.commit()
    return {"status": "created"}

@app.post("/api/items/{item_id}/increment")
def increment_item(item_id: int, db: Session = Depends(get_db)):
    # This automatically saves the precise datetime via server_default=func.now()
    new_inc = IncrementModel(item_id=item_id)
    db.add(new_inc)
    db.commit()
    count = db.query(func.count(IncrementModel.id)).filter(IncrementModel.item_id == item_id).scalar()
    return {"new_count": count}

@app.put("/api/lists/{list_id}/items/reorder")
def reorder_items(list_id: int, req: ReorderRequest, db: Session = Depends(get_db)):
    for index, item_id in enumerate(req.item_ids):
        db.query(ItemModel).filter(ItemModel.id == item_id).update({"order_index": index})
    db.commit()
    return {"status": "reordered"}