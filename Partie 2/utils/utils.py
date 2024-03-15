import random
from string import ascii_uppercase

def room_code_generator(len_code, rooms):
    while True:
        code = ""
        for i in range(len_code):
            code += random.choice(ascii_uppercase)
            
        if code not in rooms:
            break
    return code