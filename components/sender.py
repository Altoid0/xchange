import os
import json
from typing import Optional
from session import Session
from crypto.aes import AES
from crypto.mac import MAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization
from history import Message, History


class Sender:
    def __init__(self, session: Session):
        self.session = session
        # Generate new AES key for this session
        self.aes = AES()
        
    def load_receiver_public_key(self, receiver_name: str):
        pub_key_path = os.path.join(
            self.session.get_shared_path, 
            f"{receiver_name}.key"
        )
        
        if not os.path.exists(pub_key_path):
            raise FileNotFoundError(
                f"Receiver's public key not found at {pub_key_path}"
            )
        
        with open(pub_key_path, "rb") as f:
            public_key_data = f.read()
        
        # Deserialize public key
        public_key = serialization.load_pem_public_key(public_key_data)
        return public_key
    
    def encrypt_aes_key(self, public_key) -> bytes:
        key_material = self.aes.get_key + self.aes.get_iv
        
        # Encrypt using RSA with OAEP padding
        encrypted_key = public_key.encrypt(
            key_material,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key
    
    def generate_mac(self, data: bytes) -> bytes:
        mac_generator = MAC(self.aes.get_key)
        return mac_generator.generate(data)
    
    def send_message(self, plaintext_file: str, receiver_name: str, 
                     transmission_file: str = "Transmitted_Data.json") -> None:
        # Read plaintext
        if not os.path.exists(plaintext_file):
            raise FileNotFoundError(f"Message file not found: {plaintext_file}")
        
        with open(plaintext_file, "r", encoding="utf-8") as f:
            plaintext = f.read()
        
        print(f"Read message from {plaintext_file}")
        
        # Encrypt message
        encrypted_message = self.aes.encrypt(plaintext)
        print(f"Encrypted message with AES-256-CBC")
        
        # Load receiver's public key
        receiver_public_key = self.load_receiver_public_key(receiver_name)
        encrypted_aes_key = self.encrypt_aes_key(receiver_public_key)
        print(f"Encrypted AES key with RSA-2048")
        
        # Create combined ciphertext
        combined_ciphertext = encrypted_aes_key + encrypted_message
        
        # Generate MAC
        mac = self.generate_mac(combined_ciphertext)
        print(f"Generated HMAC-SHA256 for authentication")
        
        # Create message object
        message = Message(
            ciphertext=combined_ciphertext,
            mac=mac,
            iv=self.aes.get_iv  # initial message
        )
        
        # Write to transmission file
        history = History()
        history.messages.append(message)
        
        transmission_path = os.path.join(
            self.session.get_shared_path,
            transmission_file
        )
        
        with open(transmission_path, "w") as f:
            json.dump(history.encode(), f, indent=2)
        
        print(f"Message transmitted to {transmission_path}")
        print(f"\nTransmission Summary:")
        print(f"Encrypted AES Key: {len(encrypted_aes_key)} bytes")
        print(f"Encrypted Message: {len(encrypted_message)} bytes")
        print(f"MAC: {len(mac)} bytes")
        print(f"Total Size: {len(combined_ciphertext) + len(mac)} bytes")