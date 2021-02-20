from flask import Flask, request, render_template

from Crypto.PublicKey import RSA

from Blockchain import *

app = Flask(__name__)
blockchain = Blockchain()


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
    toRet += "Public key:  (n={}, e={})".format(hex(keyPair.n), hex(keyPair.e))
    toRet += "Private key: (n={}, d={})".format(hex(keyPair.n), hex(keyPair.d))
    return toRet


app.run(host="0.0.0.0", port=5000)

