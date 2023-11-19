#coding=utf-8
import os
from web3 import Web3, HTTPProvider, Account
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

class InscriptionMinter(object):
    def __init__(self):
        self.private_key = os.getenv('PRIVATE_KEY')
        self.to_address = Web3.to_checksum_address(os.getenv('RECIPIENT_ADDRESS'))
        self.from_address = Account.from_key(self.private_key).address
        self.text_data = os.getenv('TEXT_DATA')
        self.rpc_url = os.getenv('RPC_URL')
        self.max_mint_times = int(os.getenv('MAX_MINT_TIMES'))
        self.wait_receipt = os.getenv('WAIT_RECEIPT') == '1'
        self._web3 = None

    def run(self):
        for i in range(self.max_mint_times):
            print(f"Mint {i+1} times, current balance fee: {self.balance_fee}")
            self.minting()
            print(f"{'-' * 20}\n")

    def minting(self):
        # send transaction
        transaction = self.build_signed_transaction()
        tx_hash = self.web3.eth.send_raw_transaction(transaction.rawTransaction)
        # Get the transaction hash
        print(f"Transaction hash: {tx_hash.hex()}")

        # check if transaction success
        if self.wait_receipt:
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction receipt: {tx_receipt}")
            if tx_receipt['status'] == 1:
                print(f"Transaction success, used {tx_receipt['gasUsed']} gas")
            else:
                print(f"Transaction failed")

    @property
    def web3(self):
        if self._web3 is None:
            self._web3 = Web3(HTTPProvider(self.rpc_url))
            self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            if not self._web3.is_connected():
                raise Exception('Not connected to Ethereum network')
            print(f"connected to Ethereum network: {self.rpc_url}")
        return self._web3


    @property
    def balance_fee(self):
        return Web3.from_wei(self.web3.eth.get_balance(self.from_address), 'ether')

    def build_signed_transaction(self):
        transaction = {
            'chainId': self.web3.eth.chain_id,
            'from': self.from_address,
            'to': self.to_address,
            'value': self.web3.to_wei(0, 'ether'),
            'data': self.web3.to_hex(text=self.text_data),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
            'gasPrice': self.web3.eth.gas_price
        }

        gas = self.web3.eth.estimate_gas(transaction)
        transaction['gas'] = gas
        print(f"Transaction: {transaction}")

        # Sign the transaction
        return self.web3.eth.account.sign_transaction(
            transaction,
            self.private_key
        )


if __name__ == '__main__':
    load_dotenv()
    InscriptionMinter().run()