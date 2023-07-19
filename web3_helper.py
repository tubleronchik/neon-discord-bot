import web3
import json
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_account import Account

from utils import to_thread

def download_xrt_abi() -> dict:
    with open("abi/XRT.json") as f:
        xrt_abi = json.load(f)
    return xrt_abi

def setup_provider(http_provider: str, pk) -> web3.Web3:
    provider_account = Account.from_key(pk)
    w3 = web3.Web3(web3.Web3.HTTPProvider(http_provider))
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(provider_account))
    return w3

def get_contract(w3: web3.Web3, xrt_address: str) -> web3.contract.Contract:
    abi = download_xrt_abi()
    return w3.eth.contract(address=xrt_address, abi=abi)

@to_thread
def transfer(xrt: web3.contract.Contract, w3: web3.Web3, address: str, contract_owner: str, amount: int) -> str:
    tx = xrt.functions.transfer(address, amount).transact({"from": contract_owner})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx)
    return tx_receipt.transactionHash.hex()

