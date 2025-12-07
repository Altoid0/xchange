import os
import json
from typing import Optional
from session import Session
from crypto.aes import AES
from crypto.mac import MAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from history import History


class Receiver:
    def __init__(self, session: Session):
        self.session = session
        
    def load_private_key(self):
        priv_key_path = os.path.join(
            self.session.get_profile_path,
            "priv.key"
        )
        
        if not os.path.exists(priv_key_path):
            raise FileNotFoundError(
                f"Private key not found at {priv_key_path}. "
                "Generate keys first."
            )
        
        with open(priv_key_path, "rb") as f:
            private_key_data = f.read()
        
        # Deserialize private key
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=None
        )
        return private_key
    
    def decrypt_aes_key(self, encrypted_key: bytes, private_key) -> tuple:
        # Decrypt using RSA with OAEP padding
        decrypted_key_material = private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Split
        aes_key = decrypted_key_material[:32]
        iv = decrypted_key_material[32:48]
        
        return aes_key, iv
    
    def verify_mac(self, data: bytes, received_mac: bytes, aes_key: bytes) -> bool:
        mac_verifier = MAC(aes_key)
        return mac_verifier.verify(data, received_mac)
    
    def receive_message(self, transmission_file: str = "Transmitted_Data.json",
                       output_file: Optional[str] = None) -> str:
        # Read transmission file
        transmission_path = os.path.join(
            self.session.get_shared_path,
            transmission_file
        )
        
        if not os.path.exists(transmission_path):
            raise FileNotFoundError(
                f"Transmission file not found: {transmission_path}"
            )
        
        with open(transmission_path, "r") as f:
            data = json.load(f)
        
        history = History()
        history.decode(data)
        
        if not history.messages:
            raise ValueError("No messages found in transmission file")
        
        message = history.messages[0]
        print(f"Read encrypted data from {transmission_path}")
        
        # Load private key
        private_key = self.load_private_key()
        print(f"Loaded private key")
        
        # Extract encrypted AES key
        encrypted_aes_key = message.ciphertext[:256]
        encrypted_message = message.ciphertext[256:]
        
        # Decrypt AES key
        aes_key, iv = self.decrypt_aes_key(encrypted_aes_key, private_key)
        print(f"Decrypted AES key with RSA-2048")
        
        # Verify MAC
        if not self.verify_mac(message.ciphertext, message.mac, aes_key):
            raise ValueError(
                "MAC verification failed. Message may have been tampered with."
            )
        print(f"MAC verification successful")
        
        # Initialize AES cipher
        aes = AES(key=aes_key, iv=iv)
        
        # Decrypt message
        plaintext = aes.decrypt(encrypted_message)
        print(f"Decrypted message with AES-256-CBC")
        
        if output_file:
            output_path = os.path.join(
                self.session.get_profile_path,
                output_file
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(plaintext)
            print(f"Saved decrypted message to {output_path}")
        
        print("\n")
        print("Decrypted Message:")
        print("\n")
        print(plaintext)
        print("\n")
        
        return plaintext