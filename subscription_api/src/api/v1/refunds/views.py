from typing import List

from fastapi import APIRouter, Depends, Request

from core.auth.wrapper import login_required
from db.service.pg_service import PostgresService, get_db_service
from schemas.subscription_schema import RefundSchema

router = APIRouter()


@router.get(
    "/",
    response_model=List[RefundSchema],
    summary="Отображение возвратов пользователя.",
    description="Отображает все возвраты пользователя, включая сумму возврата, дату, статус итп."
)
@login_required()
async def refunds_list(
        request: Request,
        db_service: PostgresService = Depends(get_db_service)
):
    refunds = db_service.get_customer_all_refunds(request.user.id)
    return refunds


@router.get(
    "/{refund_id}",
    response_model=RefundSchema,
    summary="Отобразить конкретный возврат по его id."
)
@login_required()
async def get_refund(
        refund_id: str,
        request: Request,
        db_service: PostgresService = Depends(get_db_service)
):
    refund = db_service.get_customer_refund_by_id(request.user.id, refund_id)
    return refund
