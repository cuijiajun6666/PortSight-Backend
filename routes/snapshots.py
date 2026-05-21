from fastapi import APIRouter
from asset_snapshots import (
    get_latest_closed_trading_date,
    has_snapshot_for_date,
    load_snapshots,
    upsert_snapshot
)

router = APIRouter()


@router.get("/asset_snapshots")
def get_asset_snapshots():
    refresh_latest_closed_snapshot_if_missing()
    return {
        "ok": True,
        "snapshots": load_snapshots()
    }


def refresh_latest_closed_snapshot_if_missing():
    trading_date = get_latest_closed_trading_date()
    if trading_date is None:
        return

    trading_date_str = trading_date.isoformat()
    if has_snapshot_for_date(trading_date_str):
        return

    from routes.account import fetch_account_snapshot

    snapshot = fetch_account_snapshot()
    if snapshot is None:
        print("补记最近收盘资产失败：获取账户资产失败")
        return

    upsert_snapshot(
        trading_date=trading_date_str,
        total_assets=snapshot["total_assets"],
        principal=snapshot["principal"]
    )
    print("补记最近收盘资产:", trading_date_str)
