import bcrypt
import base64

class Encryption:
    def bcrypt_hash(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return base64.b64encode(hashed_password).decode('utf-8')

    def bcrypt_verify(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
