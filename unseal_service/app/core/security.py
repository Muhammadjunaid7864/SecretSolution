from cryptography.fernet import Fernet

def generte_wraping_key(wrap):
    return Fernet(wrap)