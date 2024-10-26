from jose import jwt
from jwt import PyJWKClient
import json
import base64
from cryptography.hazmat.primitives import serialization

# URL del JWKS de Auth0
jwks_url = "https://dev-k8isc1a1s4ms6dur.us.auth0.com/.well-known/jwks.json"

# Función para validar el token JWT
def validate_jwt_token(token):
    jwks_client = PyJWKClient(jwks_url)
    try:
        rsa_key = jwks_client.get_signing_key_from_jwt(token).key
        print(f"typekey: {type(rsa_key)}")
        # Pasamos a pem
        rsa_key_pem = rsa_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        decoded = jwt.decode(
            token,
            rsa_key_pem,
            algorithms=["RS256"],
            audience="https://dev-k8isc1a1s4ms6dur.us.auth0.com/api/v2/"
        )
        return decoded
    except Exception as e:
        print(f"Error decoding JWT: {e}")
        return None