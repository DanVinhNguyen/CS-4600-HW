import os
import base64
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.backends import default_backend

# Receiver's RSA key generation
receiver_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

receiver_public_key = receiver_private_key.public_key()

# Save receiver's RSA private key to a file
with open('./receiver/private_key.pem', 'wb') as private_key_file:
    private_key_file.write(
        receiver_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Save receiver's RSA public key to a file
with open('./receiver/public_key.pem', 'wb') as public_key_file:
    public_key_file.write(
        receiver_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

# Load transmitted data from file
with open('./sender/Transmitted_Data', 'rb') as transmitted_data_file:
    transmitted_data = transmitted_data_file.read()

# Separate encrypted message, encrypted AES key, and HMAC digest
encrypted_message = transmitted_data[:256]
encrypted_aes_key = transmitted_data[256:512]
digest = transmitted_data[512:]

# Decrypt AES key using receiver's RSA private key
decrypted_aes_key = receiver_private_key.decrypt(
    encrypted_aes_key,
    asymmetric_padding.OAEP(
        mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Decrypt message using AES
aes_cipher = Cipher(algorithms.AES(decrypted_aes_key), modes.ECB(), backend=default_backend())
aes_decryptor = aes_cipher.decryptor()
decrypted_message = aes_decryptor.update(encrypted_message) + aes_decryptor.finalize()

# Verify HMAC for message integrity
hmac_key = HMAC(decrypted_aes_key, hashes.SHA256(), backend=default_backend())
hmac_key.update(encrypted_message)

try:
    hmac_key.verify(digest)
    print("Message integrity verified.")
    print("Decrypted message:", decrypted_message.decode())

    with open("Message_output.txt", "a") as file:
        file.write(decrypted_message.decode())

except InvalidSignature:
    print("Message integrity verification failed.")
