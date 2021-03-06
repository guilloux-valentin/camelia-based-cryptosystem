import os
import prompt
import secrets
import string
import codecs
import sys
import base64
import random
import binascii
import math
import hashlib
import platform

print(platform.architecture())

from gmpy2 import xmpz, to_binary, invert, powmod, is_prime
from hashlib import sha1

from random import randrange

MASK8   = 0xff
MASK32  = 0xffffffff
MASK64  = 0xffffffffffffffff
MASK128 = 0xffffffffffffffffffffffffffffffff

Sigma1 = 0xA09E667F3BCC908B
Sigma2 = 0xB67AE8584CAA73B2
Sigma3 = 0xC6EF372FE94F82BE
Sigma4 = 0x54FF53A5F1D36F1C
Sigma5 = 0x10E527FADE682D1D
Sigma6 = 0xB05688C2B3E6C1FD

def SBOX2(x):
        return(rotate_left(SBOX1(x),1,8))

def SBOX3(x):
        return rotate_left(SBOX1(x),7,8)

def SBOX4(x):
        return SBOX1(rotate_left(x,1,8))

def SBOX1(x):
    line = "0x{:02x}".format(x)[2]
    column = "0x{:02x}".format(x)[3]
    dict =     {'0' : {     '0': 112,   '1' : 130,  '2' : 44,   '3' : 236,  '4' : 179,  '5' : 39,   '6' : 192,  '7':229,    '8':228,    '9':133,   'a':87,     'b':53,     'c':234,    'd': 12,    'e':174,    'f':65},
                '1' : {     '0': 35,    '1' : 239,  '2' : 107,  '3' : 147,  '4' : 69,   '5' : 25,   '6' : 165,  '7':33,     '8':237,    '9':14,    'a':79,     'b':78,     'c':29,     'd': 101,   'e':146,    'f':189},
                '2' : {     '0': 134,   '1' : 184,  '2' : 175,  '3' : 143,  '4' : 124,  '5' : 235,  '6' : 31,   '7':206,    '8':62,     '9':48,    'a':220,    'b':95,     'c':94,     'd': 197,   'e':11,     'f':26},
                '3' : {     '0': 166,   '1' : 225,  '2' : 57,   '3' : 202,  '4' :213,   '5' : 71,   '6' : 93,   '7':61,     '8':217,    '9':1,     'a':90,     'b':214,    'c':81,     'd': 86,    'e':108,    'f':77},
                '4' : {     '0': 139,   '1' : 13,   '2' : 154,  '3' : 102,  '4' :251,   '5' : 204,  '6' : 176,  '7':45,     '8':116,    '9':18,    'a':43,     'b':32,     'c':240,    'd': 177,    'e':132,    'f':153},
                '5' : {     '0': 223,   '1' : 76,   '2' : 203,  '3' : 194,  '4' :52,    '5' : 126,  '6' : 118,  '7':5,      '8':109,    '9':183,   'a':169,    'b':49,     'c':209,    'd': 23,    'e':4,    'f':215},
                '6' : {     '0': 20,    '1' : 88,   '2' : 58,   '3' : 97,   '4' :222,   '5' : 27,   '6' : 17,   '7':28,     '8':50,     '9':15,    'a':156,    'b':22,     'c':83,     'd': 24,    'e':242,    'f':34},
                '7' : {     '0': 254,   '1' : 68,   '2' : 207,  '3' : 178,  '4' :195,   '5' : 181,  '6' : 122,  '7':145,    '8':36,     '9':8,     'a':232,    'b':168,    'c':96,     'd': 252,    'e':105,    'f':80},
                '8' : {     '0': 170,   '1' : 208,  '2' : 160,  '3' : 125,  '4' :161,   '5' : 137,  '6' : 98,   '7':151,    '8':84,     '9':91,    'a':30,     'b':149,    'c':224,    'd': 255,    'e':100,    'f':210},
                '9' : {     '0': 16,    '1' : 196,  '2' : 0,    '3' : 72,   '4' :163,   '5' : 247,  '6' : 117,  '7':219,    '8':138,    '9':3,     'a':230,    'b':218,    'c':9,      'd': 63,    'e':221,    'f':148},
                'a' : {     '0': 135,   '1' : 92,   '2' : 131,  '3' : 2,    '4' :205,   '5' : 74,   '6' : 144,  '7':51,     '8':115,    '9':103,   'a':246,    'b':243,     'c':157,    'd': 127,    'e':191,    'f':226},
                'b' : {     '0': 82,    '1' : 155,  '2' : 216,  '3' : 38,   '4' :200,   '5' : 55,   '6' : 198,  '7':59,     '8':129,    '9':150,   'a':111,    'b':75,    'c':19,     'd': 190,    'e':99,    'f':46},
                'c' : {     '0': 233,   '1' : 121,  '2' : 167,  '3' : 140,  '4' :159,   '5' : 110,  '6' : 188,  '7':142,    '8':41,     '9':245,   'a':249,    'b':182,     'c':47,     'd': 253,    'e':180,    'f':89},
                'd' : {     '0': 120,   '1' : 152,  '2' : 6,    '3' : 106,  '4' :231,   '5' : 70,   '6' : 113,  '7':186,    '8':212,    '9':37,    'a':171,    'b':66,    'c':136,    'd': 162,    'e':141,    'f':250},
                'e' : {     '0': 114,   '1' : 7,    '2' : 185,  '3' : 85,   '4' :248,   '5' : 238,  '6' : 172,  '7':10,     '8':54,     '9':73,    'a':42,     'b':104,    'c':60,      'd': 56,    'e':241,    'f':164},
                'f' : {     '0': 64,    '1' : 40,   '2' : 211,  '3' : 123,  '4' :187,   '5' : 201,  '6' : 67,   '7':193,    '8':21,     '9':227,   'a':173,    'b':244,    'c':119,    'd': 199,    'e':128,    'f':158},
                }
    column = str(column)
    return dict[line][column]


def generate_keys():
    if (sender.K == 0):
        private_key = 0x0123456789abcdeffedcba987654321000112233445566778899aabbccddeeff # Si on n'a pas de clef secrete de définie, on utilise le vecteur par défaut décrit dans la RFC de Camelia
        key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\key.dat", "wb") # source file for the key
        key_file_record =  private_key.to_bytes(32, byteorder ='big', signed=False)
        key_file.write(key_file_record)
        key_file.close
    else:
        private_key = sender.K
        key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\key.dat", "wb") # source file for the key
        key_file_record =  private_key.to_bytes(64, byteorder ='big', signed=False)
        key_file.write(key_file_record)
        key_file.close
    return {'private_key': private_key}



def F(F_IN, KE): #fonction de feistel
    x  = F_IN ^ KE
    t1 = x >> 56
    t2 = (x >> 48) & MASK8
    t3 = (x >> 40) & MASK8
    t4 = (x >> 32) & MASK8
    t5 = (x >> 24) & MASK8
    t6 = (x >> 16) & MASK8
    t7 = (x >>  8) & MASK8
    t8 = x & MASK8
    t1 = SBOX1(t1)
    t2 = SBOX2(t2)
    t3 = SBOX3(t3)
    t4 = SBOX4(t4)
    t5 = SBOX2(t5)
    t6 = SBOX3(t6)
    t7 = SBOX4(t7)
    t8 = SBOX1(t8)
    y1 = t1 ^ t3 ^ t4 ^ t6 ^ t7 ^ t8
    y2 = t1 ^ t2 ^ t4 ^ t5 ^ t7 ^ t8
    y3 = t1 ^ t2 ^ t3 ^ t5 ^ t6 ^ t8
    y4 = t2 ^ t3 ^ t4 ^ t5 ^ t6 ^ t7
    y5 = t1 ^ t2 ^ t6 ^ t7 ^ t8
    y6 = t2 ^ t3 ^ t5 ^ t7 ^ t8
    y7 = t3 ^ t4 ^ t5 ^ t6 ^ t8
    y8 = t1 ^ t4 ^ t5 ^ t6 ^ t7
    F_OUT = (y1 << 56) | (y2 << 48) | (y3 << 40) | (y4 << 32) | (y5 << 24) | (y6 << 16) | (y7 <<  8) | y8

    return F_OUT



def FL(FL_IN, KE):

    x1 = FL_IN >> 32
    x2 = FL_IN & MASK32
    k1 = KE >> 32
    k2 = KE & MASK32
    x2 = x2 ^ (rotate_left((x1 & k1),1,32))
    x1 = x1 ^ (x2 | k2)

    return (x1 << 32) | x2


