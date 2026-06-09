from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open("encryption_key.txt", "wb") as key_file:
    key_file.write(key)

print("Fernet key generated and saved to encryption_key.txt")