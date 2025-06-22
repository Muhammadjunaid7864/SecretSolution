from django.core.cache import cache
from unsealapi.models import SealStaus
from core.utils import recover_secret

class ProductState:
    @staticmethod
    def store_master_key(master_key):
        cache.set("master_key", master_key, timeout=None)

    @staticmethod
    def get_threshold():
        return SealStaus.objects.first().threshold

    @staticmethod
    def submit_key(part, threshold):
        cache_key = "submitted_unseal_keys"
        submitted_keys = cache.get(cache_key, [])

        if part in submitted_keys:
            return None

        submitted_keys.append(part)
        cache.set(cache_key, submitted_keys, timeout=600)

        if len(submitted_keys) >= threshold:
            return recover_secret(submitted_keys)
        return None