def FLINV(FLINV_IN, KE):

    y1 = FLINV_IN >> 32
    y2 = FLINV_IN & MASK32
    k1 = KE >> 32
    k2 = KE & MASK32
    y1 = y1 ^ (y2 | k2)
    y2 = y2 ^ (rotate_left( (y1 & k1) ,1,32))

    return (y1 << 32) | y2


def complete(text_to_cipher):

    """complete le texte a chiffrer avec des charactères
    vides en un nombre d'élements égale au multiple de la
    taille de bloc si besoin"""

    block_size = 16
    if (len(text_to_cipher) % block_size != 0 ): # si le bloc de texte n'est pas de longeur multiple de 16
        missing_elements_nb = block_size - (len(text_to_cipher) % block_size) # il manque donc n elements
        for i in range(missing_elements_nb):
            text_to_cipher = text_to_cipher + '\0'  # on ajoute donc des charactère NULL (hex 00) pour completer
    return(text_to_cipher)

def calculate_block_amount(text_lenght):

    """calcule le nombre de blocks de 16 bits dans un texte
    """

    if (text_lenght % 16 == 0):
        return text_lenght//16
    else:
        return (text_lenght//(16) + 1)

def encrypt_fonction(mode):

    """touche 5 du menu"""

    if (mode == 'text'):
        text_to_cipher = prompt.string(prompt="Saisir le texte à chiffrer : ")
        print ( )
        print ("->1<- 128 bits")
        print ("->2<- 192 bits")
        print ("->3<- 256 bits")
        print ( )
        key_lenght = prompt.integer(prompt="Saisir la longeur de la clef : ")
        print ( )
        print ("->1<- ECB Electronic Code Book")
        print ("->2<- CBC Cipher Block Chaining")
        print ("->3<- PCBC Propagated Cipher Block Chaining")
        print ( )
        response_encryption = prompt.integer(prompt="Choisisez votre mode de chiffrement : ")
        if (response_encryption == 1): #Electronic Code Book
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                #Préparation des clefs
                if(key_lenght == 1): #128 bits
                    private_key = int(str(hex(private_key))[:33],16)
                    key_schedule_tab = key_schedule(private_key,128)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 2 ): #192 bits
                    private_key = int(str(hex(private_key))[:49],16)
                    key_schedule_tab = key_schedule(private_key,192)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 3 ):  #256 bits
                    private_key = int(str(hex(private_key))[:65],16)
                    key_schedule_tab = key_schedule(private_key,256)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                #initialisation
                block_size = 16
                encrypted_text = ""
                text_to_cipher_block = []
                encrypted_text_int_list = []
                decrypted_text_int_list = []
                text_to_cipher_complete = complete(text_to_cipher)
                block_amount = calculate_block_amount( len(text_to_cipher_complete) )
                #chiffrement
                for i in range(block_amount):
                    text_to_cipher_block.append( text_to_cipher_complete[ (block_size*i) : ( block_size*(i+1) ) ])  # on selectionne le bloc situé aux indices [0:16] [16:32]...
                    text_to_cipher_int = int(  text_to_cipher_block[i].encode().hex(), 16  )
                    encrypted_text_int = encrypt( text_to_cipher_int , kw, ke, k ) # on chiffre ce block
                    encrypted_text_int_list.append( encrypted_text_int )    # on l'ajoute à une liste
                print(encrypted_text_int_list)
                message.value = encrypted_text_int_list
                #dechiffrement
                for i in range(block_amount):
                    encrypted_text = encrypted_text_int_list[i]
                    decrypted_text_int = decrypt( encrypted_text , kw, ke, k ) # on déchiffre le bloc
                    decrypted_text_int_list.append( decrypted_text_int  )
                #Affichage résultat
                print()
                print( "Texte clair (hex) : ")
                for i in range(block_amount):
                    print( text_to_cipher_block[i].encode().hex()  )
                print ( )
                print( "Texte chiffré (hex) : ")
                for i in range(block_amount):
                    print( hex(encrypted_text_int_list[i]) )
                print ()
                print( "Texte déchiffré (hex) : ")
                for i in range(block_amount):
                     print(hex(decrypted_text_int_list[i]))
                print()
        elif ( response_encryption == 2 ): #Cipher Block Chaining
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                #preparation des sous-clefs
                if ( key_lenght == 1 ): # 128 bits
                    private_key = int(str(hex(private_key))[:33],16)
                    key_schedule_tab = key_schedule(private_key,128)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 2 ): # 192 bits
                    private_key = int(str(hex(private_key))[:49],16)
                    key_schedule_tab = key_schedule(private_key,192)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 3 ):  # 256 bits
                    private_key = int(str(hex(private_key))[:65],16)
                    key_schedule_tab = key_schedule(private_key,256)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                # initialisation
                block_size = 16
                encrypted_text = ""
                text_to_cipher_block = []
                initialization_vector = secrets.token_bytes(16)
                # on initialise un vecteur de manière aléatoire, ie. cryptographiquement sécurisé.
                initialization_vector = int.from_bytes(initialization_vector, "big")
                print( "Initialisation Vector" )
                print(hex(initialization_vector))
                encrypted_text_int_list = []
                decrypted_text_int_list = []
                text_to_cipher_complete = complete(text_to_cipher)
                block_amount = calculate_block_amount(len(text_to_cipher_complete))
                # Chiffrement du Premier Block
                text_to_cipher_block.append(text_to_cipher_complete[0:16])
                text_to_cipher_int = int(text_to_cipher_block[0].encode().hex(), 16)
                text_to_cipher_int = initialization_vector ^ text_to_cipher_int
                # XOR entre le IV et le plaintext
                encrypted_text_int = encrypt(text_to_cipher_int , kw, ke, k)
                encrypted_text_int_list.append(encrypted_text_int)
                # Chiffrement des blocks restants
                for i in range( 1, block_amount ):
                    text_to_cipher_block.append(text_to_cipher_complete[(block_size*i):( block_size*(i+1))])
                    text_to_cipher_int = int(text_to_cipher_block[i].encode().hex(), 16)
                    encrypted_text_int = encrypt(text_to_cipher_int ^ encrypted_text_int, kw, ke, k) # chiffrement du XOR entre le chiffré précédent et le plaintext
                    encrypted_text_int_list.append(encrypted_text_int)
                message.value = encrypted_text_int_list
                # Déchiffrement du premier block
                encrypted_text = encrypted_text_int_list[0]
                print(encrypted_text)
                decrypted_text_int = decrypt(encrypted_text , kw, ke, k)
                decrypted_text_int = decrypted_text_int ^ initialization_vector
                decrypted_text_int_list.append(decrypted_text_int)
                 # Déchiffrement des blocks restants
                for i in range(1, block_amount):
                    encrypted_text_int = encrypted_text_int_list[i]
                    decrypted_text_int = decrypt(encrypted_text_int , kw, ke, k)
                    previous_encrypted_text_int = encrypted_text_int_list[i-1]
                    decrypted_text_int = decrypted_text_int ^ previous_encrypted_text_int
                    decrypted_text_int_list.append(decrypted_text_int)
                #Affichage résultat
                print()
                print("Texte clair (hex) : ")
                for i in range( block_amount ):
                    print(text_to_cipher_block[i].encode().hex())
                print( )
                print("Texte chiffré (hex) : ")
                for i in range(block_amount):
                    print(hex(encrypted_text_int_list[i]))
                print ()
                print("Texte déchiffré (hex) : ")
                for i in range(block_amount):
                     print(hex(decrypted_text_int_list[i]))
                print()
        elif(response_encryption == 3): # Propagated Cipher Block Chaining
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                # Preparation des sous-clefs
                if ( key_lenght == 1 ): #128 bits
                    private_key = int(str(hex(private_key))[:33],16)
                    key_schedule_tab = key_schedule(private_key,128)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 2 ): #192 bits
                    private_key = int(str(hex(private_key))[:49],16)
                    key_schedule_tab = key_schedule(private_key,192)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 3 ):  #256 bits
                    private_key = int(str(hex(private_key))[:65],16)
                    key_schedule_tab = key_schedule(private_key,256)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                # Initialisation
                block_size = 16
                encrypted_text = ""
                text_to_cipher_block = []
                initialization_vector = secrets.token_bytes(16)
                initialization_vector = int.from_bytes(initialization_vector, "big")
                print( "Initialisation Vector" )
                print(hex(initialization_vector))
                encrypted_text_int_list = []
                decrypted_text_int_list = []
                text_to_cipher_complete = complete( text_to_cipher )
                block_amount = calculate_block_amount(len(text_to_cipher_complete))
                # Chiffrement du Premier Block
                text_to_cipher_block.append(text_to_cipher_complete[0:16])
                text_to_cipher_int = int(text_to_cipher_block[0].encode().hex(), 16)
                text_to_cipher_int = initialization_vector ^ text_to_cipher_int
                encrypted_text_int = encrypt(text_to_cipher_int , kw, ke, k)
                encrypted_text_int_list.append(encrypted_text_int)
                # Chiffrement des blocks restants
                for i in range(1, block_amount):
                    text_to_cipher_block.append(text_to_cipher_complete[(block_size*i):( block_size*(i + 1))])
                    text_to_cipher_int = int(text_to_cipher_block[i].encode().hex(), 16)
                    previous_text_to_cipher_int = int(text_to_cipher_block[i-1].encode().hex(), 16)
                    previous_encrypted_text_int = encrypted_text_int_list[i-1]
                    encrypted_text_int = encrypt(text_to_cipher_int ^ previous_encrypted_text_int ^ previous_text_to_cipher_int, kw, ke, k)
                    encrypted_text_int_list.append(encrypted_text_int)
                message.value = encrypted_text_int_list
                # Déchiffrement du premier block
                encrypted_text = encrypted_text_int_list[0]
                print(encrypted_text)
                decrypted_text_int = decrypt(encrypted_text , kw, ke, k)
                decrypted_text_int = decrypted_text_int ^ initialization_vector
                decrypted_text_int_list.append(decrypted_text_int)
                 # Déchiffrement des blocks restants
                for i in range(1, block_amount):
                    encrypted_text_int = encrypted_text_int_list[i]
                    decrypted_text_int = decrypt(encrypted_text_int , kw, ke, k)
                    previous_plain_text_int = int(text_to_cipher_block[i-1].encode().hex(), 16)
                    previous_encrypted_text_int = encrypted_text_int_list[i-1]
                    decrypted_text_int = decrypted_text_int ^ previous_encrypted_text_int ^ previous_plain_text_int
                    decrypted_text_int_list.append(decrypted_text_int)
                #Affichage résultat
                print()
                print("Texte clair (hex) : ")
                for i in range(block_amount):
                    print(text_to_cipher_block[i].encode().hex()  )
                print( )
                print("Texte chiffré (hex) : ")
                for i in range( block_amount ):
                    print( hex(encrypted_text_int_list[i]) )
                print ()
                print("Texte déchiffré (hex) : ")
                for i in range( block_amount ):
                     print( hex(decrypted_text_int_list[i]) )
                print()
    elif ( mode == "binary" ):
        key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\key.dat", "rb") # source file for the key
        src = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\message.dat", "rb") # source file for reading (r)b
        dst = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\cipher.dat", "wb")  # cipher destination file for writing (w)b

        print()
        print ("->1<- 128 bits")
        print ("->2<- 192 bits")
        print ("->3<- 256 bits")
        print()
        key_lenght = prompt.integer(prompt="Saisir la longeur de la clef : ")
        print()
        print ("->1<- ECB Electronic Code Book")
        print ("->2<- CBC Cipher Block Chaining")
        print ("->3<- PCBC Propagated Cipher Block Chaining")
        print()
        response_encryption = prompt.integer(prompt="Choisisez votre mode de chiffrement : ")
        if ( response_encryption == 1 ): #Electronic Code Book
            private_key = generate_keys()['private_key']
            if ( key_lenght == 1 ):
                private_key = key_file.read( 16 )
                private_key = int.from_bytes(private_key, byteorder='big')
            elif ( key_lenght == 2 ):
                private_key = key_file.read( 24 )
                private_key = int.from_bytes(private_key, byteorder='big')
            elif ( key_lenght == 3 ):
                private_key = key_file.read( 32 )
                private_key = int.from_bytes(private_key, byteorder='big')
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                try:
                    # Preparation des sous-clefs
                    if ( key_lenght == 1 ): #128 bits
                        key_schedule_tab = key_schedule(private_key,128)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    elif ( key_lenght == 2 ): #192 bits
                        key_schedule_tab = key_schedule(private_key,192)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    elif ( key_lenght == 3 ):  #256 bits
                        key_schedule_tab = key_schedule(private_key,256)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    record = src.read( 16 ) # Read a record (block) from source file
                    while record :
                        block_int = int.from_bytes(record, byteorder='big', signed=False)
                        encrypted_block_int = encrypt( block_int, kw, ke, k )
                        encrypted_record =  encrypted_block_int.to_bytes(16, byteorder ='big', signed=False)
                        dst.write( encrypted_record )
                        record = src.read( 16 )
                except IOError:
                    # Your error handling here
                    # Nothing for this example
                    pass
                finally:
                    src.close()
                    dst.close()

                    cipher = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\cipher.dat", "rb")
                    record = cipher.read( 16 )
                    decrypted = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\decrypted.dat", "wb")  # cipher destination file for writing (w)b
                    while record :
                        block_int = int.from_bytes(record, byteorder='big', signed=False)
                        decrypted_block_int = decrypt( block_int, kw, ke, k )
                        decrypted_record =  decrypted_block_int.to_bytes(16, byteorder ='big', signed=False)
                        decrypted.write( decrypted_record )
                        record = cipher.read( 16 )
                    cipher.close()
                    decrypted.close()
        elif ( response_encryption == 2 ): #Cipher Block Chaining
            private_key = generate_keys()['private_key']
            if ( key_lenght == 1 ):
                private_key = key_file.read( 16 )
                private_key = int.from_bytes(private_key, byteorder='big')
            elif ( key_lenght == 2 ):
                private_key = key_file.read( 24 )
                private_key = int.from_bytes(private_key, byteorder='big')
            elif ( key_lenght == 3 ):
                private_key = key_file.read( 32 )
                private_key = int.from_bytes(private_key, byteorder='big')
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                try:
                    # Preparation des sous-clefs
                    if ( key_lenght == 1 ): #128 bits
                        key_schedule_tab = key_schedule(private_key,128)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    elif ( key_lenght == 2 ): #192 bits
                        key_schedule_tab = key_schedule(private_key,192)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    elif ( key_lenght == 3 ):  #256 bits
                        key_schedule_tab = key_schedule(private_key,256)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    initialization_vector = secrets.token_bytes(16)
                    initialization_vector = int.from_bytes( initialization_vector, "big")
                    print( "Initialisation Vector" )
                    print(hex(initialization_vector))
                    record = src.read( 16 ) # Read a 128 bit record from source file
                    block_int = int.from_bytes(record, byteorder='big', signed=False)
                    encrypted_block_int = encrypt( block_int ^ initialization_vector, kw, ke, k )
                    encrypted_record =  encrypted_block_int.to_bytes(16, byteorder ='big', signed=False)
                    dst.write( encrypted_record )
                    record = src.read( 16 )
                    while record :
                        plaintext_block_int = int.from_bytes(record, byteorder='big', signed=False)
                        encrypted_block_int = encrypt( encrypted_block_int ^ plaintext_block_int, kw, ke, k )
                        encrypted_record =  encrypted_block_int.to_bytes(16, byteorder ='big', signed=False)
                        dst.write( encrypted_record )
                        record = src.read( 16 )
                except IOError:
                    # Your error handling here
                    # Nothing for this example
                    pass
                finally:
                    src.close()
                    dst.close()


        elif ( response_encryption == 3 ): #Propagated Cipher Block Chaining
            private_key = generate_keys()['private_key']
            if ( key_lenght == 1 ):
                private_key = key_file.read( 16 )
                private_key = int.from_bytes(private_key, byteorder='big')
            elif ( key_lenght == 2 ):
                private_key = key_file.read( 24 )
                private_key = int.from_bytes(private_key, byteorder='big')
            elif ( key_lenght == 3 ):
                private_key = key_file.read( 32 )
                private_key = int.from_bytes(private_key, byteorder='big')
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                try:
                    # Preparation des sous-clefs
                    if ( key_lenght == 1 ): #128 bits
                        key_schedule_tab = key_schedule(private_key,128)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    elif ( key_lenght == 2 ): #192 bits
                        key_schedule_tab = key_schedule(private_key,192)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    elif ( key_lenght == 3 ):  #256 bits
                        key_schedule_tab = key_schedule(private_key,256)
                        k = key_schedule_tab['k']
                        ke = key_schedule_tab['ke']
                        kw = key_schedule_tab['kw']
                    initialization_vector = secrets.token_bytes(16)
                    initialization_vector = int.from_bytes( initialization_vector, "big")
                    print( "Initialisation Vector" )
                    print(hex(initialization_vector))
                    record = src.read( 16 ) # Read a 128 bit record from source file
                    block_int = int.from_bytes(record, byteorder='big', signed=False)
                    encrypted_block_int = encrypt( block_int ^ initialization_vector, kw, ke, k )
                    encrypted_record =  encrypted_block_int.to_bytes(16, byteorder ='big', signed=False)
                    dst.write( encrypted_record )
                    record = src.read( 16 )
                    while record :
                        plaintext_block_int = int.from_bytes(record, byteorder='big', signed=False)
                        encrypted_block_int = encrypt( encrypted_block_int ^ block_int ^  plaintext_block_int, kw, ke, k )
                        encrypted_record =  encrypted_block_int.to_bytes(16, byteorder ='big', signed=False)
                        dst.write( encrypted_record )
                        block_int = plaintext_block_int
                        record = src.read( 16 )
                except IOError:
                    # Your error handling here
                    # Nothing for this example
                    pass
                finally:
                    src.close()
                    dst.close()

