import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from agent_config import config

class CryptoUtils:
    def __init__(self):
        # Ensure key is 32 bytes for AES-256
        key_str = config.AGENT_SECRET_KEY
        self.key = key_str.ljust(32)[:32].encode('utf-8')

    def encrypt_payload(self, plaintext: str) -> str:
        """Encrypts data using AES-256-GCM."""
        iv = os.urandom(12) # GCM recommends 12 bytes IV
        
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        
        # Combine IV + SC_TAG + CIPHERTEXT just like a standard envelope or separate
        # Common format: IV (12) + Tag (16) + Ciphertext
        encrypted_data = iv + encryptor.tag + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt_payload(self, encrypted_b64: str) -> str:
        """Decrypts data (mostly for verify/testing)."""
        data = base64.b64decode(encrypted_b64)
        iv = data[:12]
        tag = data[12:28]
        ciphertext = data[28:]
        
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')

if __name__ == "__main__":
    crypto = CryptoUtils()
    enc = crypto.encrypt_payload("Sensitive Data")
    print(f"Encrypted: {enc}")
    dec = crypto.decrypt_payload(enc)
    print(f"Decrypted: {dec}")
