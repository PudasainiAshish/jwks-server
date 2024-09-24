from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import time
import uuid

# Key store with expiry time (in seconds)
key_store = []

def generate_rsa_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    kid = str(uuid.uuid4())  # Generate a unique Key ID
    expiry = int(time.time()) + 3600  # 1-hour expiry
    
    key_entry = {
        'kid': kid,
        'private_key': private_key,
        'public_key': public_key,
        'expiry': expiry
    }
    
    key_store.append(key_entry)
    return key_entry

def get_active_key():
    current_time = int(time.time())
    active_keys = [key for key in key_store if key['expiry'] > current_time]
    return active_keys[0] if active_keys else None

def get_expired_key():
    expired_keys = [key for key in key_store if key['expiry'] <= int(time.time())]
    return expired_keys[0] if expired_keys else None
