from cryptography.fernet import Fernet

def get_wrapping_key(wrap):
    try:
        return Fernet(wrap.wrapping_key.encode())
    except Exception as e:
        raise ValueError("Invalid wrapping key: must be 32 url-safe base64-encoded bytes") from e
