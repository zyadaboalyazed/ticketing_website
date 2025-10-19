from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import User, SLA, UserRole
from ..schemas import SLACreate, SLAUpdate, SLAResponse
from ..routers.auth import require_role

router = APIRouter(prefix="/slas", tags=["slas"])


@router.post("", response_model=SLAResponse, status_code=status.HTTP_201_CREATED)
def create_sla(
    sla: SLACreate,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    # Check if SLA with same name exists
    existing = db.query(SLA).filter(SLA.name == sla.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="SLA with this name already exists")
    
    db_sla = SLA(**sla.dict())
    db.add(db_sla)
    db.commit()
    db.refresh(db_sla)
    return db_sla


@router.get("", response_model=List[SLAResponse])
def list_slas(db: Session = Depends(get_db)):
    slas = db.query(SLA).all()
    return slas


@router.get("/{sla_id}", response_model=SLAResponse)
def get_sla(sla_id: int, db: Session = Depends(get_db)):
    sla = db.query(SLA).filter(SLA.id == sla_id).first()
    
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    
    return sla


@router.put("/{sla_id}", response_model=SLAResponse)
def update_sla(
    sla_id: int,
    sla_update: SLAUpdate,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    sla = db.query(SLA).filter(SLA.id == sla_id).first()
    
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    
    update_data = sla_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sla, field, value)
    
    db.commit()
    db.refresh(sla)
    return sla


@router.delete("/{sla_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sla(
    sla_id: int,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    sla = db.query(SLA).filter(SLA.id == sla_id).first()
    
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    
    db.delete(sla)
    db.commit()
    return None
