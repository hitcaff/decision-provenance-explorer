"""
API Router for on-chain anchors via POKT RPC.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from ..services.blockchain import get_blockchain_service, BlockchainService
from ..models.schemas import AnchorEvent

router = APIRouter()


@router.get("/", response_model=List[AnchorEvent])
async def list_anchors(
    service: BlockchainService = Depends(get_blockchain_service),
):
    if not service.is_connected():
        if not service.connect():
            raise HTTPException(status_code=503, detail="Unable to connect to POKT RPC")
    return service.get_all_anchors()


@router.get("/latest", response_model=Optional[AnchorEvent])
async def get_latest_anchor(
    service: BlockchainService = Depends(get_blockchain_service),
):
    if not service.is_connected():
        if not service.connect():
            raise HTTPException(status_code=503, detail="Unable to connect to POKT RPC")
    return service.get_latest_anchor()


@router.get("/count")
async def get_anchor_count(
    service: BlockchainService = Depends(get_blockchain_service),
):
    if not service.is_connected():
        if not service.connect():
            raise HTTPException(status_code=503, detail="Unable to connect to POKT RPC")
    count = service.get_anchor_count()
    return {"count": count}


@router.get("/verify/{chain_root}")
async def verify_chain_root(
    chain_root: str,
    service: BlockchainService = Depends(get_blockchain_service),
):
    if not service.is_connected():
        if not service.connect():
            raise HTTPException(status_code=503, detail="Unable to connect to POKT RPC")
    result = service.verify_root(chain_root)
    return result
