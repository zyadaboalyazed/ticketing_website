from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.user import User
from ..models.contract import Contract
from ..schemas.contract import Contract as ContractSchema, ContractCreate, ContractUpdate
from ..utils.dependencies import get_current_user, get_current_agent_or_admin

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/", response_model=ContractSchema, status_code=status.HTTP_201_CREATED)
def create_contract(
    contract_data: ContractCreate,
    current_user: User = Depends(get_current_agent_or_admin),
    db: Session = Depends(get_db)
):
    """Create a new contract (Agent/Admin only)"""
    # Check if client exists
    client = db.query(User).filter(User.id == contract_data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db_contract = Contract(**contract_data.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


@router.get("/", response_model=List[ContractSchema])
def list_contracts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List contracts"""
    query = db.query(Contract)
    
    # Clients can only see their own contracts
    if current_user.role.value == "client":
        query = query.filter(Contract.client_id == current_user.id)
    
    contracts = query.offset(skip).limit(limit).all()
    return contracts


@router.get("/{contract_id}", response_model=ContractSchema)
def get_contract(
    contract_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get contract by ID"""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Check permissions
    if current_user.role.value == "client" and contract.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this contract")
    
    return contract


@router.put("/{contract_id}", response_model=ContractSchema)
def update_contract(
    contract_id: int,
    contract_update: ContractUpdate,
    current_user: User = Depends(get_current_agent_or_admin),
    db: Session = Depends(get_db)
):
    """Update contract (Agent/Admin only)"""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    update_data = contract_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contract, field, value)
    
    db.commit()
    db.refresh(contract)
    return contract


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract(
    contract_id: int,
    current_user: User = Depends(get_current_agent_or_admin),
    db: Session = Depends(get_db)
):
    """Delete contract (Agent/Admin only)"""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    db.delete(contract)
    db.commit()
    return None
