import sqlite3
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

class database_encryption:
    private_key = None
    public_key = None
    key_dir = 'src'  # Directory where keys will be stored

    def __init__(self):
        if not os.path.exists(database_encryption.key_dir):
            os.makedirs(database_encryption.key_dir)

        if not os.path.exists(os.path.join(database_encryption.key_dir, 'private.pem')) or \
           not os.path.exists(os.path.join(database_encryption.key_dir, 'public.pem')):
            self.create_initial_keys()

        database_encryption.private_key = self.load_private_key()
        database_encryption.public_key = self.load_public_key()

    def create_initial_keys(self):
        # Generate RSA keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        with open(os.path.join(database_encryption.key_dir, 'private.pem'), 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(os.path.join(database_encryption.key_dir, 'public.pem'), 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_private_key(self):
        with open(os.path.join(database_encryption.key_dir, 'private.pem'), 'rb') as f:
            return serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        
    def load_public_key(self):
        with open(os.path.join(database_encryption.key_dir, 'public.pem'), 'rb') as f:
            return serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        
    def encrypt_data(data):
        data = str(data)

        # Encode the data to bytes
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
    
        # Encrypt data using public key
        cipher_text = database_encryption.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return sqlite3.Binary(cipher_text)

    def decrypt_data(encrypted_data):
        # Decrypt data using the private key
        decrypted_data = database_encryption.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode('utf-8')