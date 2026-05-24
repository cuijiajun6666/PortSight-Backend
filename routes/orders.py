from fastapi import APIRouter, Query as FastAPIQuery
from moomoo import *

from config import HOST, PORT

router = APIRouter()


def create_trade_context():
    return OpenSecTradeContext(
        filter_trdmarket=TrdMarket.US,
        host=HOST,
        port=PORT,
        security_firm=SecurityFirm.FUTUAU
    )


def json_value(value):
    try:
        if value != value:
            return None
    except Exception:
        pass
    return value


def frame_to_orders(data):
    orders = []
    for _, row in data.iterrows():
        record = {key: json_value(value) for key, value in row.to_dict().items()}
        record["order_id"] = str(record.get("order_id", ""))
        orders.append(record)
    return orders


@router.get("/orders/history")
def get_history_orders(
    code: str = "",
    start: str = "",
    end: str = "",
    status: list[str] | None = FastAPIQuery(default=None),
):
    trd_ctx = create_trade_context()
    try:
        ret, data = trd_ctx.history_order_list_query(
            status_filter_list=status or [],
            code=code,
            start=start,
            end=end,
            trd_env=TrdEnv.REAL,
            order_market=TrdMarket.NONE
        )
    finally:
        trd_ctx.close()

    if ret != RET_OK:
        return {
            "ok": False,
            "error": str(data),
            "orders": []
        }

    orders = frame_to_orders(data)
    return {
        "ok": True,
        "count": len(orders),
        "orders": orders
    }


@router.get("/history_orders")
def get_history_orders_legacy(
    code: str = "",
    start: str = "",
    end: str = "",
    status: list[str] | None = FastAPIQuery(default=None),
):
    return get_history_orders(code=code, start=start, end=end, status=status)
