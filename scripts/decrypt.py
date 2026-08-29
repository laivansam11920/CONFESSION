from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from configs import Config

def decrypt_data(packed_data: bytes) -> str:

    salt = packed_data[:16]
    iv = packed_data[16:28]
    ciphertext = packed_data[28:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    key = kdf.derive(Config.SECRET_KEY.encode('utf-8'))

    aesgcm = AESGCM(key)
    decrypted_bytes = aesgcm.decrypt(iv, ciphertext, associated_data=None)
    return decrypted_bytes.decode('utf-8')
