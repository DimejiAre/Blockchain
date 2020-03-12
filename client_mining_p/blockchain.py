import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS


class Blockchain(object):
    def __init__(self):
        self.chain = [
        {
            'index': 1,
            'previous_hash': 1,
            'proof': 100,
            'timestamp': 1571852367.484206,
            'transactions': []
        },
        {
            'index': 2,
            'previous_hash': "ddf1adddad9af96695fda647492897f058aa702f806d7eaa21dfd46ecab0fcd1",
            'proof': 24368051,
            'timestamp': 1571852436.924649,
            'transactions': [
                {
                    'amount': 1,
                    'recipient': "Brian",
                    'sender': "0"
                }
            ]
        },
        {
            'index': 3,
            'previous_hash': "2fa2bcc7b423d5d74d621835b098842cf9dd34591bfc0e68800a41cf20b2ec90",
            'proof': 8132268,
            'timestamp': 1571852467.247827,
            'transactions': [
                {
                    'amount': 1,
                    'recipient': "Brian",
                    'sender': "0"
                }
            ]
        },
        {
            'index': 4,
            'previous_hash': "3f4b18d04371d8ce3129643ccf5ad46bb9943a87adf8c5addded0d3612128f59",
            'proof': 1301845,
            'timestamp': 1571852472.199991,
            'transactions': [
                {
                    'amount': 1,
                    'recipient': "Brian",
                    'sender': "0"
                }
            ]
        },
        {
            'index': 5,
            'previous_hash': "9177932144818f9c3072d11849251bdd31096621162f0e081016fa59e25010d2",
            'proof': 13176802,
            'timestamp': 1571852599.8256152,
            'transactions': [
                {
                    'amount': "3",
                    'recipient': "Beej",
                    'sender': "Brian"
                },
                {
                    'amount': 1,
                    'recipient': "Brian",
                    'sender': "0"
                }
            ]
        },
        {
            'index': 6,
            'previous_hash': "1e110e46bd7a6a86cd39c3adae667439a40e31b20db3b314bed5b1fa56c746ea",
            'proof': 41571496,
            'timestamp': 1571852940.9420102,
            'transactions': [
                {
                    'amount': ".5",
                    'recipient': "Brady",
                    'sender': "Beej"
                },
                {
                    'amount': ".5",
                    'recipient': "Elissa",
                    'sender': "Beej"
                },
                {
                    'amount': ".5",
                    'recipient': "Tom",
                    'sender': "Beej"
                },
                {
                    'amount': 1,
                    'recipient': "Brian",
                    'sender': "0"
                }
            ]
        }
    ]
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        # Use hashlib.sha256 to create a hash
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        


        # Return the hashed block string in hexadecimal format
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     block_string = json.dumps(block, sort_keys=True)
    #     proof = 0
    #     # loop while the return from a call to valid proof is False
    #     while self.valid_proof(block_string, proof) is False:
    #         proof += 1        
    #     # return proof
    #     return proof

    @staticmethod
    def valid_proof(block_string, proof):
        block_string = json.dumps(block_string, sort_keys=True)
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # set a initial guess concatonate block string and proof then encode them
        guess = f"{block_string}{proof}".encode()
        # create a guess hash and hexdigest it
        guess_hash = hashlib.sha256(guess).hexdigest()
        # then return True if the guess hash has the valid number of leading zeros otherwise return False
        return guess_hash[:6] == "000000"



# Instantiate our Node
app = Flask(__name__)
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()

    if not data['id'] or not data['proof']:
        return jsonify({"message":"Proof or Id not present"}), 400
        
    result = blockchain.valid_proof(blockchain.last_block, data['proof'])
    if result:
        blockchain.new_block(data['proof'], blockchain.hash(blockchain.last_block))
        return jsonify({"message": "New Block Forged"})
    else:
        return jsonify({"message": "Fail"})
        

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "length": len(blockchain.chain),
        "chain": blockchain.chain
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        "last_block": blockchain.last_block
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)