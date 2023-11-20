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
        self.max_priority_fee = float(os.getenv('MAX_PRIORITY_FEE'))
        self.rpc_url = os.getenv('RPC_URL')
        self.mint_times = int(os.getenv('MAX_MINT_TIMES'))
        self.wait_receipt = os.getenv('WAIT_RECEIPT') == '1'
        self._web3 = self._base_fee = self._eip1559_transaction = None

    def run(self):
        for i in range(self.mint_times):
            print(f"Mint {i+1} times, current balance fee: {self.balance_fee}")
            self.minting()
            print(f"{'-' * 20}\n")

    def minting(self):
        # send transaction
        transaction = self.build_eip1559_transaction()
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
                raise Exception('Not connected to Ethereum network\n')
            print(f"connected to Ethereum network: {self.rpc_url}\n")
        return self._web3

    @property
    def nonce(self):
        return self.web3.eth.get_transaction_count(self.from_address, 'pending')

    @property
    def balance_fee(self):
        return Web3.from_wei(self.web3.eth.get_balance(self.from_address), 'ether')

    def build_eip1559_transaction(self):
        if self._eip1559_transaction is None:
            # Estimate gas limit for the transaction
            value = self.web3.to_wei(0, 'ether')
            hex_data = self.web3.to_hex(text=self.text_data)
            gas_estimate = self.web3.eth.estimate_gas({
                'to': self.to_address,
                'value': value,
                'from': self.from_address,
                'data': hex_data
            })

            # EIP-1559 transaction parameters
            base_fee = self.web3.eth.get_block('latest')['baseFeePerGas']
            max_priority_fee_per_gas = self.web3.to_wei(self.max_priority_fee, 'gwei')
            max_fee_per_gas = base_fee + max_priority_fee_per_gas

            # Build eip1559 transaction
            self._eip1559_transaction = {
                'type': '0x2',  # Indicates an EIP-1559 transaction
                'chainId': self.web3.eth.chain_id,
                'maxPriorityFeePerGas': max_priority_fee_per_gas,
                'maxFeePerGas': max_fee_per_gas,
                'gas': gas_estimate,
                'to': self.to_address,
                'value': value,
                'data': hex_data
            }

        self._eip1559_transaction['nonce'] = self.nonce

        # Sign the transaction
        print(f"Transaction: {self._eip1559_transaction}")
        return self.web3.eth.account.sign_transaction(
            self._eip1559_transaction,
            self.private_key
        )


if __name__ == '__main__':
    load_dotenv()
    InscriptionMinter().run()