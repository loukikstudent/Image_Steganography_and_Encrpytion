from typing import List, TypeVar

from passlib.hash import pbkdf2_sha256
from pyDes import *

A = TypeVar('A', str, bytes)


def TripleDes_Encryption24(data: A, key: A) -> A:
    """

    :type key: object
    :type data: object
    """
    encrypted_data = triple_des(key).encrypt(data, padmode=PAD_PKCS5)
    return encrypted_data


def Key_Encryption(keys: List[A]) -> List[A]:
    """

    :type keys: object
    """
    return [pbkdf2_sha256.using(salt_size=128).hash(i) for i in keys]


def Key_Verification(keys: List[A], encrypted_keys: List[A]) -> bool:
    """

    :param keys:
    :type encrypted_keys: object
    """
    if all([pbkdf2_sha256.identify(i) for i in encrypted_keys]):
        return all([pbkdf2_sha256.verify(i, j) for i in keys for j in encrypted_keys])
    return False


if __name__ == "__main__":
    # temp import
    # noinspection PyUnresolvedReferences
    from keygen import generate_keys

    print(TripleDes_Encryption24("totototo", generate_keys(1, 24)[0]))
    keys = generate_keys(1, 128)
    enc2 = ["helluu"]
    enc = Key_Encryption(keys)
    print(Key_Verification(keys, enc))
    # print(Key_Verification(keys,enc2))
