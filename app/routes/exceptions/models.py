from typing import Optional


class CustomException(Exception):
    def __init__(self, status_code: Optional[int] = None, **kwargs):
        self.status_code = status_code
        self.kwargs = kwargs
