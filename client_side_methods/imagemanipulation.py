import base64
from typing import TypeVar
from base64 import b64encode

from encryption import TripleDes_Encryption24, TripleDes_Decryption24
from keygen import generate_keys

A = TypeVar('A', str, bytes)


def Image_Loader(path: str) -> A:
    with open(f'{path}', 'rb') as ImageFile:
        string = base64.b64encode(bytes(ImageFile.read()))
    return string


def Image_Encryption(path: str, key: A) -> A:
    data = Image_Loader(path)
    enc = TripleDes_Encryption24(data, key)
    return enc


def Image_Decryption(encrypted_image: A, key: A, path: str, id: A):
    data = TripleDes_Decryption24(encrypted_image, key)
    with open(path + f"/{id}.png", 'wb') as fh:
        fh.write(base64.decodebytes(data))
    return data


if __name__ == "__main__":
    import json
    with open("t.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
    print(type(str))
    k = generate_keys(24)
    enc = Image_Encryption("t.jpg", k)
    print(type(enc))
    t = {"test": enc}
    t2 = {"test": enc.hex()}
    json.dumps(t2)

    t3 = enc.hex()
    print(enc == bytes.fromhex(t3)) # TRUEEEEEEEEEEEEEEEEEEEEEEEEEEE

    denc = Image_Decryption(bytes.fromhex(t3), k,"","test")
    print(type(denc))
    fh = open("imageToSave.png", "wb", 123)
    fh.write(base64.decodebytes(denc))
    fh.close()