def is_prime(number, method):

    """ Test de primalité de number avec 3 méthodes possibles, le crible d' Eratostene, le théorème de fermat et le test de pseudo primalité de rabin miller """

    if method == ('Eratostene'):
        return eratostene_2(number)
    elif method == ('Fermat'):
        return fermat(number)
    elif method == ('Rabin-Miller'):
        return rabinMiller(number,40) #40 itérations (recomandation du Handbook of Applied Cryptography)

def eratostene_2(n): # ma version du crible d'eratostene
    if n == 1: # 1 n'est pas premier
        return False
    d = 2
    while d**2 <= n and n%d!=0:
        d = d+1
    if d**2 > n:
        return True
    else:
        return False

def fermat(number): #Test de primalité de fermat
    a = secrets.SystemRandom().randrange(1, number)
    if ( ( a ** (number-1) ) % number == 1 ):
        return True
    else:
        return False

def rabinMiller(n, k): #retourne True si number passe k rounds du test de primalité de miler rabin (probablement premier)
    # Test si n est pair, mais attention, n est premier
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s = s + 1
        r = r // 2
    for i in range(k): # fait k tests, ici 40
        a = secrets.SystemRandom().randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j = j + 1
            if x != n - 1:
                return False
    return True

def pow(x,e,m): #calcul de l'exponentiation modulaire rapide
    y = 1
    while e>0:
        if e%2 == 0:
            x = (x*x) % m
            e = e // 2
        else:
            y = (x * y) % m
            e = e-1
    return y


