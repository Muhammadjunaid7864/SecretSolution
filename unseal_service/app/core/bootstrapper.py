from django.core.cache import cache


class BootstrapperToken:
    def __init__(self):
        self.master_key = cache.get("master_key")
    

