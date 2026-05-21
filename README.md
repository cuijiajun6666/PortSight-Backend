# PortSight Backend

FastAPI backend for PortSight, using Moomoo OpenD as the local trading and market data gateway.

## Server Variables

Use the current server public IP wherever you see `YOUR_SERVER_IP`.

```text
YOUR_SERVER_IP
```

Temporary backend URL:

```text
http://YOUR_SERVER_IP:8000
```

## First Deploy On Ubuntu

SSH into the server:

```bash
ssh root@YOUR_SERVER_IP
```

Run the bootstrap command:

```bash
REPO_URL=https://github.com/cuijiajun6666/PortSight-Backend.git BACKEND_PUBLIC_URL=http://YOUR_SERVER_IP:8000 bash -c "$(curl -fsSL https://raw.githubusercontent.com/cuijiajun6666/PortSight-Backend/main/deploy/bootstrap_ubuntu.sh)"
```

If you omit `BACKEND_PUBLIC_URL`, the deploy script will try to detect the server public IP automatically.

The script installs system dependencies, clones this repo to `/opt/moomoo-backend/app`, creates `/opt/moomoo-backend/data`, installs Python packages, creates a systemd service, opens port `8000`, and starts the backend.

## Install OpenD On Ubuntu

After deploying the backend, install and start moomoo OpenD on the same server:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/cuijiajun6666/PortSight-Backend/main/deploy/install_opend_ubuntu.sh)"
```

The script downloads the latest Ubuntu OpenD package from moomoo, extracts it under `/opt/moomoo-opend`, asks for your moomoo account and password in the SSH terminal, creates a `moomoo-opend` systemd service, and starts OpenD for first login.

If moomoo asks for device verification or 2FA, confirm it in the moomoo app. After first login succeeds, restart OpenD as a background service:

```bash
systemctl restart moomoo-opend
systemctl status moomoo-opend --no-pager
```

Then restart the backend:

```bash
systemctl restart moomoo-backend
```

## Backend Service Commands

Check service status:

```bash
systemctl status moomoo-backend --no-pager
```

Watch logs:

```bash
journalctl -u moomoo-backend -f
```

Watch OpenD logs:

```bash
journalctl -u moomoo-opend -f
```

Restart backend:

```bash
systemctl restart moomoo-backend
```

Update backend after pushing code:

```bash
cd /opt/moomoo-backend/app
git pull
systemctl restart moomoo-backend
```

## OpenD

Moomoo OpenD must run on the server too. The backend expects OpenD at:

```text
127.0.0.1:11111
```

Do not expose OpenD port `11111` to the public internet.

## Runtime Data

Runtime data directory on the server:

```text
/opt/moomoo-backend/data
```

Tracked asset history:

```text
data/asset_snapshots.json
```

Ignored runtime cache:

```text
data/market_intraday_cache.json
```