def inverse(a, m): #calcul de l'inverse
    g = pgcd(a, m)
    if (g != 1):
        print("L'inverse n'existe pas")
    else :
        return pow(a, m - 2, m)

def pgcd(a,b): #calcul du PGCD
    if (a == 0):
        return b
    return pgcd( pow(b,1,a), a)


def gen_p_q_DSA(L, N, test_method):
    print('Generation de p,q...')

    """ Methode naive pour generer p et q pour DSA
    """

    q = secrets.randbits(N)
    while not(is_prime(q, test_method)):
        q = secrets.randbits(N)
    i = 2**L
    p = 0
    while not(is_prime(p, test_method)):
        i = i + 1
        p = q*i + 1
    return p,q,i

def generate_probable_prime_pair_for_DSA(L ,N , seedlen, test_method):

    """ Implementation officielle du NIST décrite dans la norme FIPS 182-4
    """
    print('Generation de p,q...')
    outlen = 256
    V = []
    W = 0

    if ( seedlen < N ):
        return "invalid seed lenght"
    n = math.ceil(L / outlen) - 1
    b = L - 1 - ( n * outlen )
    while(1): #extrement dangereux
        domain_name_seed = secrets.randbits( seedlen )
        U = pow( int(hashlib.sha256( (domain_name_seed ).to_bytes(seedlen, byteorder='big') ).hexdigest(), 16), 1, 2**(N-1) )
        q = 2**(N-1) + U + 1 - ( pow(U,1,2) )
        while ( not(is_prime(q, test_method) ) ):
            domain_name_seed = secrets.randbits( seedlen )
            U = pow( int( hashlib.sha256( (domain_name_seed ).to_bytes(seedlen, byteorder='big') ).hexdigest(), 16), 1 , 2**(N-1) )
            q = 2**( N-1 ) + U + 1 - ( pow(U,1,2) )
        offset = 1
        for counter in range( 4*L ):
            for j in range( n + 1 ):
                V.append(pow(int(hashlib.sha256( (domain_name_seed + offset + j).to_bytes(seedlen, byteorder='big') ).hexdigest(), 16), 1, 2**seedlen))
            for i in range( n ):
                W = W + V[i]*(2**(i*outlen))
            W = W + pow( V[n],1,2**b )
            X = W + 2**(L-1)
            c = pow( X, 1, 2*q )
            p = X -( c - 1 )
            if p >= (2 ** (L - 1)):
                if ( is_prime(p, test_method) ):
                    return ( p,q )
                offset = offset + n + 1
            else:
                offset = offset + n + 1

