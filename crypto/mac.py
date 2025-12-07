from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac as crypto_hmac
from cryptography.exceptions import InvalidSignature
import hmac


class MAC:
    def __init__(self, key: bytes):
        self.key = key
    
    def generate(self, data: bytes) -> bytes:
        h = crypto_hmac.HMAC(self.key, hashes.SHA256())
        h.update(data)
        return h.finalize()
    
    def verify(self, data: bytes, received_mac: bytes) -> bool:
        h = crypto_hmac.HMAC(self.key, hashes.SHA256())
        h.update(data)
        
        try:
            expected_mac = h.finalize()
            return hmac.compare_digest(expected_mac, received_mac)
        except InvalidSignature:
            return False