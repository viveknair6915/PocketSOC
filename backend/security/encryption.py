import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from backend.config import settings

class EncryptionUtils:
    def __init__(self):
        # Ensure key is 32 bytes for AES-256
        key_str = settings.AGENT_SECRET_KEY
        self.key = key_str.ljust(32)[:32].encode('utf-8')

    def decrypt_payload(self, encrypted_b64: str) -> str:
        """Decrypts AES-GCM encrypted payload."""
        try:
            data = base64.b64decode(encrypted_b64)
            # Layout: IV (12) + Tag (16) + Ciphertext
            iv = data[:12]
            tag = data[12:28]
            ciphertext = data[28:]
            
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            raise ValueError("Invalid encrypted payload")

encryption_utils = EncryptionUtils()
