from flask import Flask, jsonify, request
import jwt
import time

app = Flask(__name__)

# Generate an initial key
generate_rsa_key()

# JWKS endpoint to return public keys that haven't expired
@app.route('/jwks', methods=['GET'])
def jwks():
    active_key = get_active_key()
    if active_key:
        jwk = {
            'kty': 'RSA',
            'kid': active_key['kid'],
            'use': 'sig',
            'alg': 'RS256',
            'n': active_key['public_key'].decode('utf-8'),  # Convert to JWK format
            'e': 'AQAB'
        }
        return jsonify({'keys': [jwk]})
    return jsonify({'keys': []}), 404

# Authentication endpoint to issue a JWT
@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired', 'false').lower() == 'true'
    key = get_expired_key() if expired else get_active_key()

    if not key:
        return jsonify({'error': 'No valid keys available'}), 400

    token = jwt.encode({'user': 'fake-user', 'exp': time.time() + 3600}, key['private_key'], algorithm='RS256', headers={'kid': key['kid']})
    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(port=8080)
