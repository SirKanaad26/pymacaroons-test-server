from flask import Flask, request, jsonify
from pymacaroons import Macaroon

app = Flask(__name__)
THIRD_PARTY_KEY = 'shared-secret-with-third-party'

@app.route('/discharge', methods=['POST'])
def discharge():
    key_id = request.json.get('key_id')
    dm = Macaroon(location='http://localhost:5001', identifier=key_id, key=THIRD_PARTY_KEY)
    return jsonify({'discharge_macaroon': dm.serialize()})

if __name__ == '__main__':
    app.run(port=5001)