class S3Storage:
    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name

    def upload(self, key: str, data: str):
        pass
