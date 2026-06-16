"""
API Router for health checks.
"""
from fastapi import APIRouter, Depends
from datetime import datetime

from ..services.provenance import get_provenance_service, ProvenanceService
from ..services.blockchain import get_blockchain_service, BlockchainService
from ..models.schemas import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check(
    provenance: ProvenanceService = Depends(get_provenance_service),
    blockchain: BlockchainService = Depends(get_blockchain_service),
):
    db_connected = False
    try:
        provenance._get_logger()
        db_connected = True
    except Exception:
        db_connected = False

    contract_connected = blockchain.is_connected()
    if not contract_connected:
        contract_connected = blockchain.connect()

    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        timestamp=datetime.utcnow().isoformat() + "Z",
        database_connected=db_connected,
        contract_connected=contract_connected,
    )
