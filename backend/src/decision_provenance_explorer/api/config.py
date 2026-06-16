"""
API Router for configuration history.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..services.provenance import get_provenance_service, ProvenanceService
from ..models.schemas import ConfigRecord, GenesisRecord

router = APIRouter()


@router.get("/", response_model=List[ConfigRecord])
async def list_configs(
    service: ProvenanceService = Depends(get_provenance_service),
):
    return service.get_configs()


@router.get("/genesis", response_model=List[GenesisRecord])
async def get_genesis_history(
    service: ProvenanceService = Depends(get_provenance_service),
):
    return service.get_genesis_history()


@router.get("/label_registry")
async def get_label_registry(
    service: ProvenanceService = Depends(get_provenance_service),
):
    logger = service._get_logger()
    return logger.labels.all_labels()
