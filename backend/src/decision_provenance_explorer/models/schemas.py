"""
Pydantic models for API responses.
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProvenanceRecord(BaseModel):
    record_id: str
    session_id: Optional[str] = None
    timestamp_iso: str
    label_id: str
    label_display: str
    config_id: str
    genesis_id: str
    schema_version: str
    input_hash: str
    output_hash: str
    model_hash: str
    # The following are only known at the moment of record_decision() — the
    # underlying decision-provenance library does not persist score/threshold/
    # chain_root/record_count/input_features/output alongside the stored record
    # (it stores only the hashes, by design). They will be None on lookups via
    # get_record()/search_records() for previously-created records.
    score: Optional[float] = None
    threshold: Optional[float] = None
    chain_root: Optional[str] = None
    record_count: Optional[int] = None
    input_features: Optional[Dict[str, Any]] = None
    output: Optional[Dict[str, Any]] = None
    ipfs_receipt: Optional[Dict[str, Any]] = None
    evm_receipt: Optional[Dict[str, Any]] = None


class VerificationResult(BaseModel):
    valid: bool
    message: str
    current_root: str
    record_count: int


class ConfigRecord(BaseModel):
    config_id: str
    model_id: str
    config_version: str
    threshold: float
    threshold_label_id: str
    changed_by: str
    change_reason: str
    timestamp_iso: str


class GenesisRecord(BaseModel):
    genesis_id: str
    model_id: str
    created_by: str
    reason: str
    schema_version: str
    timestamp_iso: str
    genesis_hash: str


class AnchorEvent(BaseModel):
    sender: str
    root: str
    model_id: str
    record_count: int
    timestamp: int
    block_number: int
    transaction_hash: str


class EUAIActReport(BaseModel):
    report_schema: str
    generated_at: str
    system: Dict[str, str]
    genesis_history: List[GenesisRecord]
    label_registry: Dict[str, str]
    config_history: List[ConfigRecord]
    audit_summary: Dict[str, Any]
    records: List[Dict[str, Any]]


class RecordSearchParams(BaseModel):
    label_id: Optional[str] = None
    label_display: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    genesis_id: Optional[str] = None
    schema_version: Optional[str] = None
    limit: int = 100
    offset: int = 0


class ConfigureRequest(BaseModel):
    model_id: str = "loan_scorer"
    model_version: str = "2.3.1"
    model_hash: Optional[str] = None
    db_path: Optional[str] = None  # falls back to settings.db_path if not provided
    input_schema_version: str = "1.0"
    ipfs_anchor: bool = False
    pinata_jwt: Optional[str] = None
    ipfs_url: str = "http://localhost:5001"
    evm_anchor_every: int = 0
    evm_config: Optional[Dict[str, Any]] = None


class InitChainRequest(BaseModel):
    changed_by: str
    reason: str


class SetConfigRequest(BaseModel):
    threshold: float
    above_label: str
    below_label: str
    config_version: Optional[str] = None
    changed_by: str
    change_reason: str


class RecordDecisionRequest(BaseModel):
    input_features: Dict[str, Any]
    output: Dict[str, Any]
    score: float
    session_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    database_connected: bool
    contract_connected: bool
