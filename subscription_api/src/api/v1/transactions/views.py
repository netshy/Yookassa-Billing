from typing import List

from db.crud import (
    get_all_transactions,
    get_transaction_by_id,
)
from fastapi import Depends, APIRouter

from db.database import get_db
from schemas.subscription_schema import TransactionSchema
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/", response_model=List[TransactionSchema])
def transactions_list(db: Session = Depends(get_db)):
    transactions = get_all_transactions(db)
    return transactions


@router.get("/{transaction_id}", response_model=TransactionSchema)
def transaction_get(transaction_id: str, db: Session = Depends(get_db)):
    transaction = get_transaction_by_id(db, transaction_id)
    return transaction
