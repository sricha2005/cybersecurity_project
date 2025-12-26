from cryptography.fernet import Fernet
import subprocess
import logging
from datetime import datetime

# ---------- Logging Setup ----------
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ---------- Key ----------
key = Fernet.generate_key()
cipher = Fernet(key)

# ---------- Storage ----------
store = {}
id_counter = 1
print(" Secure Encryption ")
print("Type 'help' to see commands")

logging.info("started")

while True:
    user_input = input("\n> ").strip()

    # HELP
    if user_input == "help":
        print("\nAvailable Commands:")
        print("encrypt <message>")
        print("decrypt <id>")
        print("list")
        print("exit")

    # EXIT
    elif user_input == "exit":
        print("Exiting ...")
        logging.info(" exited by user")
        break

    # LIST
    elif user_input == "list":
        if not store:
            print("No stored messages")
        else:
            print("Stored IDs:")
            for i in store:
                print(i)

    # ENCRYPT MESSAGE
    elif user_input.startswith("encrypt "):
        message = user_input[8:]

        print("\n[PLAIN MESSAGE]")
        print(message)

        encrypted = cipher.encrypt(message.encode())
        msg_id = f"ID{id_counter}"

        store[msg_id] = encrypted
        id_counter += 1

        print("\n[ENCRYPTED MESSAGE]")
        print(encrypted)
        print("\nStored as:", msg_id)

        logging.info(f"Message encrypted and stored as {msg_id}")

    # DECRYPT + EXECUTE
    elif user_input.startswith("decrypt "):
        msg_id = user_input[8:]

        if msg_id not in store:
            print("Invalid ID")
            logging.warning("Invalid decrypt attempt")
            continue

        encrypted = store[msg_id]
        message = cipher.decrypt(encrypted).decode()

        print("\n[DECRYPTED MESSAGE]")
        print(message)

        logging.info(f"Message {msg_id} decrypted")

        # Try executing as command
        output = subprocess.getoutput(message)

        if output and "not recognized" not in output.lower():
            print("\n[COMMAND OUTPUT]")
            print(output)
            logging.info(f"Command executed: {message}")
        else:
            print("\n[MESSAGE OUTPUT]")
            print(message)
            logging.info("Decrypted message was not a system command")

    else:
        print("Invalid command. Type 'help'")
