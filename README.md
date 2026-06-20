# Decision Provenance Explorer
> **Real-time audit trail dashboard for ML decisions with cryptographic verification on Polygon Amoy via POKT Network.**

---

## Overview

The Decision Provenance Explorer solves a critical problem: **ML models make consequential decisions daily (loans, fraud flags, hiring) stored in mutable databases that can be silently altered.** This dashboard provides tamper-evident verification using Merkle-chained records anchored to Polygon Amoy via POKT Network's decentralized RPC.

### The Problem

| Without Provenance | With Decision Provenance |
|---|---|
| DB rows edited without trace | SHA-256 hashes of inputs/outputs |
| No proof model version unchanged | Versioned config with mandatory reasons |
| Regulators can't verify claims | EU AI Act Article 13 compliant exports |
| Silent threshold changes | Every change = new versioned config |

---

## Live Demo

| Service | URL |
|---|---|
| **Frontend Dashboard** | https://decision-provenance-explorer.vercel.app |
| **API Documentation** | https://decision-provenance-api.onrender.com/docs |
| **Health Check** | https://decision-provenance-api.onrender.com/health |
| **Contract (Polygon Amoy)** | https://amoy.polygonscan.com/address/0x31e8841C3511177847dbAbF289EdFC6f60CB1fb3 |
| **Live Anchor Transaction** | https://amoy.polygonscan.com/tx/27c82e2e48cc320b54bb0961dd8926234208eb58c2418c79dd88ca72c4363e12 |

---

## Features

| Feature | Description | Endpoint |
|---|---|---|
| **Record Lookup** | Paste any record ID → full cryptographic provenance | `/records/{id}` |
| **Anchor Feed** | Real-time `Anchored` events from Polygon Amoy via POKT RPC | `/anchors` |
| **Decision Timeline** | Area/bar/line charts, configurable windows & groupings | `/records` |
| **Config History** | All threshold changes with documented reasons + impact | `/config` |
| **Diff Tool** | Compare two time windows → detect model drift | `/records` |
| **Export** | EU AI Act Article 13 compliance reports (JSON) | `/records/export/eu_ai_act` |

---

## Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Frontend       │────▶│   Backend        │────▶│  POKT Network    │
│   (React/Vite)   │     │  (FastAPI)       │     │  (Polygon Amoy)  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │decision-provenance│
                        │  (SQLite/WAL)    │
                        └──────────────────┘
```

---

## Quick Start (Local)

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker (optional)

### Development
```bash
# Clone
git clone https://github.com/hitcaff/decision-provenance-explorer.git
cd decision-provenance-explorer

# Frontend (Terminal 1)
cd frontend
cp .env.example .env  # VITE_API_BASE_URL=http://127.0.0.1:8000
npm install
npm run dev  # → http://localhost:5173

# Backend (Terminal 2)
cd ../backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
cp .env.example .env
uvicorn decision_provenance_explorer.main:app --reload  # → http://127.0.0.1:8000
```

### Docker
```bash
docker-compose up -d
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

---

## Production Deployment

### Frontend → Vercel
```bash
cd frontend
vercel --prod
# Set VITE_API_BASE_URL=https://your-api.onrender.com
```

### Backend → Render
```bash
# 1. Create Render Web Service
# 2. Build: pip install -e .
# 3. Start: uvicorn decision_provenance_explorer.main:app --host 0.0.0.0 --port $PORT
# 4. Add env vars: POKT_RPC_URL, CONTRACT_ADDRESS, DB_PATH=/data/provenance.db
# 5. Add persistent disk at /data
```

### Environment Variables
| Variable | Local | Production |
|---|---|---|
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000` | `https://api.yourdomain.com` |
| `POKT_RPC_URL` | `https://lb.nodies.app/v2/polygon-amoy` | Same |
| `CONTRACT_ADDRESS` | `0x31e8841C3511177847dbAbF289EdFC6f60CB1fb3` | Same |
| `DB_PATH` | `provenance.db` | `/data/provenance.db` |
| `CORS_ORIGINS` | `http://localhost:5173` | `https://your-frontend.vercel.app` |

---

## Contract Details

| Property | Value |
|---|---|
| **Contract** | ProvenanceRegistry |
| **Address** | `0x31e8841C3511177847dbAbF289EdFC6f60CB1fb3` |
| **Network** | Polygon Amoy (Chain ID: 80002) |
| **RPC** | POKT Network (`lb.nodies.app`) |
| **Live Anchor** | [View on Polygonscan](https://amoy.polygonscan.com/tx/27c82e2e48cc320b54bb0961dd8926234208eb58c2418c79dd88ca72c4363e12) |

---

## API Reference

### Records
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/records` | Search with filters |
| `GET` | `/records/{record_id}` | Single record provenance |
| `POST` | `/records` | Create decision record |
| `GET` | `/records/verify/chain` | Verify Merkle chain |
| `GET` | `/records/export/eu_ai_act` | EU AI Act Art. 13 report |

### Anchors
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/anchors` | All on-chain anchors |
| `GET` | `/anchors/latest` | Latest anchor event |
| `GET` | `/anchors/count` | Total anchor count |
| `GET` | `/anchors/verify/{chain_root}` | Verify root on-chain |

### Config
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/config` | All config versions |
| `GET` | `/config/genesis` | Genesis history |
| `GET` | `/config/label_registry` | Label ID → display mapping |

---

## Real Usage Example

```python
# Integrate into your ML pipeline
from decision_provenance import ProvenanceLogger

logger = ProvenanceLogger(
    model_id="loan_scorer_v2",
    model_version="2.3.1",
    db_path="provenance.db",
    evm_anchor_every=100,  # anchor every 100 decisions
    evm_config={
        "private_key": os.environ["SIGNER_KEY"],
        "contract_address": "0x8E6e5B00...",
        "rpc_url": os.environ["POKT_RPC_URL"],
    }
)

logger.init_chain(changed_by="ml_team", reason="production deploy v2.3.1")
logger.set_config(threshold=0.62, above_label="approved", below_label="denied",
                  changed_by="risk_team", change_reason="Q3 calibration")

@logger.log(score_fn=lambda out: out["score"])
def predict(features):
    return model(features)

# Every call automatically logs tamper-evident record + anchors to Polygon
result = predict({"income": 95000, "credit_score": 740})
```

Then view in dashboard: paste `record_id` → full provenance + on-chain verification.

---

## Built With

| Layer | Stack |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Recharts, ethers.js v6 |
| **Backend** | FastAPI, Pydantic 2, decision-provenance, web3.py v7 |
| **Blockchain** | Polygon Amoy, POKT Network (decentralized RPC) |
| **Database** | SQLite (WAL mode), decision-provenance Merkle chains |
| **Deploy** | Vercel (frontend), Render (backend), Docker Compose |

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Hackathon

Built for **POKT Network** — "Built on Pocket"

**Team:** Hitesh Srivastava  
**POKT Discord:** @hitcaff
