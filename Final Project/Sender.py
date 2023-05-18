import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Sender's RSA key generation
sender_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

sender_public_key = sender_private_key.public_key()

# Save sender's RSA private key to a file
with open('./sender/private_key.pem', 'wb') as private_key_file:
    private_key_file.write(
        sender_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Save sender's RSA public key to a file
with open('./sender/public_key.pem', 'wb') as public_key_file:
    public_key_file.write(
        sender_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

# Receiver's RSA public key loading
with open('./receiver/public_key.pem', 'rb') as public_key_file:
    receiver_public_key = serialization.load_pem_public_key(
        public_key_file.read(),
        backend=default_backend()
    )

# AES key generation and encryption with receiver's RSA public key
aes_key = os.urandom(32)  # 256-bit AES key

rsa_encrypted_aes_key = receiver_public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Message encryption using AES
with open('./receiver/plain_text.txt', 'r') as text:
    message = text.read()
padder = sym_padding.PKCS7(128).padder()
padded_message = padder.update(message.encode()) + padder.finalize()

aes_cipher = Cipher(algorithms.AES(aes_key), modes.ECB(), backend=default_backend())
aes_encryptor = aes_cipher.encryptor()
encrypted_message = aes_encryptor.update(padded_message) + aes_encryptor.finalize()

# Append HMAC for message integrity
hmac_key = os.urandom(32)  # HMAC key for message integrity
hmac_ = HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
hmac_.update(encrypted_message)
digest = hmac_.finalize()

# Save transmitted data to file
with open('./sender/Transmitted_Data', 'wb') as transmitted_data_file:
    transmitted_data_file.write(encrypted_message + rsa_encrypted_aes_key + digest)
