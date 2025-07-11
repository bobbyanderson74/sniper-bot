import requests
import json
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from base58 import b58decode
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
from solana.system_program import TransferParams, transfer

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
client = Client(SOLANA_RPC)

class PhantomWallet:
    def __init__(self, private_key):
        secret_key = b58decode(private_key)
        self.keypair = Keypair.from_bytes(secret_key)
        self.public_key = self.keypair.pubkey()

    def buy_token(self, token_address, amount_sol=0.1):
        try:
            url = "https://quote-api.jup.ag/v6/swap"
            params = {
                "inputMint": "So11111111111111111111111111111111111111112",  # SOL
                "outputMint": token_address,
                "amount": int(amount_sol * 1_000_000_000),
                "slippage": 2,
                "userPublicKey": str(self.public_key),
                "wrapUnwrapSOL": True
            }
            res = requests.get(url, params=params)
            data = res.json()

            swap_tx = data.get("swapTransaction")
            if not swap_tx:
                print("❌ No transaction returned from Jupiter.")
                return None

            from base64 import b64decode, b64encode
            tx_bytes = b64decode(swap_tx)
            tx = Transaction.deserialize(tx_bytes)
            tx.sign([self.keypair])
            signed_tx = b64encode(tx.serialize()).decode()

            result = client.send_raw_transaction(signed_tx, opts=TxOpts(skip_confirmation=False, preflight_commitment="confirmed"))
            print(f"✅ Buy TX hash: {result['result']}")
            return result["result"]

        except Exception as e:
            print(f"❌ Error buying token: {e}")
            return None

    def sell_token(self, token_address):
        # You can customize this using Jupiter too
        print("🔁 Selling logic placeholder...")
        return "sell-tx-hash-placeholder"
