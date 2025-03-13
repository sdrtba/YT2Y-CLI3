from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from json import loads
import requests
import hashlib
import os
import sys

TOKEN = None
KIND = None
SONGS_DIR = 'output'
TOKEN_FILE = 'etc/token.sec'
KIND_FILE = 'etc/kind'

def exist_upload() -> None:
    t = ""
    with open('etc/1.txt', 'r', encoding='utf-8') as file:
        t = file.read()


    try:
        contents = os.listdir(SONGS_DIR)
        for content in contents:
            if content in t:
                continue
            else:
                print(''.join(content.split('.m4a')[0:-1]))
                upload(''.join(content.split('.m4a')[0:-1]))
                with open('etc/1.txt', 'a', encoding='utf-8') as file:
                    file.write(content+'\n')
    except FileNotFoundError:
        print('\033[91mПапка output не найдена\033[0m')
    except PermissionError:
        print('\033[91mНет доступа к папке output\033[0m')

def check_kind():
    if not os.path.exists(KIND_FILE):
        print('\033[91mKIND не найден\033[0m')
        set_kind()

def check_token():
    if not os.path.exists(TOKEN_FILE):
        print('\033[91mTOKEN не найден\033[0m')
        set_token()

def set_kind() -> None:
    global KIND

    if not os.path.exists(KIND_FILE):
        KIND = input('Kind: ') or '3'
        with open(KIND_FILE, 'w') as file:
            file.write(KIND)
        return

    with open(KIND_FILE, 'r') as file:
        KIND = file.read()


def encrypt(text: str) -> bytes:
    """Шифрует текст с использованием AES-256 в режиме CBC."""
    key = hashlib.sha256(input('Key: ').encode()).digest()  # Получаем ключ из строки
    iv = os.urandom(16)  # Генерируем случайный IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Выравниваем текст до 16 байтов (блок AES) с использованием PKCS7
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_text = padder.update(text.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()

    return iv + ciphertext  # Возвращаем IV + зашифрованные данные

def decrypt(encrypted_data: bytes) -> str:
    """Дешифрует данные, зашифрованные функцией encrypt."""
    key = hashlib.sha256(input('Key: ').encode()).digest()
    iv, ciphertext = encrypted_data[:16], encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted_data.decode()  # Возвращаем расшифрованные данные

def set_token() -> None:
    global TOKEN
    if not os.path.exists(TOKEN_FILE):
        TOKEN = input('Enter token: ')
        with open(TOKEN_FILE, 'wb') as file:
            file.write(encrypt(TOKEN))
        return

    with open(TOKEN_FILE, 'rb') as file:
        TOKEN = decrypt(file.read())

def get_target(filename: str) -> str:
    headers = {'Authorization': f'Bearer {TOKEN}'}
    url = f'https://music.yandex.ru/handlers/ugc-upload.jsx?kind={KIND}&filename={filename}'
    text = requests.get(url, headers=headers).text
    try:
        target = text[text.find('post-target') + 14:text.find('ugc-track-id') - 3]
        return target
    except:
        print(text, target)
        sys.exit(0)

def upload(filename: str) -> str:
    if KIND is None:
        set_kind()
    if TOKEN is None:
        set_token()

    target = get_target(filename)

    with open(f'{SONGS_DIR}\\{filename}.m4a', 'rb') as f:
        files = {'file': ('filename', f, 'audio/mp3')}
        r = requests.post(url=target, files=files)
    return loads(r.text)

if __name__ == '__main__':
    upload('123')
