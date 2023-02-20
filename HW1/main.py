import sys

def caeser_cipher(k, m):
    ans = ""
    m = m.upper()

    # turns offset into a number
    if type(k) is str:
        k = ord(k.upper()) - ord("A")

    for char in m:
        ans += chr((ord(char) - ord("A") + k) % 26 + ord("A"))

    return ans

def ceaser_decipher(k, m):
    ans = ""
    m = m.upper()

    # turns offset into a number
    if type(k) is str:
        k = ord(k.upper()) - ord("A")

    for char in m:
        ans += chr((ord(char) - ord("A") - k) % 26 + ord("A"))

    return ans

def vigenere_cipher(key, message):
    ans = ""
    message = message.strip().upper()
    key_counter = 0

    for char in message:
        key_counter = key_counter % len(key)
        if char != ' ':
            ans += caeser_cipher(key[key_counter], char)
        else:
            ans += ' '
        key_counter += 1

    return ans

def vigenere_decipher(key, message):
    ans = ""
    message = message.strip().upper()
    key_counter = 0

    for char in message:
        key_counter = key_counter % len(key)
        if char != ' ':
            ans += ceaser_decipher(key[key_counter], char)
        else:
            ans += ' '
        key_counter += 1

    return ans

def menu():
    while(True):
        print("Type 1 to encrypt or 2 to decrypt")
        print("Enter anything else to exit")

        num = input("Enter Selection: ")

        if num == "1":
            key = input("Enter key: ")
            message = input("Enter message to encrypt: ")
            v_ciph = vigenere_cipher(key, message)
            print(f"Vigenere Cipher: {message} + key({key}) -> {v_ciph}")
        elif num == "2":
            key = input("Enter key: ")
            message = input("Enter message to decrypt: ")
            v_deciph = vigenere_decipher(key, message)
            print(f"Vigenere Decipher: {message} + key({key}) -> {v_deciph}")
        else:
            sys.exit()

if __name__ == '__main__':
    '''
    -- ==== TEST CASES === --
    
    c_ciph = caeser_cipher(9, "VELVET") # VELVET -> ENUENC
    print(f"Caeser Cipher: {c_ciph}")

    c_deciph = ceaser_decipher(9, c_ciph) # ENUENC -> VELVET
    print(f"Caeser Decipher: {c_deciph}")

    v_ciph = vigenere_cipher("VIG", "THE BOY HAS THE TOY") # THEBOYHASTHETOY -> OPKWWECIYOPKOWE
    print(f"Vigenere Cipher: {v_ciph}")

    v_deciph = vigenere_decipher("VIG", v_ciph)
    print(f"Vigenere Decipher: {v_deciph}")'''

    menu()