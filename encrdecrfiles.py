import hashlib
import getpass
from random import choice


START_MESSAGE = '------------START OF PYENCRYPT/DECRYPT PROGRAM DATA-----------'
END_MESSAGE =   '------------ END OF PYENCRYPT/DECRYPT PROGRAM DATA -----------'

class InputPasswordNotCorrect(Exception):
    pass

def is_even(number):
    return number % 2 == 0

def get_even_letters(message):
    even_letters = []
    for counter in range(0, len(message)):
        if is_even(counter):
            even_letters.append(message[counter])
    return even_letters

def get_odd_letters(message):
    odd_letters = []
    for counter in range(0, len(message)):
        if not is_even(counter):
            odd_letters.append(message[counter])
    return odd_letters

def swap_letters(message):
    letter_list = []
    if not is_even(len(message)):
        message = message = 'x'
    even_letters = get_even_letters(message)
    odd_letters = get_odd_letters(message)
    for counter in range(0, int(len(message)/2)):
        letter_list.append(odd_letters[counter])
        letter_list.append(even_letters[counter])
    new_message = ''.join(letter_list)
    return new_message

def encrypt(message):
    le_fa_message = add_fake(message)
    swapped_message = swap_letters(le_fa_message)
    encrypted_message = ''.join(reversed(swapped_message))
    return encrypted_message

def decrypt(message):
    unreversed_message = ''.join(reversed(message))
    swapped_message = swap_letters(unreversed_message)
    even_message = get_even_letters(swapped_message)
    decrypted_message = ''.join(even_message)
    return decrypted_message


def add_fake(message):
    encrypted_list = []
    fake_letters = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'z', 'c', 'v', 'b', \
                    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ',
                    '!', '@', '#','$','%', '^', '&','*', '(', ')', '.', ',',
                    '/']
    for counter in range(0, len(message)):
        encrypted_list.append(message[counter])
        encrypted_list.append(choice(fake_letters))
    fake_l_message = ''.join (encrypted_list)
    return fake_l_message

def gen_passwd(password):
    passwd = hashlib.sha512(password.encode()).hexdigest()
    passwd = str(passwd)
    return passwd

def encrypt_file(filename, hashfilename, passwd):
    with open(filename, 'r') as ftr:
        ftr_contents = ftr.read()
        ftr.close()
    with open(hashfilename, 'w') as hf:
        encr_contents = encrypt(ftr_contents)
        f_passwd = encrypt(passwd)
        f_passwd = f_passwd + '\{[|]}/'
        hf.write(START_MESSAGE+'\n')
        hf.write(f_passwd)
        hf.write(encr_contents)
        hf.write('\n'+END_MESSAGE+'\n')
        hf.close()
    print('Complete!')

def decrypt_file(hashfilename, outfilename, passwd):
    with open(hashfilename, 'r') as hftr:
        w_encr_contents = hftr.read()
        w_encr_contents = w_encr_contents.strip(START_MESSAGE+'\n')
        w_encr_contents = w_encr_contents.strip('\n'+END_MESSAGE+'\n')
        f_passwd, encr_contents  = w_encr_contents.split('\{[|]}/', maxsplit=1)
        f_passwd = decrypt(f_passwd)
        if passwd != f_passwd:
            raise InputPasswordNotCorrect('The inputted password is not correct.')
        else:
            print('Password Correct')
        hftr.close()
    with open(outfilename, 'w') as out:
        contents = decrypt(encr_contents)
        out.write(contents)
        out.close()
    print('Complete!')

print('Welcome to the Password-Protected File Encrypter/Decrypter Program!')
task = input('Do you want to [E]ncrypt or [D]ecrypt or [EX]it: ')

if task.lower() == 'encrypt' or task.lower() == 'e':
    fn = input('File to encrypt: ')
    hashfn = input('File to put encrypted contents in: ')
    passw = getpass.getpass('Password for the file with the encrypted contents: ')
    passw = gen_passwd(passw)
    encrypt_file(fn, hashfn, passw)
elif task.lower() == 'decrypt' or task.lower() == 'd':
    hashfn = input('File to decrypt: ')
    outfn = input('File to put decrypted contents in: ')
    fpassw = getpass.getpass('Password for the file to decrypt: ')
    fpassw = gen_passwd(fpassw)
    decrypt_file(hashfn, outfn, fpassw)
elif task.lower() == 'exit' or task.lower() == 'ex':
    print('Exiting...')
else:
    print('Unknown Task')

