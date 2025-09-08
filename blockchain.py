import hashlib
import json
import time
from typing import List


class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data  # dictionary: {filename, storage_path, uploader, ...}
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.data)}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self, difficulty=2, chain_file="chain.json"):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.chain_file = chain_file
        try:
            self.load_chain()
        except FileNotFoundError:
            self.chain = [self.create_genesis_block()]
            self.save_chain()

    def create_genesis_block(self):
        return Block(0, "0", time.time(), {"filename": "Genesis Block"}, 0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    def save_chain(self):
        with open(self.chain_file, "w") as f:
            json.dump(
                [b.__dict__ for b in self.chain],
                f,
                default=lambda o: o.__dict__,
                indent=4,
            )

    def load_chain(self):
        with open(self.chain_file, "r") as f:
            data = json.load(f)
            self.chain = []
            for b in data:
                block = Block(
                    b["index"],
                    b["previous_hash"],
                    b["timestamp"],
                    b["data"],
                    b["nonce"],
                )
                block.hash = b["hash"]
                self.chain.append(block)

    def find_by_filename(self, filename: str) -> List[Block]:
        out = []
        for b in self.chain:
            d = b.data
            if isinstance(d, dict) and filename.lower() in d.get("filename", "").lower():
                out.append(b)
        return out
