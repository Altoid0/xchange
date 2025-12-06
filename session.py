class Session:
    def __init__(self, profile_path, shared_path):
        self.profile_path = profile_path
        self.shared_path = shared_path
        self.shared_secret = None

    def set_shared_secret(self, secret: str):
        self.shared_secret = secret

    @property
    def get_profile_path(self) -> str:
        return self.profile_path

    @property
    def get_shared_path(self) -> str:
        return self.shared_path