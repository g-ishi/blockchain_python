# one-note:セクション3　ブロックチェーンクラスの作成

import logging
import sys
import time
import hashlib
import json

import utils


# マイニングディフィカリティ
MINING_DIFICALITY = 3

# マイニングの報酬の送り元名
MINING_SENDER = 'The Block Chain'

# マイニングの報酬
MINING_REWORD = 1.0

# stream=sys.stdoutとすることで、標準出力にもログが出力される
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# ロガーを設定する　このモジュールがトップレベルモジュールではないので。
logger = logging.getLogger(__name__)

# コードスタイルで、クラスはobject継承するように書く方が見やすい


class BlockChain(object):
    def __init__(self, blockchain_address=None):
        """
        blockchain_address: マイニングの報酬を受け取るブロックチェーンアドレス
        transaction_pool: トランザクションプールを表す
        chain: ブロックチェーンのリストが入る　ブロックチェーンオブジェクトのリスト
        """
        self.transaction_pool = []
        self.chain = []
        self.blockchain_address = blockchain_address
        # ブロックチェーンの最初のブロックは、初期化時に作成しておく必要がある
        self.create_block(0, self.hash({}))

    def create_block(self, nonce, previous_hash):
        """ブロックチェーンを作成する関数

        作成したブロックをブロックチェーンのリストに追加し、
        トランザクションプールを空にする
        """
        # ブロックを作成
        block = {
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash,
        }

        # ブロックをソートする ハッシュ化したときに毎回同じハッシュ値になるように
        sorted_block = utils.sorted_dict_by_key(block)

        # ブロックを追加
        self.chain.append(sorted_block)

        # トランザクションプールを空にする
        self.transaction_pool = []

        return sorted_block

    def hash(self, block):
        """
        ブロックのハッシュ化を行う関数

        引数がソートされた状態のブロックとは限らないので、再度ソートしておく
        ハッシュ化するのに文字列にするので、json.dumpsを使用する
        """
        sorted_block = json.dumps(block, sort_keys=True)
        hash_value = hashlib.sha256(sorted_block.encode()).hexdigest()

        return hash_value

    def add_transaction(self, sender_blockchain_address, recipient_blockchain_address, value):
        """
        新しいトランザクションを作成し、トランザクションプールに追加する
        valueは金額を扱うので、floatでキャストする
        """
        # トランザクションを作成
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address': sender_blockchain_address,
            'recipient_blockchain_address': recipient_blockchain_address,
            'value': float(value),
        })

        # トランザクションプールに追加する
        self.transaction_pool.append(transaction)
        # 追加に成功したらTrue
        return True

    def valid_proof(self, transactions, prev_hash, nonce, difficulty=MINING_DIFICALITY):
        """
        nonceの計算を行う
        """
        # ハッシュ値の計算を行うブロックを定義しておく
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': prev_hash,
        })

        # ハッシュ値の計算を行う
        guess_hash = self.hash(guess_block)

        # マイニングディフィカリティに応じたルールで判断する
        return guess_hash[:difficulty] == '0' * difficulty

    def proof_of_work(self):
        """
        prev_hashとtransactionsから、nonceを計算する関数
        """
        transactions = self.transaction_pool.copy()
        prev_hash = self.hash(self.chain[-1])

        # 正しい解がもとまるまで、計算を続ける
        nonce = 0
        while self.valid_proof(transactions, prev_hash, nonce) is False:
            nonce += 1

        return nonce

    def mining(self):
        """
        マイニングを行うコアメソッド
        """
        # マイニングの報酬を提供するトランザクションをトランザクションプールに追加する
        self.add_transaction(
            sender_blockchain_address=MINING_SENDER,
            recipient_blockchain_address=self.blockchain_address,
            value=MINING_REWORD
        )
        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        # ログをjson形式で吐いておくと、ログ解析ツールが使いやすいなどのメリットがある
        logging.info({'action': 'mining', 'status': 'success'})
        return True

    def calculate_total_amount(self, blockchain_address):
        """
        引数のブロックチェーンアドレスが持つ金額を計算する
        ブロックチェーンの中からブロックを一個ずつ取り出して、トランザクションを漁って行く
        """
        total_amount = 0.0

        for block in self.chain:
            for transaction in block['transactions']:
                value = float(transaction['value'])
                # お金が送られてきた場合は、足す
                if blockchain_address == transaction['recipient_blockchain_address']:
                    total_amount += value
                # お金を送った場合は、引く
                if blockchain_address == transaction['sender_blockchain_address']:
                    total_amount -= value
        
        return total_amount


if __name__ == '__main__':
    # ブロックチェーンを作成する
    blockchain_address = 'my block chain address'
    block_chain = BlockChain(blockchain_address=blockchain_address)

    # ブロックチェーンにブロックを追加する
    block_chain.add_transaction('A', 'B', 1.0)
    block_chain.mining()
    utils.pprint(block_chain.chain)

    block_chain.add_transaction('C', 'D', 2.0)
    block_chain.add_transaction('X', 'Y', 3.0)
    block_chain.mining()
    utils.pprint(block_chain.chain)

    # 合計金額を出力する
    print('my', block_chain.calculate_total_amount(block_chain.blockchain_address))
    print('C', block_chain.calculate_total_amount('C'))
    print('D', block_chain.calculate_total_amount('D'))
