"""
Core configuration for the backend.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Decision Provenance Explorer API"
    debug: bool = False
    log_level: str = "INFO"

    # CORS
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://decision-provenance-explorer-me2k.vercel.app",
            "*",
        ],
        description="Allowed CORS origins",
    )

    # Database
    db_path: str = "provenance.db"

    # POKT Network RPC
    pokt_rpc_url: str = "https://poly-amoy-testnet.api.pocket.network"

    # Contract
    contract_address: str = "0x8E6e5B004818A796C8D4B098aCaD5cD86b9F4c32"

    # Address that signs and submits anchor() transactions (derived from
    # PROVENANCE_SIGNER_KEY at anchoring time). The registry contract indexes
    # anchors per-sender, so reads must query by THIS address, not contract_address.
    anchor_signer_address: str = "0x8e50426474338c47B5D4936176AD3D3Dba9261Ae"

    # Polygonscan API (for verification)
    polygonscan_api_key: str = ""

    # Model defaults
    default_model_id: str = "loan_scorer"
    default_model_version: str = "2.3.1"


settings = Settings()

