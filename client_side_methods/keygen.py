import random
import string


def generate_keys(number, size):
    lettersAndNumbers = string.ascii_letters + string.digits
    list_of_numbers = ["".join([random.choice(lettersAndNumbers) for _ in range(size)])for _ in range(number)]
    return list_of_numbers



if __name__=="__main__":
    print(generate_keys(1,24))
    