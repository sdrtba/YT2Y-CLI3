from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import os

def derive_key(user_key: str) -> bytes:
    """Генерирует 32-байтовый ключ из строки, введённой пользователем."""
    return hashlib.sha256(user_key.encode()).digest()

def encrypt(text: str, user_key: str) -> bytes:
    """Шифрует текст с использованием AES-256 в режиме CBC."""
    key = derive_key(user_key)  # Получаем ключ из строки
    iv = os.urandom(16)  # Генерируем случайный IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Выравниваем текст до 16 байтов (блок AES)
    padded_text = text + (16 - len(text) % 16) * " "
    ciphertext = encryptor.update(padded_text.encode()) + encryptor.finalize()

    return iv + ciphertext  # Возвращаем IV + зашифрованные данные

def decrypt(encrypted_data: bytes, user_key: str) -> str:
    """Дешифрует данные, зашифрованные функцией encrypt."""
    key = derive_key(user_key)
    iv, ciphertext = encrypted_data[:16], encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_padded.decode().strip()  # Убираем пробелы после расшифровки

# Пример использования
user_key = input("Введите ключ: ")
message = "Hello, world!"

encrypted = encrypt(message, user_key)
print("Зашифрованные данные:", encrypted.hex())
print("Зашифрованные данные:", encrypted)

decrypted = decrypt(encrypted, user_key)
print("Расшифрованное сообщение:", decrypted)
