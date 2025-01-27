from nacl.public import PublicKey, SealedBox
import base64

def encrypt_secret(public_key: str, secret_value: str) -> str:
    # Decode the base64 encoded public key
    public_key_bytes = base64.b64decode(public_key)
    
    # Create a PublicKey object
    key = PublicKey(public_key_bytes)
    
    # Create a SealedBox for encryption
    sealed_box = SealedBox(key)
    
    # Encrypt the secret value
    encrypted_bytes = sealed_box.encrypt(secret_value.encode('utf-8'))
    
    # Return the base64 encoded encrypted value
    return base64.b64encode(encrypted_bytes).decode('utf-8')