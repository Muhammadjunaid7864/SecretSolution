from django.core.cache import cache
from .utils import recover_secret
from unsealapi.models import SealStatus
from rest_framework.response import Response
from .security import generte_wraping_key
class SecretProduct:
    @staticmethod
    def store_master_key(master_key):
        cache.set("master_key",master_key,timeout=None)

    @staticmethod
    def get_threshold():
        return SealStatus.objects.first().threshold
    
    @staticmethod
    def get_unseal_key():
        try:
            master_key = cache.get("master_key")
            ferent = generte_wraping_key(master_key)
            unseal_keys = SealStatus.objects.first().unseal_key
            decrypt_unseal_key = [ferent.decrypt(ecr.encode()).decode() for ecr in unseal_keys]
            return decrypt_unseal_key
        except Exception as e:
            return e
    
    @staticmethod
    def submit_key(key, threshold):
        cache_key   = "submit_unseal_key"
        submit_key  = cache.get(cache_key, [])
                
        submit_key.append(key)
        cache.set(cache_key, submit_key, timeout=600)
        if len(submit_key) >= threshold:
            cache.set(cache_key,submit_key,timeout=600)
            return recover_secret(submit_key)
        
        return None