def DSA_generate_params(L_lenght, N_lenght, test_method):

    """Génére les paramétres p, q, g de DSA celon la méthode précedente.
    """

    p_q_pair = generate_probable_prime_pair_for_DSA(L_lenght, N_lenght, 256, test_method)
    (p, q) = p_q_pair[0],p_q_pair[1]
    h = secrets.SystemRandom().randrange(2,p-2) # on choisi un h au hasard entre 2 et p-2
    g = pow( h , (p-1)//q, p) # g = h ^ (p-1)/q [p]


    return {'p': p,'q': q,'g': g }


def sign_dsa(message, private_key, p, q, g):
    print('Signature en cours...')
    k = secrets.SystemRandom().randrange(1, q - 1)  # on choisi un k au hasard entre 1 et q -1
    r = pow( pow(g,k,p) , 1, q) # on calcule r = (g^k mod p) mod q
    hash = (int(sha1(to_binary(xmpz(message))).hexdigest(), 16)) # on calcule le hash du message
    s = pow(inverse(k,q)*(hash + private_key*r),1 ,q ) #  on calcule s = (k^-1 (H(m) + xr) mod q
    while (r == 0 or s == 0): # dans le cas ou r ou s son nul, on recalcule la signature (r,s)
        k = secrets.SystemRandom().randrange(1,q-1)
        r = pow(pow(g,k,p),1, q)
        s = pow((inverse(k,q)*hash + private_key*r),1 ,q ) #la signature est (r,s)
    return s,r,hash

def sign_dsa_message(message, private_key, p, q, g): # de même que ci dessous, sauf que il faut calculer le hash du message total
    print('Signature en cours...')
    concat = ""
    for i in range(len(message.value)):
        concat = concat + hex(message.value[i])[2:]
    k = secrets.SystemRandom().randrange(1, q - 1)
    r = pow( pow(g,k,p) , 1, q)
    hash = (int(sha1(concat.encode()).hexdigest(), 16))
    s = pow(inverse(k,q)*(hash + private_key*r),1 ,q )
    while (r == 0 or s == 0):
        k = secrets.SystemRandom().randrange(1,q-1)
        r = pow(pow(g,k,p),1, q)
        s = pow((inverse(k,q)*hash + private_key*r),1 ,q )
    return s,r,hash #la signature est (r,s)


def validate_sign_dsa(s, r, hash, y, p, q, g):
    if ( not(0<r<q) or not( 0<s<q) ):
        return False
    w = inverse(s,q) # on calcule w = s^-1 mod q
    u1 = pow(hash*w,1,q) # on calcule u1 = hash(message) * w mod q
    u2 = pow(r*w,1,q) # on calcule u2 = r * w mod q
    b = pow(y,u2,p)
    a = pow(g,u1,p)
    v = pow( pow(a*b,1,p),1,q) # on calcule (g^u1 * y^u2 mod p) mod q

    print("v = " + str(hex(v)))
    print("r = " + str(hex(r)))

    return v == r # si v == r (True) la signature est valide

def generate_safe_prime(bit_lenght, test_method):

    """
    Génére un nombre premier cryptographiquement sécurisé p tel que 2*p + 1 est également premier. Cette methode est détaillé dans la rfc du protocole d'échange de clef de deffie Helman adapoté par SSH et dans le HandBook Of Aplied Cryptography
    """

    print("generate safe prime")
    q = generate_prime_number(bit_lenght-1, test_method)
    print("Calculate")
    p = 2*q + 1
    while (not(is_prime( ((q-1)//2), test_method)) and not(is_prime( (p), test_method))): # on test la primalité avec p = 2*q+1 et (q-1)//2
        q = generate_prime_number(bit_lenght-1, test_method)
        print('.', end='')
        p = 2*q + 1
    print("P :")
    print(p)
    return p



def generate_generator(p):
    print("Generate Generator")
    """
    D'après la RFC de SSH, pour l'échange de clef de deffie Helman, il est recomandé d'uitilser 2 ou 5 comme génerateur ce qui est possible car p est cryptographiquement sécurisé. ON se contente ici de la définition : un element alpha est générateur ssi alpha^p mod p est different de 1 et alpha^2 mod p different de 2
    """
    for g in range (1,p-1):
        if ( pow(g,(p-1)//2,p) != 1 and pow(g,2,p) != 1 ):
            print("Generator = " + str(g))
            return g
    return 'no generator'




def generate_random_number_for_primality_test(bit_length):

    """
    Génere un entier d'une suite de bits, typiquement dans notre implementation
    entre 512 bits (bit de poid fort) et 512 + (1 + 2 + 4 + 8 +....) = 1023 bits

    on applique un masque pour ne garder que les impaires (tout les premiers étant impaires)

    """

    h = secrets.randbits(bit_length)
    h = h | ( (1 << bit_length - 1) | 1)
    return h


def generate_prime_number(bit_length, test_method): #test method = 'Rabin-Miller', 'Fermat', 'eratostene'

    """
    On se propose de tester la primalité du nombre aléatoire spécifique généré dans la méthode ci-dessus

    """
    p = generate_random_number_for_primality_test(bit_length)
    while not(is_prime(p, test_method)):

        p = generate_random_number_for_primality_test(bit_length)
    return p

def generate_public_private_keys_asymetric_el_gamal(p , g):

    """on retourne x,y a partir du set de parametre p, g"""

    """On genere un entier aléatoire x dans [1,p - 1]"""


    x = secrets.SystemRandom().randrange(1, p - 2)
    y = pow(g,x,p)

    return {'private_key': x, 'public_key': y }

def generate_public_private_keys_asymetric_dsa(p, q , g):

    print("Géneration d'un couple de clés privé/publique x,y")

    """on retourne x,y a partir du set de parametre p, q, g"""

    """On genere un entier aléatoire x dans [1,q-1]"""

    p = int(p)
    q = int(q)
    g = int(g)



    x = secrets.SystemRandom().randrange(1, q-1)
    y = pow(g,x,p)

    return {'private_key': x, 'public_key': y }

def rotate_left(val, r_bits, max_bits):

    """fonctionne correctement à présent"""

    return (val << r_bits%max_bits) & (2**max_bits-1) | ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))











def key_schedule(K, key_length):


    if ( key_length ) == 128:

        KL = K
        KR = 0

    elif ( key_length ) == 192:


        KL = K >> 64




        KR = ((K & MASK64) << 64) | (~(K & MASK64))& MASK64


    elif ( key_length ) == 256:

        KL = K >> 128
        KR = K & MASK128

    D1 = (KL ^ KR) >> 64
    D2 = (KL ^ KR) & MASK64
    D2 = D2 ^ F(D1, Sigma1)
    D1 = D1 ^ F(D2, Sigma2)
    D1 = D1 ^ (KL >> 64)
    D2 = D2 ^ (KL & MASK64)
    D2 = D2 ^ F(D1, Sigma3)
    D1 = D1 ^ F(D2, Sigma4)
    KA = (D1 << 64) | D2
    D1 = (KA ^ KR) >> 64
    D2 = (KA ^ KR) & MASK64
    D2 = D2 ^ F(D1, Sigma5)
    D1 = D1 ^ F(D2, Sigma6)
    KB = (D1 << 64) | D2

    if ( key_length ) == 128:

        kw1 = (rotate_left(KL,0,128) ) >> 64
        kw2 = (rotate_left(KL,0,128) ) & MASK64
        k1  = (rotate_left(KA,0,128) ) >> 64
        k2  = (rotate_left(KA,0,128) ) & MASK64
        k3  = (rotate_left(KL,15,128)  ) >> 64
        k4  = (rotate_left(KL,15,128)  ) & MASK64
        k5  = (rotate_left(KA,15,128)  ) >> 64
        k6  = (rotate_left(KA,15,128)  ) & MASK64
        ke1 = (rotate_left(KA,30,128)  ) >> 64
        ke2 = (rotate_left(KA,30,128)  ) & MASK64
        k7  = (rotate_left(KL,45,128)  ) >> 64
        k8  = (rotate_left(KL,45,128)  ) & MASK64
        k9  = (rotate_left(KA,45,128)  ) >> 64
        k10 = (rotate_left(KL,60,128)  ) & MASK64
        k11 = (rotate_left(KA,60,128)  ) >> 64
        k12 = (rotate_left(KA,60,128)  ) & MASK64
        ke3 = (rotate_left(KL,77,128)  ) >> 64
        ke4 = (rotate_left(KL,77,128)  ) & MASK64
        k13 = (rotate_left(KL,94,128)  ) >> 64
        k14 = (rotate_left(KL,94,128)  ) & MASK64
        k15 = (rotate_left(KA,94,128)  ) >> 64
        k16 = (rotate_left(KA,94,128)  ) & MASK64
        k17 = (rotate_left(KL,111,128) ) >> 64
        k18 = (rotate_left(KL,111,128) ) & MASK64
        kw3 = (rotate_left(KA,111,128) ) >> 64
        kw4 = (rotate_left(KA,111,128) ) & MASK64
        kw = [kw1,kw2,kw3,kw4]
        k = [k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17,k18]
        ke = [ke1,ke2,ke3,ke4]

    elif ( key_length == 192 or key_length == 256):


        kw1 = ( rotate_left(KL,0,128) ) >> 64
        kw2 = ( rotate_left(KL,0,128) ) & MASK64
        k1  = ( rotate_left(KB,0,128) ) >> 64
        k2  = ( rotate_left(KB,0,128) ) & MASK64
        k3  = ( rotate_left(KR,15,128) ) >> 64
        k4  = ( rotate_left(KR,15,128) ) & MASK64
        k5  = ( rotate_left(KA,15,128) ) >> 64
        k6  = ( rotate_left(KA,15,128) ) & MASK64
        ke1 = ( rotate_left(KR,30,128) ) >> 64
        ke2 = ( rotate_left(KR,30,128) ) & MASK64
        k7  = ( rotate_left(KB,30,128) ) >> 64
        k8  = ( rotate_left(KB,30,128) ) & MASK64
        k9  = ( rotate_left(KL,45,128) ) >> 64
        k10 = ( rotate_left(KL,45,128) ) & MASK64
        k11 = ( rotate_left(KA,45,128) ) >> 64
        k12 = ( rotate_left(KA,45,128) ) & MASK64
        ke3 = ( rotate_left(KL,60,128) ) >> 64
        ke4 = ( rotate_left(KL,60,128) ) & MASK64
        k13 = ( rotate_left(KR,60,128) ) >> 64
        k14 = ( rotate_left(KR,60,128) ) & MASK64
        k15 = ( rotate_left(KB,60,128) ) >> 64
        k16 = ( rotate_left(KB,60,128) ) & MASK64
        k17 = ( rotate_left(KL,77,128) ) >> 64
        k18 = ( rotate_left(KL,77,128) ) & MASK64
        ke5 = ( rotate_left(KA,77,128) ) >> 64
        ke6 = ( rotate_left(KA,77,128) ) & MASK64
        k19 = ( rotate_left(KR,94,128) ) >> 64
        k20 = ( rotate_left(KR,94,128) ) & MASK64
        k21 = ( rotate_left(KA,94,128) ) >> 64
        k22 = ( rotate_left(KA,94,128) ) & MASK64
        k23 = ( rotate_left(KL,111,128) ) >> 64
        k24 = ( rotate_left(KL,111,128) ) & MASK64
        kw3 = ( rotate_left(KB,111,128) ) >> 64
        kw4 = ( rotate_left(KB,111,128) ) & MASK64
        kw = [kw1,kw2,kw3,kw4]
        k = [k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17,k18,k19,k20,k21,k22,k23,k24]
        ke = [ke1,ke2,ke3,ke4,ke5,ke6]
    return {'KA': KA, 'KB': KB ,'KR': KR, 'KL' : KL, 'ke' : ke, 'k' : k , 'kw' : kw}

def encrypt(M, kw, ke, k ):


    if (len(k) == 18): #128bit key
                            #indicies are lowered to minus 1 to improve readability
        D1 = M >> 64
        D2 = M & MASK64

        D1 = D1 ^ kw[1-1]       # Prewhitening
        D2 = D2 ^ kw[2-1]
        D2 = D2 ^ F(D1, k[1-1])     # Round 1
        D1 = D1 ^ F(D2, k[2-1])     # Round 2
        D2 = D2 ^ F(D1, k[3-1])     # Round 3
        D1 = D1 ^ F(D2, k[4-1])     # Round 4
        D2 = D2 ^ F(D1, k[5-1])     # Round 5
        D1 = D1 ^ F(D2, k[6-1])     # Round 6
        D1 = FL   (D1, ke[1-1])     # FL
        D2 = FLINV(D2, ke[2-1])     # FLINV
        D2 = D2 ^ F(D1, k[7-1])     # Round 7
        D1 = D1 ^ F(D2, k[8-1])     # Round 8
        D2 = D2 ^ F(D1, k[9-1])     # Round 9
        D1 = D1 ^ F(D2, k[10-1])    # Round 10
        D2 = D2 ^ F(D1, k[11-1])    # Round 11
        D1 = D1 ^ F(D2, k[12-1])    # Round 12
        D1 = FL   (D1, ke[3-1])     # FL
        D2 = FLINV(D2, ke[4-1])     # FLINV
        D2 = D2 ^ F(D1, k[13-1])    # Round 13
        D1 = D1 ^ F(D2, k[14-1])    # Round 14
        D2 = D2 ^ F(D1, k[15-1])    # Round 15
        D1 = D1 ^ F(D2, k[16-1])    # Round 16
        D2 = D2 ^ F(D1, k[17-1])    # Round 17
        D1 = D1 ^ F(D2, k[18-1])    # Round 18
        D2 = D2 ^ kw[3-1]           # Postwhitening
        D1 = D1 ^ kw[4-1]
        C = (D2 << 64) | D1


    else: #129 256 bit key

        D1 = M >> 64
        D2 = M & MASK64


        D1 = D1 ^ kw[1-1]
        D2 = D2 ^ kw[2-1]
        D2 = D2 ^ F(D1, k[1-1])
        D1 = D1 ^ F(D2, k[2-1])
        D2 = D2 ^ F(D1, k[3-1])
        D1 = D1 ^ F(D2, k[4-1])
        D2 = D2 ^ F(D1, k[5-1])
        D1 = D1 ^ F(D2, k[6-1])
        D1 = FL   (D1, ke[1-1])
        D2 = FLINV(D2, ke[2-1])
        D2 = D2 ^ F(D1, k[7-1])
        D1 = D1 ^ F(D2, k[8-1])
        D2 = D2 ^ F(D1, k[9-1])
        D1 = D1 ^ F(D2, k[10-1])
        D2 = D2 ^ F(D1, k[11-1])
        D1 = D1 ^ F(D2, k[12-1])
        D1 = FL   (D1, ke[3-1])
        D2 = FLINV(D2, ke[4-1])
        D2 = D2 ^ F(D1, k[13-1])
        D1 = D1 ^ F(D2, k[14-1])
        D2 = D2 ^ F(D1, k[15-1])
        D1 = D1 ^ F(D2, k[16-1])
        D2 = D2 ^ F(D1, k[17-1])
        D1 = D1 ^ F(D2, k[18-1])
        D1 = FL   (D1, ke[5-1])
        D2 = FLINV(D2, ke[6-1])
        D2 = D2 ^ F(D1, k[19-1])
        D1 = D1 ^ F(D2, k[20-1])
        D2 = D2 ^ F(D1, k[21-1])
        D1 = D1 ^ F(D2, k[22-1])
        D2 = D2 ^ F(D1, k[23-1])
        D1 = D1 ^ F(D2, k[24-1])
        D2 = D2 ^ kw[3-1]
        D1 = D1 ^ kw[4-1]

        #128-bit ciphertext C is constructed from D1 and D2 as follows.

        C = (D2 << 64) | D1

    return C


def decrypt(C, kw, ke, k):

    kw2 = kw.copy()
    ke2 = ke.copy()
    k2 = k.copy()


                        #indicies are lowered to minus 1 to improve readability
    if (len(ke) == 4): #128bits key
        kw2[1-1], kw2[3-1] = kw2[3-1], kw2[1-1]
        kw2[2-1], kw2[4-1] = kw2[4-1], kw2[2-1]
        k2[1-1], k2[18-1] = k2[18-1], k2[1-1]
        k2[2-1], k2[17-1] = k2[17-1], k2[2-1]
        k2[3-1], k2[16-1] = k2[16-1], k2[3-1]
        k2[4-1], k2[15-1] = k2[15-1], k2[4-1]
        k2[5-1], k2[14-1] = k2[14-1], k2[5-1]
        k2[6-1], k2[13-1] = k2[13-1], k2[6-1]
        k2[7-1], k2[12-1] = k2[12-1], k2[7-1]
        k2[8-1], k2[11-1] = k2[11-1], k2[8-1]
        k2[9-1], k2[10-1] = k2[10-1], k2[9-1]
        ke2[1-1], ke2[4-1] = ke2[4-1], ke2[1-1]
        ke2[2-1], ke2[3-1] = ke2[3-1], ke2[2-1]
    elif (len(ke) == 6): #192-256 bits key
        kw2[1-1], kw2[3-1] = kw2[3-1], kw2[1-1]
        kw2[2-1], kw2[4-1] = kw2[4-1], kw2[2-1]
        k2[1-1], k2[24-1] = k2[24-1], k2[1-1]
        k2[2-1], k2[23-1] = k2[23-1], k2[2-1]
        k2[3-1], k2[22-1] = k2[22-1], k2[3-1]
        k2[4-1], k2[21-1] = k2[21-1], k2[4-1]
        k2[5-1], k2[20-1] = k2[20-1], k2[5-1]
        k2[6-1], k2[19-1] = k2[19-1], k2[6-1]
        k2[7-1], k2[18-1] = k2[18-1], k2[7-1]
        k2[8-1], k2[17-1] = k2[17-1], k2[8-1]
        k2[9-1], k2[16-1] = k2[16-1], k2[9-1]
        k2[10-1], k2[15-1] = k2[15-1], k2[10-1]
        k2[11-1], k2[14-1] = k2[14-1], k2[11-1]
        k2[12-1], k2[13-1] = k2[13-1], k2[12-1]
        ke2[1-1], ke2[6-1] = ke2[6-1], ke2[1-1]
        ke2[2-1], ke2[5-1] = ke2[5-1], ke2[2-1]
        ke2[3-1], ke2[4-1] = ke2[4-1], ke2[3-1]
    return encrypt(C, kw2, ke2, k2 )







class Message:

    def __init__(self, value, signature):
        self.value = value
        self.signature = signature


    def __str__(self):

        return 'Message : value = ' + str(self.value) + '  signature = ' + str(self.signature)




class Sender:

    def __init__(self, private_key, public_key_certificator):
        self.public_key_certificator = public_key_certificator
        self.private_key = private_key
        self.p = 0
        self.g = 0
        self.a = 0
        self.A = 0
        self.K = 0

    @staticmethod
    def verify_certificate(system, receiver, certificator_public_key):

        if(validate_sign_dsa(receiver.certificate[0],receiver.certificate[1],receiver.certificate[2] ,certificator_public_key, system.p, system.q, system.g ) == True):
            print("Certificat valide")
        else:
            print("Certificat invalide")

    def send_message(message, key_lenght, mode):
        print("ok")

    def send_message(key_lenght, mode):
        print("ok")

    def sign(self, message,system):
       signature = sign_dsa_message(message, self.private_key , system.p, system.q, system.g)
       message.signature = signature

    def encrypt(message, private_key):
        print("ok")

    def send_difie_hellman_params(self, Receiver):
        Receiver.B = pow(self.g,Receiver.b,self.p)

    def set_private_key(B):
        self.K = pow(B,a,p)


    def request_public_key(certificator):
      return certificator.public_key

    def requestPublicKey(certificator):
        self.certificatorPublicKey = certificator.publicKey


    def __str__(self):
        return 'Sender : ' +  '\n' +'private_key = ' + str(hex(self.private_key))  +  '\n' + 'public_key_certificator = ' + str(hex(self.public_key_certificator))  +  '\n' + ' Secret Key =' + str(hex(self.K))


class Receiver:

    def __init__(self, private_key, public_key, certificate):
        self.public_key = public_key
        self.private_key = private_key
        self.certificate = certificate
        self.b = 0
        self.K = 0


    def decrypt(Message, key_lenght):
        return certificator.signPrivc(publicKeyS)

    def ask_signature(public_key):
        print("ok")

    def sign(private_key, public_key):
        print("ok")

    def send_B_and_set_private_key(self, Sender):
        self.b = secrets.SystemRandom().randrange(2,(Sender.p)-2)
        Sender.K = pow(self.B,Sender.a,Sender.p)

    def set_private_key(self, A, p):
        self.K = pow(A,self.b,p)


    @staticmethod
    def verify_signature(message, sender):
        if(validate_sign_dsa(message.signature[0],message.signature[1],message.signature[2] ,sender.public_key, system.p, system.q, system.g ) == True):
            print("Signature valide")
        else:
            print("Signature invalide")


    def __str__(self):

        if(isinstance(self.certificate, tuple)):
            hex_certif = []
            for i in range(len(self.certificate)):
                hex_certif.append(hex(self.certificate[i]))
        else:
            hex_certif = hex(self.certificate)

        return  'Receiver :'+  '\n' +'private_key = ' +  str(hex(self.private_key)) +  '\n' + 'public_key = ' + str(hex(self.public_key)) +  '\n' + 'certificate = ' + str(hex_certif) +  '\n' + 'Secret Key = ' + str(hex(self.K))

class Certificator:

    def __init__(self, private_key, public_key):
        self.public_key = public_key
        self.private_key = private_key




    def sign_with_private_key(self, receiver_public_key, system):
        return sign_dsa(receiver_public_key, self.private_key, system.p, system.q, system.g)

    def __str__(self):
        return 'Certificator :' +  '\n' + 'private_key = ' + str(hex(self.private_key)) + '\n' +'public_key = ' + str(hex(self.public_key))

class System:

    def __init__(self, p, q, g):
        self.p = p
        self.q = q
        self.g = g





def main(): #programme principal
    print ("Bonjour ô maitre ! Que souhaitez vous faire aujourd'hui ?")
    print ("->1<- Générer des couples de clés publiques / privées.")
    print ("->2<- Générer un certificat.")
    print ("->3<- Vérifier la validité d'un certificat.")
    print ("->4<- Partager la clé secrète.")
    print ("->5<- Chiffrer un message.")
    print ("->6<- Signer un message.")
    print ("->7<- Vérifier une signature.")
    print ("->8<- Toutes les étapes")
    print ("->9<- Terminer")
    """
    Test Vector
        key_schedule_tab = key_schedule(0x0123456789abcdeffedcba9876543210,128)
        k = key_schedule_tab['k']
        ke = key_schedule_tab['ke']
        kw = key_schedule_tab['kw']

        encrypted_int = encrypt( 0x0123456789abcdeffedcba9876543210 , kw, ke, k )
        print( hex(0x0123456789abcdeffedcba9876543210) )
        print ( hex(encrypted_int) )
    """
    response = prompt.integer(prompt="Choisisez votre action : ")
    if (response == 1): # generation de couples de clef public/privé
        """
        il s'agit de trouver un q, p, fortement premier et calculer g
        les paramétres de DSA tel que définit dans la publication du NIST FIPS 186-4
        Ensuite il est possible de générer par utilisateur des couples clefs publics/privées
        """
        params_tab = DSA_generate_params(1024, 160, 'Rabin-Miller')
        system.p = params_tab['p']
        system.q = params_tab['q']
        system.g = params_tab['g']
        print("P :")
        print(system.p)
        print("Q :")
        print(system.q)
        key_tab = generate_public_private_keys_asymetric_dsa(system.p, system.q, system.g)
        certificator.public_key = key_tab['public_key']
        certificator.private_key = key_tab['private_key']
        key_tab_receiver = generate_public_private_keys_asymetric_dsa(system.p,system.q,system.g)
        receiver.private_key =  key_tab_receiver['private_key']
        receiver.public_key = key_tab_receiver['public_key']
        key_tab_sender = generate_public_private_keys_asymetric_dsa(system.p,system.q,system.g)
        sender.private_key =  key_tab_sender['private_key']
        sender.public_key = key_tab_sender['public_key']


        # Écriture des clef dans des fichiers

        certificator_public_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Certificator\public_key.dat", "wb")  # destination file for writing (w)b
        certificator_public_key_record =  certificator.public_key.to_bytes(128, byteorder ='big', signed=False)
        certificator_public_key_file.write(certificator_public_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             certificator_public_key_file.write(tag_record)
        certificator_public_key_file.close()

        certificator_private_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Certificator\private_key.dat", "wb")  # destination file for writing (w)b
        certificator_private_key_record =  certificator.private_key.to_bytes(20, byteorder ='big', signed=False)
        certificator_private_key_file.write(certificator_private_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             certificator_private_key_file.write(tag_record)
        certificator_private_key_file.close()

        sender_public_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Sender\public_key.dat", "wb")  # destination file for writing (w)b
        sender_public_key_record = sender.public_key.to_bytes(128, byteorder ='big', signed=False)
        sender_public_key_file.write(sender_public_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             sender_public_key_file.write(tag_record)
        sender_public_key_file.close()

        sender_private_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Sender\private_key.dat", "wb")  # destination file for writing (w)b
        sender_private_key_record = sender.private_key.to_bytes(20, byteorder ='big', signed=False)
        sender_private_key_file.write(sender_private_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             sender_private_key_file.write(tag_record)
        sender_private_key_file.close()

        receiver_public_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Receiver\public_key.dat", "wb")  # destination file for writing (w)b
        receiver_public_key_record = receiver.public_key.to_bytes(128, byteorder ='big', signed=False)
        receiver_public_key_file.write(receiver_public_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             receiver_public_key_file.write(tag_record)
        receiver_public_key_file.close()

        receiver_private_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Receiver\private_key.dat", "wb")  # destination file for writing (w)b
        receiver_private_key_record = receiver.private_key.to_bytes(20, byteorder ='big', signed=False)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             receiver_private_key_file.write(tag_record)
        receiver_private_key_file.write(receiver_private_key_record)
        receiver_private_key_file.close()


        print("")
        print(str(receiver))
        print("")
        print(str(sender))
        print("")
        print(str(certificator))
        print("")
        print(str(message))
        print("")
        main()
    elif ( response == 2 ): # géneration d'un certificat
        receiver.certificate = certificator.sign_with_private_key(receiver.public_key,system)
        print(receiver.certificate)
        receiver_certificate_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Certificator\certificate.pem", "wb")  # destination file for writing (w)b
        certificator_record_s1 = receiver.certificate[0].to_bytes(128, byteorder ='big', signed=False)
        certificator_record_s2 = receiver.certificate[1].to_bytes(128, byteorder ='big', signed=False)
        certificator_record_hash = receiver.certificate[2].to_bytes(128, byteorder ='big', signed=False)
        receiver_certificate_file.write(certificator_record_s1)
        receiver_certificate_file.write(certificator_record_s2)
        receiver_certificate_file.write(certificator_record_hash)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             receiver_certificate_file.write(tag_record)
        receiver_certificate_file.close()

        print("")
        print(str(receiver))
        print("")
        print(str(sender))
        print("")
        print(str(certificator))
        print("")
        print(str(message))
        main()
    elif ( response == 3 ): # verifier la validité d'un certificat
        print("Verification...")
        sender.verify_certificate(system, receiver, certificator.public_key)
        print("")
        print(str(receiver))
        print("")
        print(str(sender))
        print("")
        print(str(certificator))
        print("")
        print(str(message))
        print("")
        main()
    elif ( response == 4 ): # partager la clé secrete
        print("Generation et partage de la clé...")
        sender.p = generate_safe_prime(512, 'Rabin-Miller') # on génére un premier cryptographiquement sécurisé de 512 bits
        sender.g = generate_generator(sender.p) # on génére un élement générateur à partir de ce premier
        sender.a = secrets.SystemRandom().randrange(2,sender.p-2) # Sender choisi un a au hasard entre 2 et p -2
        receiver.b = secrets.SystemRandom().randrange(2,sender.p-2) # Receiver choisi un b au hasard entre 2 et p -2
        sender.A = pow(sender.g , sender.a, sender.p) # Sender calcule A = g^a [p]
        sender.send_difie_hellman_params(receiver) # Sender envoie g, P, A au receiver
        receiver.set_private_key(sender.A, sender.p) # Receiver peut donc calculer B = g^b [p] et definir sa clé secrète à K = A^b [p]
        receiver.send_B_and_set_private_key(sender) # Receiver envoie B a Sender qui a son tour peut calculer sa clef secrète K = B^a [p]

        print("")
        print(str(sender))

        print("")
        print(str(receiver))
        print("")

        main()
    elif ( response == 5 ): # chiffrer un message
        read_mode = prompt.integer(prompt="Voulez vous le mode Texte (1) ou Fichier Binaire (2) ? : ")
        if ( read_mode == 1 ):
            encrypt_fonction("text")
        elif ( read_mode == 2 ):
            encrypt_fonction("binary")
        print("")
        print(str(receiver))
        print("")
        print(str(sender))
        print("")
        print(str(certificator))
        print("")
        print(str(message))
        print("")
        main()
    elif ( response == 6 ): # signer un message
        sender.sign(message,system)

        print("")
        print(str(receiver))
        print("")
        print(str(sender))
        print("")
        print(str(certificator))
        print("")
        print(str(message))
        print("")

        main()
    elif ( response == 7 ):  # verifier la signature du message
        receiver.verify_signature(message, sender)
        main()
    elif ( response == 8 ): # Toutes les étapes du programme
        params_tab = DSA_generate_params(1024, 160, 'Rabin-Miller')
        system.p = params_tab['p']
        system.q = params_tab['q']
        system.g = params_tab['g']
        print("P :")
        print(system.p)
        print("Q :")
        print(system.q)
        key_tab = generate_public_private_keys_asymetric_dsa(system.p, system.q, system.g)
        certificator.public_key = key_tab['public_key']
        certificator.private_key = key_tab['private_key']
        key_tab_receiver = generate_public_private_keys_asymetric_dsa(system.p,system.q,system.g)
        receiver.private_key =  key_tab_receiver['private_key']
        receiver.public_key = key_tab_receiver['public_key']
        key_tab_sender = generate_public_private_keys_asymetric_dsa(system.p,system.q,system.g)
        sender.private_key =  key_tab_sender['private_key']
        sender.public_key = key_tab_sender['public_key']


        # Écriture des clef dans des fichiers

        certificator_public_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Certificator\public_key.dat", "wb")  # destination file for writing (w)b
        certificator_public_key_record =  certificator.public_key.to_bytes(128, byteorder ='big', signed=False)
        certificator_public_key_file.write(certificator_public_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             certificator_public_key_file.write(tag_record)
        certificator_public_key_file.close()

        certificator_private_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Certificator\private_key.dat", "wb")  # destination file for writing (w)b
        certificator_private_key_record =  certificator.private_key.to_bytes(20, byteorder ='big', signed=False)
        certificator_private_key_file.write(certificator_private_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             certificator_private_key_file.write(tag_record)
        certificator_private_key_file.close()

        sender_public_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Sender\public_key.dat", "wb")  # destination file for writing (w)b
        sender_public_key_record = sender.public_key.to_bytes(128, byteorder ='big', signed=False)
        sender_public_key_file.write(sender_public_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             sender_public_key_file.write(tag_record)
        sender_public_key_file.close()

        sender_private_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Sender\private_key.dat", "wb")  # destination file for writing (w)b
        sender_private_key_record = sender.private_key.to_bytes(20, byteorder ='big', signed=False)
        sender_private_key_file.write(sender_private_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             sender_private_key_file.write(tag_record)
        sender_private_key_file.close()

        receiver_public_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Receiver\public_key.dat", "wb")  # destination file for writing (w)b
        receiver_public_key_record = receiver.public_key.to_bytes(128, byteorder ='big', signed=False)
        receiver_public_key_file.write(receiver_public_key_record)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             receiver_public_key_file.write(tag_record)
        receiver_public_key_file.close()

        receiver_private_key_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Receiver\private_key.dat", "wb")  # destination file for writing (w)b
        receiver_private_key_record = receiver.private_key.to_bytes(20, byteorder ='big', signed=False)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             receiver_private_key_file.write(tag_record)
        receiver_private_key_file.write(receiver_private_key_record)
        receiver_private_key_file.close()



        receiver.certificate = certificator.sign_with_private_key(receiver.public_key,system)
        print(receiver.certificate)
        receiver_certificate_file = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\Certificator\certificate.pem", "wb")  # destination file for writing (w)b
        certificator_record_s1 = receiver.certificate[0].to_bytes(128, byteorder ='big', signed=False)
        certificator_record_s2 = receiver.certificate[1].to_bytes(128, byteorder ='big', signed=False)
        certificator_record_hash = receiver.certificate[2].to_bytes(128, byteorder ='big', signed=False)
        receiver_certificate_file.write(certificator_record_s1)
        receiver_certificate_file.write(certificator_record_s2)
        receiver_certificate_file.write(certificator_record_hash)
        for _ in range(128):
             tag_record = secrets.randbits(128).to_bytes(16, byteorder ='big', signed=False)
             receiver_certificate_file.write(tag_record)
        receiver_certificate_file.close()

        print("Verification...")
        sender.verify_certificate(system, receiver, certificator.public_key)

        print("Generation et partage de la clé...")
        sender.p = generate_safe_prime(512, 'Rabin-Miller') # on génére un premier cryptographiquement sécurisé de 512 bits
        sender.g = generate_generator(sender.p) # on génére un élement générateur à partir de ce premier
        sender.a = secrets.SystemRandom().randrange(2,sender.p-2) # Sender choisi un a au hasard entre 2 et p -2
        receiver.b = secrets.SystemRandom().randrange(2,sender.p-2) # Receiver choisi un b au hasard entre 2 et p -2
        sender.A = pow(sender.g , sender.a, sender.p) # Sender calcule A = g^a [p]
        sender.send_difie_hellman_params(receiver) # Sender envoie g, P, A au receiver
        receiver.set_private_key(sender.A, sender.p) # Receiver peut donc calculer B = g^b [p] et definir sa clé secrète à K = A^b [p]
        receiver.send_B_and_set_private_key(sender) # Receiver envoie B a Sender qui a son tour peut calculer sa clef secrète K = B^a [p]

        read_mode = prompt.integer(prompt="Voulez vous le mode Texte (1) ou Fichier Binaire (2) ? : ")
        if ( read_mode == 1 ):
            encrypt_fonction("text")
        elif ( read_mode == 2 ):
            encrypt_fonction("binary")

        sender.sign(message,system)
        receiver.verify_signature(message, sender)



        main()
    elif ( response == 9 ):
        print ("Fin")
    else:
        main()



print('  ____ ____  _ ____                                              _           _   _                          __ _                          ')
print(' / ___/ ___|/ | ___|    ___ ___  _ __ ___  _ __ ___  _   _ _ __ (_) ___ __ _| |_(_) ___  _ __    ___  ___  / _| |___      ____ _ _ __ ___ ')
print('| |  _\\___ \\| |___ \\   / __/ _ \\| \'_ ` _ \\| \'_ ` _ \\| | | | \'_ \\| |/ __/ _` | __| |/ _ \\| \'_ \  / __|/ _ \\| |_| __\\ \\ /\ / / _` | \'__/ _ \\')
print('| |_| |___) | |___) | | (_| (_) | | | | | | | | | | | |_| | | | | | (_| (_| | |_| | (_) | | | | \__ \ (_) |  _| |_ \ V  V / (_| | | |  __/')
print(' \____|____/|_|____/   \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|_|\___\__,_|\__|_|\___/|_| |_| |___/\___/|_|  \__| \_/\_/ \__,_|_|  \___|')
print()
message = Message(value = 0, signature = 0)
system = System(p = 0, q = 0, g = 0)
sender = Sender(private_key = 0, public_key_certificator = 0)
receiver = Receiver(private_key = 0, public_key = 0, certificate = 0)
certificator = Certificator(private_key = 0, public_key = 0)

main() #programme principal