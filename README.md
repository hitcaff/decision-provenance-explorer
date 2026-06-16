# Decision Provenance Explorer

Real-time audit trail dashboard for ML decisions with cryptographic verification on Polygon Amoy via POKT Network.

## Overview

The Decision Provenance Explorer is a web dashboard that provides visibility into tamper-evident ML decision logs. It connects to:

- **POKT Network** decentralized RPC for trustless on-chain verification
- **Polygon Amoy** testnet where the ProvenanceRegistry contract is deployed
- **decision-provenance** Python library for Merkle-chained decision records

## Features

| Feature | Description |
|---------|-------------|
| **Record Lookup** | Paste any record ID to see full cryptographic provenance |
| **Anchor Feed** | Real-time anchoring events from Polygon Amoy via POKT RPC |
| **Decision Timeline** | Visual chart of decisions over time (area/bar/line) |
| **Config History** | All threshold changes with documented reasons |
| **Diff Tool** | Compare two time windows to detect model drift |
| **Export** | EU AI Act Article 13 compliance reports |

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Frontend      │────▶│    Backend       │────▶│  POKT Network    │
│   (React/Vite)  │     │  (FastAPI)       │     │  (Polygon Amoy)  │
└─────────────────┘     └──────────────────┘     └──────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │decision-provenance│
                        │   (SQLite)        │
                        └──────────────────┘
```

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker (optional)

### Development

```bash
# Clone and enter project
cd decision-provenance-explorer

# Start frontend
cd frontend
npm install
npm run dev

# Start backend (in another terminal)
cd backend
pip install -e .
uvicorn decision_provenance_explorer.main:app --reload
```

### Docker

```bash
docker-compose up -d
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Contract Details

| Property | Value |
|----------|-------|
| **Contract** | ProvenanceRegistry |
| **Address** | `0x8E6e5B004818A796C8D4B098aCaD5cD86b9F4c32` |
| **Network** | Polygon Amoy (Chain ID: 80002) |
| **RPC** | POKT Network (`lb.nodies.app`) |
| **Live Anchor** | [View on Polygonscan](https://amoy.polygonscan.com/tx/a22f89733295a729b0d7142b49e13da49d1a6340836cde3a33d5d3be79edc7f5) |

## API Endpoints

### Records
- `GET /records` - Search records with filters
- `GET /records/{record_id}` - Get single record
- `POST /records` - Create new decision record
- `GET /records/verify/chain` - Verify Merkle chain
- `GET /records/export/eu_ai_act` - Export compliance report

### Anchors
- `GET /anchors` - List all on-chain anchors
- `GET /anchors/latest` - Get latest anchor
- `GET /anchors/count` - Total anchor count
- `GET /anchors/verify/{chain_root}` - Verify root on-chain

### Config
- `GET /config` - List all configuration versions
- `GET /config/current` - Get current config
- `GET /config/genesis` - Genesis history

## Built With

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, ethers.js
- **Backend**: FastAPI, Pydantic, decision-provenance, web3.py
- **Infrastructure**: POKT Network, Polygon Amoy, Docker

## License

MIT License - see LICENSE file for details.

## Hackathon

Built for **POKT Network Build Week 1** - "Built on Pocket"