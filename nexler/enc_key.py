import os
import traceback

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from nexler.utils import dir_util


def generate_enc_key():
    try:
        # Generate RSA private key
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Serialize private key to PEM format for saving securely
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Serialize public key to PEM format for sharing with other services if needed
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        directory = "encryption/"
        if not os.path.exists(f"{directory}private_key.pem"):
            dir_util.create_directory(directory)

            # Save keys securely in files or a key management service
            with open(f"{directory}private_key.pem", "wb") as f:
                f.write(pem_private_key)
            with open(f"{directory}public_key.pem", "wb") as f:
                f.write(pem_public_key)
            print("Encryption Keys generated successfully.")
        else:
            print('Encryption keys already exists.')
    except Exception as e:
        print(f"An error occurred while creating the component: {e}, Trace: {traceback.format_exc()}")
