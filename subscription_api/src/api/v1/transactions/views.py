from typing import List

from fastapi import APIRouter, Depends

from db.service.pg_service import PostgresService, get_db_service
from schemas.transaction import TransactionSchema

router = APIRouter()


@router.get("/", response_model=List[TransactionSchema])
def transactions_list(db_service: PostgresService = Depends(get_db_service)):
    transactions = db_service.get_all_transactions()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionSchema)
def transaction_get(transaction_id: str, db_service: PostgresService = Depends(get_db_service)):
    transaction = db_service.get_transaction_by_id(transaction_id)
    return transaction
