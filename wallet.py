import requests
from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from base58 import b58decode
import json

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
client = Client(SOLANA_RPC)

class PhantomWallet:
    def __init__(self, private_key, public_key):
        self.private_key = b58decode(private_key)
        self.keypair = Keypair.from_secret_key(self.private_key)
        self.public_key = public_key

    def buy_token(self, token_address, amount_sol=0.1):
        try:
            url = "https://quote-api.jup.ag/v6/swap"
            params = {
                "inputMint": "So11111111111111111111111111111111111111112",
                "outputMint": token_address,
                "amount": int(amount_sol * 1_000_000_000),
                "slippage": 2,
                "userPublicKey": self.public_key,
                "wrapUnwrapSOL": True
            }

            res = requests.get(url, params=params)
            data = res.json()
            swap_tx = data.get("swapTransaction")
            if not swap_tx:
                return None

            tx_bytes = b58decode(swap_tx)
            tx = Transaction.deserialize(tx_bytes)
            tx.recent_blockhash = client.get_recent_blockhash()["result"]["value"]["blockhash"]
            tx.fee_payer = self.keypair.public_key
            tx_sig = client.send_transaction(tx, self.keypair, opts=TxOpts(skip_confirmation=False))
            return tx_sig.get("result")
        except:
            return None

    def sell_token(self, token_address):
        return self.buy_token("So11111111111111111111111111111111111111112")
