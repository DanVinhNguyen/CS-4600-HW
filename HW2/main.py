
# function to turn a string hex into actual hexadecimal
def to_hex(hex_string):
    return int(hex_string, 16)


# Task 1: Deriving the Private Key'
# Given:
p = 0xF7E75FDC469067FFDC4E847C51F452DF
q = 0xE85CED54AF57E53E092113E62F436F4F
e = 0x0D88C3

# d = e^(-1) mod (p - 1)(q - 1)
d = pow(e, -1, (p - 1)*(q - 1))
print("Task 1: ")
print(f"Private key \"d\" = {hex(d)}\n")


# Task 2: Encrypting a Message
# Provided information:
n_task2 = 0xDCBFFE3E51F62E09CE7032E2677A78946A849DC4CDDE3A4D0CB81629242FB1A5
e_task2 = 0x010001
m_task2 = "A top secret!"
d_task2 = 0x74D806F9F3A62BAE331FFE3F0A68AFE35B3D2E4794148AACBC26AA381CD7D30D

hex_message_task2 = to_hex(m_task2.encode("utf-8").hex())
#print(f"hex_message_task2: {hex(hex_message_task2)}")

# M = m^(e) mod N
#encoded_message_task2 = (hex_message_task2 ^ e_task2) % n_task2
encoded_message_task2 = pow(hex_message_task2, e_task2, n_task2)

print("Task 2: ")
print(f"Encoded message: {hex(encoded_message_task2)}\n")


# Task 3: Decrypting a Message
# Given:
encrypted_message = 0x8C0F971DF2F3672B28811407E2DABBE1DA0FEBBBDFC7DCB67396567EA1E2493F
#d_task2 = 0x74D806F9F3A62BAE331FFE3F0A68AFE35B3D2E4794148AACBC26AA381CD7D30D
#n_task2 = 0xDCBFFE3E51F62E09CE7032E2677A78946A849DC4CDDE3A4D0CB81629242FB1A5

# M = e^d mod n
unencrypted_message_hex = str(hex(pow(encrypted_message, d_task2, n_task2)))

# Convert to string
unencrypted_message = bytes.fromhex(unencrypted_message_hex.replace('0x', '')).decode('utf-8')

print("Task 3: ")
print(f"Unencrypted message: {unencrypted_message}\n")


# Task 4: Signing a Message
# Given:
m_task4 = "I owe you $2000."
m_task4_2 = "I owe you $3000."
#d_task2 = 0x74D806F9F3A62BAE331FFE3F0A68AFE35B3D2E4794148AACBC26AA381CD7D30D
#n_task2 = 0xDCBFFE3E51F62E09CE7032E2677A78946A849DC4CDDE3A4D0CB81629242FB1A5

# convert message to hex
hex_message_task5 = to_hex(m_task4.encode("utf-8").hex())
hex_message_task5_2 = to_hex(m_task4_2.encode("utf-8").hex())

# sig = m^(d) mod n
# generate the signature
sig_task4 = pow(hex_message_task5, d_task2, n_task2)
sig_task4_2 = pow(hex_message_task5_2, d_task2, n_task2)
print("Task 4: ")
print(f"Signature: {hex(sig_task4)}")
print("Augmented original message to: \"I owe you $3000.\"")
print(f"Signature: {hex(sig_task4_2)}\n")


#  Task 5: Verifying a Signature
# Given:
m_task5 = "Launch a missile."
S_task5 = 0x643D6F34902D9C7EC90CB0B2BCA36C47FA37165C0005CAB026C0542CBDB6802F
e_task5 = 0x010001 #(this hex value equals to decimal 65537)
n_task5 = 0xAE1CD4DC432798D933779FBD46C6E1247F0CF1233595113AA51B450F18116115

# convert the plaintext into hex to check against later
m_task5_hex = to_hex(m_task5.encode("utf-8").hex())

#M = S^e % n
# generate the signature with the public information
sig_task5 = pow(S_task5, e_task5, n_task5)

# check if the message is the same as both
print("Task 5: ")
print(f"Plain text: {hex(m_task5_hex)}")
print(f"Signature:  {hex(sig_task5)}")
if sig_task5 == m_task5_hex:
    print("The signature IS verified.")
else:
    print("Signature NOT verified.")
