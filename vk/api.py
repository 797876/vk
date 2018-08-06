import logging

from vk.utils import stringify_values

logger = logging.getLogger('vk')


class API:
    def __init__(self, session, method_common_params):
        self._session = session
        self._method_common_params = method_common_params

    def __call__(self, method):
        return APIMethod(self._session, method, self._method_common_params)

    __getattr__ = __call__


class APIMethod:
    def __init__(self, session, method, method_common_params):
        self._session = session
        self._method = method
        self._method_common_params = method_common_params

    def __getattr__(self, method):
        return self.__class__(self._session, self._method + '.' + method, self._method_common_params)

    def __call__(self, **method_params):
        request_method_params = self._method_common_params.copy()
        request_method_params.update(stringify_values(method_params))

        return self._session.send(APIRequest(self._method, request_method_params))


class APIRequest:
    def __init__(self, method, method_params):
        self.method = method
        self.method_params = method_params
