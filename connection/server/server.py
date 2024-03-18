import socket
import threading
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Generate DH parameters
parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())

# Generate private and public keys
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

# Serialize public key
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


# Send public key to client
def send_public_key(conn):
    conn.sendall(public_key_bytes)


# Perform key exchange and derive shared key
def perform_key_exchange(conn, private_key):
    # Receive client's public key
    client_public_key_bytes = conn.recv(1024)
    client_public_key = serialization.load_pem_public_key(
        client_public_key_bytes,
        backend=default_backend()
    )

    # Perform key exchange
    shared_key = private_key.exchange(client_public_key)

    return shared_key


# Encrypt and send data
def send_encrypted_data(conn, shared_key, data):
    cipher = shared_key[:16]
    iv = shared_key[16:32]
    key = shared_key[32:]
    conn.sendall(iv + cipher.encrypt(data))


# Decrypt received data
def receive_encrypted_data(conn, shared_key):
    cipher = shared_key[:16]
    iv = shared_key[16:32]
    key = shared_key[32:]
    encrypted_data = conn.recv(1024)
    return cipher.decrypt(encrypted_data)


# Handle client connection
def handle_client(conn, addr):
    print(f"Connected to {addr}")

    # Generate DH parameters and private key for this connection
    parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())
    private_key = parameters.generate_private_key()

    send_public_key(conn, private_key)
    shared_key = perform_key_exchange(conn, private_key)

    # Example data exchange
    send_encrypted_data(conn, shared_key, b"Hello from server!")
    decrypted_data = receive_encrypted_data(conn, shared_key)
    print("Received from client:", decrypted_data.decode())

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
