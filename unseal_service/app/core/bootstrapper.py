import json
from django.core.cache import cache
from .security import get_warping_key
from .models import Wraping_key
from .seal_state import ProductState
class ProductBootStrapper:

    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)
    
    def decrypt_master_key(self,wrap):
        encrypted_master_key = cache.get('master_key')
        if not encrypted_master_key:
            return None
        
        fernet = get_warping_key(wrap)

        return fernet.decrypt(encrypted_master_key.encode()).decode()
    
    def run(self):
        master_key = self.decrypt_master_key(wrap=Wraping_key)
        if master_key:
            ProductState.stored_master_key(master_key=master_key)
            print("[BOOT] master key restored")
        
        elif self.config["unseal_strategy"] == "manual":
            print("[BOOT] Secret Solution is seal. Please submit unseal key")
        else:
            raise Exception("Secret Solution unseal failed. Check configuration.")
