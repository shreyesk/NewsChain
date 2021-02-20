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
    toRet += f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})"
    toRet += f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})"
    return toRet


app.run(debug=True, port=5000)

