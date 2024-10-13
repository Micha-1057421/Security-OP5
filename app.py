from flask import Flask, render_template, request, flash
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message.decode()  

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    try:
        decrypted_message = f.decrypt(encrypted_message.encode()).decode()
        return decrypted_message
    except Exception as e:
        return str(e) 

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        action = request.form.get("action")

        if action == 'encrypt':
            output_text = encrypt_message(user_input)
        elif action == 'decrypt':
            output_text = decrypt_message(user_input)

    return render_template("index.html", output_text=output_text)

if __name__ == "__main__":
    generate_key() 
    app.run(debug=True)
