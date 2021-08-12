import hashlib


class EncryptionService:
    @staticmethod
    def sha1_encrypt(value: str) -> str:
        return hashlib.sha1(value.encode('utf-8')).hexdigest()
