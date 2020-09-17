from .utils import _read_file

class KeysInfo:
    def __init__(
        self,
        key_file,
        cert_file,
        verify_cert_file=None,
        password_file=None,
    ):
        self.key_data = _read_file(key_file)
        self.cert_data = _read_file(cert_file)
        self.verify_cert_data = (
            _read_file(verify_cert_file)
            if verify_cert_file
            else self.cert_data
        )
        self.password = _read_file(password_file, "r") if password_file else None