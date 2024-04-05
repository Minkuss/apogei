import socket
import hashlib
import threading
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2

params_numbers = dh.DHParameterNumbers(p, g)
parameters = params_numbers.parameters(default_backend())

# Generate private and public keys
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

# Serialize public key
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Send public key to client
def send_public_key(conn):
    conn.sendall(public_key_bytes)

# Perform key exchange and derive shared key
def perform_key_exchange(conn):
    # Receive client's public key
    client_public_key_bytes = conn.recv(1024)
    client_public_key = serialization.load_der_public_key(
        client_public_key_bytes,
        backend=default_backend()
    )

    print("Client public key: " + str(client_public_key))

    # Perform key exchange
    shared_key = private_key.exchange(client_public_key)

    return shared_key

# Generate fixed-length key from shared key
def derive_key(shared_key):
    return hashlib.sha256(shared_key).digest()

# Encrypt message
def encrypt_message(message, key):
    key = derive_key(key)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message) + padder.finalize()
    return encryptor.update(padded_data) + encryptor.finalize()

# Decrypt message
def decrypt_message(encrypted_message, key):
    key = derive_key(key)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = decryptor.update(encrypted_message) + decryptor.finalize()
    return unpadder.update(decrypted_data) + unpadder.finalize()

# Handle client connection
def handle_client(conn, addr):
    print(f"Connected to {addr}")
    send_public_key(conn)
    shared_key = perform_key_exchange(conn)

    # Receive encrypted message
    encrypted_message = conn.recv(1024)
    decrypted_message = decrypt_message(encrypted_message, shared_key)
    print("Received message:", decrypted_message.decode())

    conn.close()

# Main server loop
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
