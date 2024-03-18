import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345


# Perform key exchange and derive shared key
def perform_key_exchange(conn, private_key):
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

    # Send public key to server
    conn.sendall(public_key_bytes)

    # Receive server's public key
    server_public_key_bytes = conn.recv(1024)
    server_public_key = serialization.load_pem_public_key(
        server_public_key_bytes,
        backend=default_backend()
    )

    # Perform key exchange
    shared_key = private_key.exchange(server_public_key)

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


# Handle server connection
def handle_server(conn, private_key):
    shared_key = perform_key_exchange(conn, private_key)

    # Example data exchange
    send_encrypted_data(conn, shared_key, b"Hello from client!")
    decrypted_data = receive_encrypted_data(conn, shared_key)
    print("Received from server:", decrypted_data.decode())


# Main client loop
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())
        private_key = parameters.generate_private_key()
        handle_server(client_socket, private_key)


if __name__ == "__main__":
    main()
