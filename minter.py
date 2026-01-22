from flask import Flask, jsonify, request
from pymacaroons import Macaroon, Verifier
from pymacaroons.verifier import Verifier as VerifierClass

app = Flask(__name__)

SECRET_KEY = 'primary-service-secret-key'
THIRD_PARTY_KEY = 'shared-secret-with-third-party'

@app.route('/macaroon', methods=['GET'])
def create_macaroon():
    m = Macaroon(
        location='http://localhost:5000',
        identifier='primary-key-id',
        key=SECRET_KEY
    )
    m.add_first_party_caveat('user = alice')
    m.add_third_party_caveat(
        location='http://localhost:5001',
        key=THIRD_PARTY_KEY,
        key_id='third-party-key-id'
    )
    return jsonify({'macaroon': m.serialize()})

@app.route('/verify', methods=['POST'])
def verify_macaroon():
    data = request.json
    try:
        m = Macaroon.deserialize(data['macaroon'])
        dm = Macaroon.deserialize(data['discharge'])
        v = Verifier(discharge_macaroons=[dm])
        v.satisfy_exact('user = alice')
        v.verify(m, SECRET_KEY)
        return jsonify({"status": "Success"})
    except Exception as e:
        return jsonify({"status": "Failed", "reason": str(e)}), 403

if __name__ == '__main__':
    app.run(port=5000, debug=True)