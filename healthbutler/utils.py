import base64
import hmac
import time
import json
import copy

from django.conf import settings


class Jwt():

    @staticmethod
    def encode(self_payload: dict, key: str=settings.SECRET_KEY, exp: int=600) -> str:
        header = {'typ': 'JWT', 'alg': 'HS256'}
        header_json = json.dumps(header, separators=(',', ':'), sort_keys=True)
        header_json_base64 = Jwt.b64encode(header_json.encode())

        self_payload_copy = copy.deepcopy(self_payload)
        self_payload_copy["exp"] = time.time() + exp
        self_payload_copy_json = json.dumps(self_payload_copy, separators=(',', ':'), sort_keys=True)
        self_payload_copy_json_base64 = Jwt.b64encode(self_payload_copy_json.encode())

        # init sign
        hm = hmac.new(key.encode(), header_json_base64 + b'.' + self_payload_copy_json_base64,
                      digestmod="SHA256")
        hm_base64 = Jwt.b64encode(hm.digest())
        return (header_json_base64 + b'.' + self_payload_copy_json_base64 + b'.' + hm_base64).decode()

    @staticmethod
    def b64encode(js):
        return base64.urlsafe_b64encode(js).replace(b"=", b"")

    @staticmethod
    def b64decode(bs):
        rem = len(bs) % 4
        if rem > 0:
            bs += b'=' * (4 - rem)
        return base64.urlsafe_b64decode(bs)

    @staticmethod
    def decode(token_str: str, key: str=settings.SECRET_KEY) -> dict:
        token = token_str.encode()
        header_bs, payload_bs, signature_bs = token.split(b".")
        hm = hmac.new(key.encode(), header_bs + b"." + payload_bs, digestmod="SHA256")
        if signature_bs != Jwt.b64encode(hm.digest()):
            return {}
        payload_js = Jwt.b64decode(payload_bs)
        payload = json.loads(payload_js)
        now = time.time()
        if int(now) > int(payload["exp"]):
            return {}
        return payload
