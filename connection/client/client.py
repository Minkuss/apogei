import datetime
import socket
import hashlib
import json

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pickle

from cryptography.hazmat.primitives.kdf.hkdf import HKDF

SERVER_HOST = '172.20.10.4'
SERVER_PORT = 30033

p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2

params_numbers = dh.DHParameterNumbers(p, g)
parameters = params_numbers.parameters(default_backend())

# Generate private and public keys
private_key = parameters.generate_private_key()
public_key = private_key.public_key()


def perform_key_exchange(conn: socket) -> bytes:
    """Perform key exchange and derive shared key."""
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

    print('Server public key: ' + str(server_public_key))

    # Perform key exchange
    shared_key = private_key.exchange(server_public_key)

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
    unpadded_data = (unpadder.update(decrypted_data)
                      + unpadder.finalize())

    return unpadded_data


def handle_server(conn: socket) -> None:
    """Handle server connection."""
    shared_key = perform_key_exchange(conn)

    encrypted_message = conn.recv(2 ** 16)
    decrypted_message = decrypt_message(encrypted_message, shared_key).decode(encoding='utf-8')

    data = json.loads(decrypted_message)
    return data


def main() -> None:
    """Lopping client."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        handle_server(client_socket)


if __name__ == '__main__':
    main()
