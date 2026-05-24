from fastapi import APIRouter, Query as FastAPIQuery
from moomoo import *

from config import HOST, PORT
from deal_cache import (
    load_deal_cache,
    sync_known_history_deals,
)

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


def frame_to_deals(data):
    deals = []
    for _, row in data.iterrows():
        record = {key: json_value(value) for key, value in row.to_dict().items()}
        record["deal_id"] = str(record.get("deal_id", ""))
        record["order_id"] = str(record.get("order_id", ""))
        deals.append(record)
    return deals


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


@router.get("/deals/history")
def get_history_deals(
    code: str = "",
    start: str = "",
    end: str = "",
):
    trd_ctx = create_trade_context()
    try:
        ret, data = trd_ctx.history_deal_list_query(
            code=code,
            start=start,
            end=end,
            trd_env=TrdEnv.REAL,
            deal_market=TrdMarket.NONE
        )
    finally:
        trd_ctx.close()

    if ret != RET_OK:
        return {
            "ok": False,
            "error": str(data),
            "deals": []
        }

    deals = frame_to_deals(data)
    return {
        "ok": True,
        "count": len(deals),
        "deals": deals
    }


@router.get("/history_deals")
def get_history_deals_legacy(
    code: str = "",
    start: str = "",
    end: str = "",
):
    return get_history_deals(code=code, start=start, end=end)


@router.get("/deals")
def get_cached_deals():
    cache = load_deal_cache()
    deals = cache.get("deals", [])
    return {
        "ok": True,
        "updated_at": cache.get("updated_at"),
        "count": len(deals),
        "deals": deals
    }


@router.post("/deals/sync_known_history")
def sync_known_history():
    return sync_known_history_deals()
