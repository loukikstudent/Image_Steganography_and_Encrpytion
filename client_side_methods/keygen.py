import random
import string


def generate_keys(size):
    lettersAndNumbers = string.ascii_letters + string.digits
    return "".join([random.choice(lettersAndNumbers) for _ in range(size)])


if __name__=="__main__":
    print(generate_keys(1,24))