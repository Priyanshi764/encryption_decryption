from cryptography.fernet import Fernet
import os

# ---------- KEY MANAGEMENT ----------
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("🔑 Key generated and saved as 'key.key'")

def load_key():
    if not os.path.exists("key.key"):
        print("❌ Key file not found. Please generate a key first.")
        return None
    with open("key.key", "rb") as key_file:
        return key_file.read()

def load_key_with_password():
    password = input("🔑 Enter password to access the key: ")
    if password != "pp":  # Change this to your own secure password
        print("❌ Incorrect password. Access denied.")
        return None
    return load_key()

# ---------- ENCRYPTION ----------
def encrypt_file(filename):
    key = load_key_with_password()
    if key is None:
        return
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(filename, "wb") as file:
        file.write(encrypted)

    print(f"✅ File '{filename}' encrypted.")

def encrypt_file_with_new_name(filename):
    key = load_key_with_password()
    if key is None:
        return
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    new_filename = filename + ".enc"
    with open(new_filename, "wb") as file:
        file.write(encrypted)

    print(f"✅ File encrypted and saved as '{new_filename}'.")

def encrypt_all_in_folder(folder_path):
    key = load_key_with_password()
    if key is None:
        return
    fernet = Fernet(key)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                original = file.read()
            encrypted = fernet.encrypt(original)
            with open(file_path, "wb") as file:
                file.write(encrypted)
            print(f"✅ Encrypted: {filename}")

# ---------- DECRYPTION ----------
def decrypt_file(filename):
    key = load_key_with_password()
    if key is None:
        return
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        encrypted = file.read()

    try:
        decrypted = fernet.decrypt(encrypted)
    except:
        print("❌ Decryption failed. Is the key correct?")
        return

    with open(filename, "wb") as file:
        file.write(decrypted)

    print(f"✅ File '{filename}' decrypted.")

# ---------- MAIN MENU ----------
def main():
    while True:
        print("\n=== ENCRYPTION CONSOLE APP ===")
        print("1. Generate Key")
        print("2. Encrypt File")
        print("3. Decrypt File")
        print("4. Exit")
        print("5. Encrypt All Files in Folder")
        print("6. Encrypt File and Save with New Name")

        choice = input("Choose an option (1–6): ")

        if choice == "1":
            generate_key()
        elif choice == "2":
            filename = input("Enter file name to encrypt (e.g., sample.txt): ")
            encrypt_file(filename)
        elif choice == "3":
            filename = input("Enter file name to decrypt: ")
            decrypt_file(filename)
        elif choice == "4":
            print("👋 Exiting program.")
            break
        elif choice == "5":
            folder = input("Enter folder path: ")
            encrypt_all_in_folder(folder)
        elif choice == "6":
            filename = input("Enter file name to encrypt and save with new name: ")
            encrypt_file_with_new_name(filename)
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
