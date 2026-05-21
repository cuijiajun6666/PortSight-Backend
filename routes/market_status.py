# routes/market_status.py
from fastapi import APIRouter
from moomoo import *
from config import HOST, PORT

router = APIRouter()

@router.get("/market_status")
def get_market_status():
    quote_ctx = OpenQuoteContext(host=HOST, port=PORT)

    ret, data = quote_ctx.get_global_state()
    quote_ctx.close()

    if ret != RET_OK:
        return {"ok": False, "error": str(data)}

    return {
        "ok": True,
        "market_us": data.get("market_us"),
        "qot_logined": data.get("qot_logined"),
        "trd_logined": data.get("trd_logined"),
        "program_status_type": data.get("program_status_type")
    }