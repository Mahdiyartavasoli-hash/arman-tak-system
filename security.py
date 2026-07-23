from passlib.context import CryptContext

passcode = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return passcode.hash(password)

def verify_password(pass_log: str, pass_hash: str) -> bool:
    return passcode.verify(pass_log, pass_hash)