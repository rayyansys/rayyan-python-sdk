from typing import Protocol


class RequestInterface(Protocol):
    def request_handler(self, *args, **kwargs): ...

class RayyanProtocol(Protocol):
    request: RequestInterface
