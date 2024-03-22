import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding
import threading

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


# Perform key exchange and derive shared key
def perform_key_exchange(conn):
    # Serialize public key
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Send public key to server
    conn.sendall(public_key_bytes)

    # Receive server's public key
    server_public_key_bytes = conn.recv(1024)
    server_public_key = serialization.load_der_public_key(
        server_public_key_bytes,
        backend=default_backend()
    )

    print("Server public key: " + str(server_public_key))

    # Perform key exchange
    shared_key = private_key.exchange(server_public_key)

    return shared_key


# Encrypt and send data
def send_encrypted_data(conn, shared_key, data):
    # Разбиение общего ключа на составляющие: IV, ключ шифрования и ключ аутентификации
    iv = shared_key[:16]
    key = shared_key[16:]

    # Инициализация объекта шифра с использованием алгоритма AES и режима CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Получение объекта шифра для шифрования данных
    encryptor = cipher.encryptor()

    # Дополнение данных до кратного размера блока
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Шифрование дополненных данных и отправка зашифрованных данных через соединение
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    conn.sendall(iv + encrypted_data)


# Decrypt received data
def receive_encrypted_data(conn, shared_key):
    cipher = shared_key[:16]
    iv = shared_key[16:32]
    key = shared_key[32:]
    encrypted_data = conn.recv(1024)
    return cipher.decrypt(encrypted_data)


# Handle server connection
def handle_server(conn):
    shared_key = perform_key_exchange(conn)

    # Example data exchange
    send_encrypted_data(conn, shared_key, b"Hello from client!")
    decrypted_data = receive_encrypted_data(conn, shared_key)
    print("Received from server:", decrypted_data.decode())


# Main client loop
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        handle_server(client_socket)


if __name__ == "__main__":
    main()
