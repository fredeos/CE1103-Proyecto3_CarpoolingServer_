import bcrypt
class Encryption:
    @classmethod
    def encode_password(cls,password:str):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password
    @classmethod
    def verify_password(cls,check_password:str, encoded_password):
        return bcrypt.checkpw(check_password.encode("utf-8"), encoded_password)