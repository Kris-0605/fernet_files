from cryptography.fernet import Fernet
from base64 import urlsafe_b64decode, urlsafe_b64encode
import os
from typing import Union, Optional, Type
from io import BytesIO, RawIOBase, BufferedIOBase
from types import TracebackType

_magic_dict = {}
_fernet_for_magic = Fernet(Fernet.generate_key())

def _add_magic(size: int) -> int:
    pass
    
class FernetFile:
    def __init__(self, key: bytes, file: Union[str, RawIOBase, BufferedIOBase], chunksize: int = 65536) -> None:
        self.file = file

    def seek(self, *args, whence=os.SEEK_SET):
        if type(self.file) == BytesIO:
            return self.file.seek(args[0])
        if len(args) == 2:
            whence = args[1]
        return self.file.seek(args[0], whence)

    def read(self, *args, **kwargs):
        return self.file.read(*args, **kwargs)
    
    def write(self, *args, **kwargs):
        return self.file.write(*args, **kwargs)
    
    def close(self) -> None:
        self.file.close()

    generate_key = Fernet.generate_key

    def __enter__(self) -> "FernetFile":
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], exc_traceback: Optional[TracebackType]) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()