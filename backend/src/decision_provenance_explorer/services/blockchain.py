"""
Service for interacting with the Polygon Amoy blockchain via POKT RPC.
"""
import json
from typing import Optional, List
from web3 import Web3
from web3.contract import Contract
from web3.types import FilterParams
from ..core.config import settings
from ..models.schemas import AnchorEvent


PROVENANCE_REGISTRY_ABI = json.loads("""[
  {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"bytes32","name":"root","type":"bytes32"},{"indexed":false,"internalType":"string","name":"modelId","type":"string"},{"indexed":false,"internalType":"uint256","name":"recordCount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"Anchored","type":"event"},
  {"inputs":[{"internalType":"bytes32","name":"root","type":"bytes32"},{"internalType":"string","name":"modelId","type":"string"},{"internalType":"uint256","name":"recordCount","type":"uint256"}],"name":"anchor","outputs":[],"stateMutability":"nonpayable","type":"function"},
  {"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"getAnchorCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
  {"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getAnchor","outputs":[{"internalType":"bytes32","name":"root","type":"bytes32"},{"internalType":"string","name":"modelId","type":"string"},{"internalType":"uint256","name":"recordCount","type":"uint256"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"}
]""")


class BlockchainService:
    def __init__(self):
        self.w3: Optional[Web3] = None
        self.contract: Optional[Contract] = None
        self._connected = False

    def connect(self) -> bool:
        try:
            self.w3 = Web3(Web3.HTTPProvider(settings.pokt_rpc_url))
            if self.w3.is_connected():
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(settings.contract_address),
                    abi=PROVENANCE_REGISTRY_ABI,
                )
                self._connected = True
                return True
        except Exception as e:
            print(f"Failed to connect to POKT RPC: {e}")
        self._connected = False
        return False

    def is_connected(self) -> bool:
        return self._connected

    def get_anchor_count(self) -> int:
        if not self._connected or not self.contract:
            raise RuntimeError("Not connected to blockchain")
        deployer = Web3.to_checksum_address(settings.contract_address)
        count = self.contract.functions.getAnchorCount(deployer).call()
        return count

    def get_latest_anchor(self) -> Optional[AnchorEvent]:
        if not self._connected or not self.contract:
            raise RuntimeError("Not connected to blockchain")
        try:
            deployer = Web3.to_checksum_address(settings.contract_address)
            count = self.get_anchor_count()
            if count == 0:
                return None
            root, model_id, record_count, timestamp = self.contract.functions.getAnchor(
                deployer, count - 1
            ).call()
            return AnchorEvent(
                sender=deployer,
                root=root.hex() if isinstance(root, bytes) else root,
                model_id=model_id,
                record_count=record_count,
                timestamp=timestamp,
                block_number=0,
                transaction_hash="",
            )
        except Exception as e:
            print(f"Failed to get latest anchor: {e}")
            return None

    def get_all_anchors(self) -> List[AnchorEvent]:
        if not self._connected or not self.contract:
            raise RuntimeError("Not connected to blockchain")
        anchors = []
        deployer = Web3.to_checksum_address(settings.contract_address)
        count = self.get_anchor_count()
        for i in range(count):
            try:
                root, model_id, record_count, timestamp = self.contract.functions.getAnchor(
                    deployer, i
                ).call()
                anchors.append(AnchorEvent(
                    sender=deployer,
                    root=root.hex() if isinstance(root, bytes) else root,
                    model_id=model_id,
                    record_count=record_count,
                    timestamp=timestamp,
                    block_number=0,
                    transaction_hash="",
                ))
            except Exception as e:
                print(f"Failed to get anchor {i}: {e}")
        return anchors

    def verify_root(self, chain_root: str) -> dict:
        if not self._connected or not self.contract:
            return {"verified": False, "message": "Not connected to blockchain"}
        try:
            deployer = Web3.to_checksum_address(settings.contract_address)
            count = self.get_anchor_count()
            target_root = chain_root.lower()
            if not target_root.startswith("0x"):
                target_root = "0x" + target_root
            for i in range(count - 1, -1, -1):
                root, model_id, record_count, timestamp = self.contract.functions.getAnchor(
                    deployer, i
                ).call()
                root_hex = root.hex() if isinstance(root, bytes) else root
                if root_hex.lower() == target_root:
                    return {
                        "verified": True,
                        "anchor": AnchorEvent(
                            sender=deployer, root=root_hex, model_id=model_id,
                            record_count=record_count, timestamp=timestamp,
                            block_number=0, transaction_hash="",
                        ),
                        "message": f"Chain root verified on Polygon Amoy at anchor index {i}",
                    }
            return {"verified": False, "message": "Chain root not found in any on-chain anchor"}
        except Exception as e:
            return {"verified": False, "message": f"Verification failed: {str(e)}"}


_blockchain_service: Optional[BlockchainService] = None


def get_blockchain_service() -> BlockchainService:
    global _blockchain_service
    if _blockchain_service is None:
        _blockchain_service = BlockchainService()
        _blockchain_service.connect()
    return _blockchain_service
