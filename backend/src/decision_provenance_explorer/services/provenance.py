"""
Service for interacting with the decision-provenance library.
"""
from typing import Optional, List, Dict, Any
from decision_provenance import ProvenanceLogger
from decision_provenance.config_record import ConfigRecord as DPConfigRecord
from decision_provenance.genesis import GenesisRecord as DPGenesisRecord
from ..core.config import settings
from ..models.schemas import (
    ConfigRecord, GenesisRecord, ProvenanceRecord, VerificationResult,
    EUAIActReport, RecordSearchParams, ConfigureRequest, InitChainRequest,
    SetConfigRequest, RecordDecisionRequest,
)


class ProvenanceService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.db_path
        self._logger: Optional[ProvenanceLogger] = None

    def _get_logger(self, config: Optional[ConfigureRequest] = None) -> ProvenanceLogger:
        if self._logger is None:
            cfg = config or ConfigureRequest()
            self._logger = ProvenanceLogger(
                model_id=cfg.model_id,
                model_version=cfg.model_version,
                model_hash=cfg.model_hash,
                db_path=cfg.db_path,
                input_schema_version=cfg.input_schema_version,
                ipfs_anchor=cfg.ipfs_anchor,
                pinata_jwt=cfg.pinata_jwt,
                ipfs_url=cfg.ipfs_url,
                evm_anchor_every=cfg.evm_anchor_every,
                evm_config=cfg.evm_config,
            )
        return self._logger

    def configure(self, config: ConfigureRequest) -> Dict[str, str]:
        self._logger = None
        logger = self._get_logger(config)
        return {"message": f"Logger configured for model {config.model_id} v{config.model_version}"}

    def init_chain(self, request: InitChainRequest) -> GenesisRecord:
        logger = self._get_logger()
        genesis = logger.init_chain(changed_by=request.changed_by, reason=request.reason)
        return GenesisRecord(
            genesis_id=genesis.genesis_id, model_id=genesis.model_id,
            created_by=genesis.created_by, reason=genesis.reason,
            schema_version=genesis.schema_version, timestamp_iso=genesis.timestamp_iso,
            genesis_hash=genesis.genesis_hash,
        )

    def set_config(self, request: SetConfigRequest) -> ConfigRecord:
        logger = self._get_logger()
        config = logger.set_config(
            threshold=request.threshold,
            above_label=request.above_label,
            below_label=request.below_label,
            config_version=request.config_version,
            changed_by=request.changed_by,
            change_reason=request.change_reason,
        )
        return ConfigRecord(
            config_id=config.config_id, model_id=config.model_id,
            config_version=config.config_version, threshold=config.threshold,
            threshold_label_id=config.threshold_label_id, changed_by=config.changed_by,
            change_reason=config.change_reason, timestamp_iso=config.timestamp_iso,
        )

    def record_decision(self, request: RecordDecisionRequest) -> ProvenanceRecord:
        logger = self._get_logger()
        result = logger.record(
            input_features=request.input_features,
            output=request.output,
            score=request.score,
            session_id=request.session_id,
        )
        return ProvenanceRecord(**result)

    def get_record(self, record_id: str) -> Optional[ProvenanceRecord]:
        logger = self._get_logger()
        chain = logger.chain
        record = chain.get_record(record_id)
        if record:
            return ProvenanceRecord(**record)
        return None

    def search_records(self, params: RecordSearchParams) -> List[ProvenanceRecord]:
        logger = self._get_logger()
        records = logger.search(
            label_id=params.label_id, label_display=params.label_display,
            date_from=params.date_from, date_to=params.date_to,
            genesis_id=params.genesis_id, schema_version=params.schema_version,
            limit=params.limit, offset=params.offset,
        )
        return [ProvenanceRecord(**r) for r in records]

    def verify_chain(self) -> VerificationResult:
        logger = self._get_logger()
        valid, message = logger.verify()
        return VerificationResult(
            valid=valid, message=message,
            current_root=logger.chain.current_root,
            record_count=logger.chain.record_count,
        )

    def export_eu_ai_act(self) -> EUAIActReport:
        logger = self._get_logger()
        report = logger.export_eu_ai_act()
        return EUAIActReport(**report)

    def get_configs(self) -> List[ConfigRecord]:
        logger = self._get_logger()
        configs = logger.configs.all_configs(logger.model_id)
        return [ConfigRecord(
            config_id=c.config_id, model_id=c.model_id,
            config_version=c.config_version, threshold=c.threshold,
            threshold_label_id=c.threshold_label_id, changed_by=c.changed_by,
            change_reason=c.change_reason, timestamp_iso=c.timestamp_iso,
        ) for c in configs]

    def get_genesis_history(self) -> List[GenesisRecord]:
        logger = self._get_logger()
        genesis_list = logger.genesis.all_for_model(logger.model_id)
        return [GenesisRecord(
            genesis_id=g.genesis_id, model_id=g.model_id,
            created_by=g.created_by, reason=g.reason,
            schema_version=g.schema_version, timestamp_iso=g.timestamp_iso,
            genesis_hash=g.genesis_hash,
        ) for g in genesis_list]

    def close(self):
        if self._logger:
            self._logger.close()
            self._logger = None


_provenance_service: Optional[ProvenanceService] = None


def get_provenance_service() -> ProvenanceService:
    global _provenance_service
    if _provenance_service is None:
        _provenance_service = ProvenanceService()
    return _provenance_service
