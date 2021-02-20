import Blockchain
import requests
import jsonpickle


class BlockchainManager:
    def __init__(self, address, known_address):
        self.address = address
        self.addresses = []
        if known_address != "0":
            self.addresses.append(known_address)
            self.get_addresses(known_address)
        blockchains = []
        # for address in self.addresses:
        #     blockchains.append(self.get_blockchain(address))
        # longest_blockchain = self.get_longest_blockchain(blockchains)
        # self.blockchain = longest_blockchain

    def get_addresses(self, known_address):
        r = requests.get(url="http://" + known_address + ":5000/connected_addresses")
        addresses = r.json()["addresses"]
        self.addresses.append(addresses)
        # send req to known_address for adresses
        # append these to self.addresses
        for address in self.addresses:
            json = {"address_to_add": self.address}
            r = requests.post(url="http://" + address + ":5000/add_address", json=json)

    def get_blockchain(self, target_address):
        # get the blockchain from target address
        pass

    def get_longest_blockchain(self, blockchains):
        longest_blockchain = Blockchain.Blockchain()
        for blockchain in blockchains:
            if blockchain.verify_chain():
                if len(blockchain.chain) > len(longest_blockchain.chain):
                    longest_blockchain = blockchain
        return longest_blockchain


from flask import Flask, request, render_template
from Crypto.PublicKey import RSA


address = input("Enter address")
known_address = input("Enter known address")
blockchain_manager = BlockchainManager(address, known_address)
app = Flask(__name__)


@app.route('/connected_addresses', methods=['GET'])
def connected_addresses():
    return jsonpickle.encode(blockchain_manager)


@app.route('/add_address', methods=['POST'])
def add_address():
    address_to_add = request.form['address_to_add']
    blockchain_manager.addresses.append(address_to_add)
    return "Success"


'''
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_string = blockchain.get_chain().replace("\n", "<br>")
    return chain_string


@app.route('/add_article', methods=['GET'])
def show_article_form():
    return render_template("form.html")


@app.route('/add_article', methods=['POST'])
def add_article():
    text = request.form['text']
    public_key = request.form['public_key']
    private_key = request.form['private_key']
    n = request.form['n']
    if blockchain.add_new_article(Article(text, public_key, private_key, n)):
        return blockchain.unconfirmed_articles[-1].text
    return "unsuccessful"


@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine()
    return "New block mined"


@app.route('/get_key', methods=['GET'])
def get_key():
    keyPair = RSA.generate(bits=1024)
    toRet = ""
    toRet += f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})"
    toRet += f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})"
    return toRet
'''

app.run(host="0.0.0.0", port=5000, debug=True)
