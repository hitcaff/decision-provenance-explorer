"""
API Router for decision records.
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel

from ..services.provenance import get_provenance_service, ProvenanceService
from ..models.schemas import (
    ProvenanceRecord, VerificationResult, EUAIActReport,
    RecordSearchParams, RecordDecisionRequest, ConfigureRequest,
    InitChainRequest, SetConfigRequest,
)

router = APIRouter()


class RecordResponse(BaseModel):
    data: Optional[ProvenanceRecord] = None
    error: Optional[str] = None


class RecordsResponse(BaseModel):
    data: List[ProvenanceRecord]
    total: int
    limit: int
    offset: int


@router.get("/")
async def list_records(
    label_id: Optional[str] = Query(None),
    label_display: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    genesis_id: Optional[str] = Query(None),
    schema_version: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ProvenanceService = Depends(get_provenance_service),
):
    params = RecordSearchParams(
        label_id=label_id, label_display=label_display,
        date_from=date_from, date_to=date_to,
        genesis_id=genesis_id, schema_version=schema_version,
        limit=limit, offset=offset,
    )
    records = service.search_records(params)
    total = len(records)  # simplified
    return RecordsResponse(data=records, total=total, limit=limit, offset=offset)


@router.get("/{record_id}")
async def get_record(
    record_id: str,
    service: ProvenanceService = Depends(get_provenance_service),
):
    record = service.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return RecordResponse(data=record)


@router.post("/", response_model=RecordResponse)
async def create_record(
    request: RecordDecisionRequest,
    service: ProvenanceService = Depends(get_provenance_service),
):
    try:
        record = service.record_decision(request)
        return RecordResponse(data=record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/verify/chain", response_model=VerificationResult)
async def verify_chain(
    service: ProvenanceService = Depends(get_provenance_service),
):
    return service.verify_chain()


@router.get("/export/eu_ai_act", response_model=EUAIActReport)
async def export_eu_ai_act(
    service: ProvenanceService = Depends(get_provenance_service),
):
    return service.export_eu_ai_act()


@router.post("/configure")
async def configure_logger(
    request: ConfigureRequest,
    service: ProvenanceService = Depends(get_provenance_service),
):
    return service.configure(request)


@router.post("/init_chain")
async def init_chain(
    request: InitChainRequest,
    service: ProvenanceService = Depends(get_provenance_service),
):
    try:
        genesis = service.init_chain(request)
        return genesis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/set_config")
async def set_config(
    request: SetConfigRequest,
    service: ProvenanceService = Depends(get_provenance_service),
):
    try:
        config = service.set_config(request)
        return config
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
