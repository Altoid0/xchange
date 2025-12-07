import os
from session import Session
from crypto.rsa import RSA
from crypto.aes import AES

class SecretManager:
    def __init__ (self, session: Session):
        self.session = session
        self.aes = None

    def read_pair(self) -> tuple:
        # Check if priv.key exists in profile path
        priv_key_path = os.path.join(self.session.get_profile_path, "priv.key")
        profile_name = os.path.basename(self.session.get_profile_path)
        pub_key_path = os.path.join(self.session.get_shared_path, f"{profile_name}.key")
        if os.path.exists(priv_key_path) and os.path.exists(pub_key_path):
            with open(priv_key_path, "rb") as priv_file:
                private_key = priv_file.read()
            with open(pub_key_path, "rb") as pub_file:
                public_key = pub_file.read()
            print("Private key already exists. Key pair generation skipped.")
            return public_key, private_key
        else:
            return None, None

    def write_pair(self) -> None:
        public_key, private_key = RSA().generate_keypair()
        if public_key and private_key:
            # Write private key to profile path
            priv_key_path = os.path.join(self.session.get_profile_path, "priv.key")
            with open(priv_key_path, "wb") as priv_file:
                priv_file.write(private_key)
            
            # Write public key to shared path
            profile_name = os.path.basename(self.session.get_profile_path)
            pub_key_path = os.path.join(self.session.get_shared_path, f"{profile_name}.key")
            with open(pub_key_path, "wb") as pub_file:
                pub_file.write(public_key)
            
            print(f"Key pair generated and saved:\nPrivate Key: {priv_key_path}\nPublic Key: {pub_key_path}")

    def generate_pair(self) -> None:
        public_key, private_key = self.read_pair()
        if public_key is None or private_key is None:
            self.write_pair()

    def set_aes(self, aes: AES) -> None:
        self.aes = aes
