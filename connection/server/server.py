import socket
import sys
import threading
import json
import time

from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from database.Database import Database
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


SERVER_HOST = ''
if int(input('Press 1 to enter 192.168.0.16\nPress 2 to enter your ip\nEnter your choice: ')) == 1:
    SERVER_HOST = '192.168.0.16'
else:
    SERVER_HOST = input('Enter your ip: ')

SERVER_PORT = int(input('Enter port: '))

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


def send_public_key(conn: socket) -> None:
    """Send public key to client."""
    conn.sendall(public_key_bytes)


#
def perform_key_exchange(conn: socket) -> bytes:
    """Perform key exchange and derive shared key."""
    # Receive client's public key
    client_public_key_bytes = conn.recv(1024)
    client_public_key = serialization.load_der_public_key(
        client_public_key_bytes,
        backend=default_backend()
    )

    print('Client public key: ' + str(client_public_key))

    # Perform key exchange
    shared_key = private_key.exchange(client_public_key)

    return shared_key


def derive_key(shared_key: bytes) -> bytes:
    """Derive key."""
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_key)
    return derived_key


def encrypt_message(message: bytes, key: bytes) -> bytes:
    """Encrypt message."""
    key = derive_key(key)
    iv = b'\x00' * 16  # Initialization vector, should be random for real-world usage
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Применяем дополнение PKCS7
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message) + padder.finalize()

    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return iv + ciphertext


def decrypt_message(encrypted_message: bytes, key: bytes) -> bytes:
    """Decrypt message."""
    key = derive_key(key)
    iv = encrypted_message[:16]  # Получаем IV из зашифрованного сообщения
    ciphertext = encrypted_message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Удаляем дополнение
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data


def handle_client(conn: socket, addr: any, data: list) -> None:
    """Handle client connection."""

    def chunker(seq, size):
        """chunk a sequence by size."""
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    print(f'Connected to {addr}')
    send_public_key(conn)
    shared_key = perform_key_exchange(conn)

    CHUNK_SIZE = 12
    data = chunker(data, CHUNK_SIZE)

    for chunk in data:
        encrypted_message = encrypt_message((json.dumps(chunk, ensure_ascii=False)).encode(), shared_key)

        conn.sendall(sys.getsizeof(encrypted_message).to_bytes(4, signed=True))

        conn.sendall(encrypted_message)
        time.sleep(0.3)

    end = 0
    conn.sendall(end.to_bytes(4, signed=True))
    conn.close()


def main(db: Database) -> None:
    """Lopping server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        print(f'Server listening on {SERVER_HOST}:{SERVER_PORT}')

        while True:
            conn, addr = server_socket.accept()
            result = db.select_all_as_dict()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, result))
            client_thread.start()
            print('Data sent')


if __name__ == '__main__':
    main(Database())
