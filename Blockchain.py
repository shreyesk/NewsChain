from hashlib import sha256, sha512
import time
import jsonpickle


class Article:
    def __init__(self, text, public_key, private_key, n):
        self.text = text
        self.public_key = int(public_key, 16)
        self.n = int(n, 16)
        hash_val = int.from_bytes(sha512(self.text.encode()).digest(), byteorder='big')
        self.signature = pow(hash_val, int(private_key, 16), self.n)

    def verify_signature(self):
        hash_val = int.from_bytes(sha512(self.text.encode()).digest(), byteorder='big')
        hash_from_signature = pow(self.signature, self.public_key, self.n)
        return hash_val == hash_from_signature

    def get_data(self):
        data = str(self.text) + str(self.public_key) + str(self.n) + str(self.signature)
        return data


class Block:
    def __init__(self, index, articles, timestamp, previous_hash):
        self.index = index
        self.articles = articles
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = ""

    def compute_hash(self):
        articles_string = ""
        for article in self.articles:
            articles_string += article.get_data()
        block_string = (str(self.index) + articles_string +
                        str(self.timestamp) + self.previous_hash +
                        str(self.nonce))
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 4

    def __init__(self):
        self.unconfirmed_articles = []
        self.chain = []
        self.create_genesis_block()
        self.load_from_file("example_chain")

    def load_from_pickle(self, pickle):
        new_blockchain = jsonpickle.decode(pickle)
        self.__dict__.update(new_blockchain.__dict__)

    def load_from_file(self, file_name):
        self.chain = []
        with open(file_name) as f:
            json_string = f.readline()
            self.load_from_pickle(json_string)


    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0" * self.difficulty)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_block(self, block, proof):
        previous_hash = self.chain[-1].hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith("0" * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def passes_filter(self, article):
        if article.verify_signature():
            return True
        return False

    # adds a received article if it passes the desired filters
    def add_new_article(self, article):
        if self.passes_filter(article):
            self.unconfirmed_articles.append(article)
            return True
        return False

    def mine(self):
        if not self.unconfirmed_articles:
            return False

        last_block = self.chain[-1]

        new_block = Block(index=last_block.index + 1,
                          articles=self.unconfirmed_articles,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_articles = []
        return new_block.index

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            # check hashes first
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]
            if curr_block.compute_hash() != curr_block.hash:
                return False
            if curr_block.previous_hash != prev_block.hash:
                return False
        return True

    def get_chain(self):
        return jsonpickle.encode(self)
        # chain_string = ""
        # chain_string += "blocks: " + str(len(self.chain)) + "\n\n\n\n"
        # for block in self.chain:
        #     block_string = ""
        #     block_string += "index: " + str(block.index) + "\n"
        #     block_string += "articles: " + str(len(block.articles)) + "\n\n"
        #     for article in block.articles:
        #         article_string = ""
        #         article_string += str(article.text.decode()) + "\n"
        #         article_string += "public: " + str(article.public_key) + "\n"
        #         article_string += "n: " + str(article.n) + "\n"
        #         article_string += "signature: " + str(article.signature) + "\n"
        #         block_string += article_string + "\n"
        #     block_string += "timestamp: " + str(block.timestamp) + "\n"
        #     block_string += "previous: " + str(block.previous_hash) + "\n"
        #     block_string += "nonce: " + str(block.nonce) + "\n"
        #     block_string += "hash: " + str(block.hash) + "\n\n"
        #     chain_string += block_string + "\n"
        # return chain_string
