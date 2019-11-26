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

from gmpy2 import xmpz, to_binary, invert, powmod, is_prime

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
    #print (hex(x))
    #print("0x{:02x}".format(x))
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
    #print(line)
    #print(column)

    return dict[line][column]


#01 112 130  44 236 179  39 192 229 228 133  87  53 234  12 174  65
#10:  35 239 107 147  69  25 165  33 237  14  79  78  29 101 146 189
#20: 134 184 175 143 124 235  31 206  62  48 220  95  94 197  11  26
#30: 166 225  57 202 213  71  93  61 217   1  90 214  81  86 108  77
#40: 139  13 154 102 251 204 176  45 116  18  43  32 240 177 132 153
#50: 223  76 203 194  52 126 118   5 109 183 169  49 209  23   4 215
#60:  20  88  58  97 222  27  17  28  50  15 156  22  83  24 242  34
#70: 254  68 207 178 195 181 122 145  36   8 232 168  96 252 105  80
#80: 170 208 160 125 161 137  98 151  84  91  30 149 224 255 100 210
#90:  16 196   0  72 163 247 117 219 138   3 230 218   9  63 221 148
#a0: 135  92 131   2 205  74 144  51 115 103 246 243 157 127 191 226
#b0:  82 155 216  38 200  55 198  59 129 150 111  75  19 190  99  46
#c0: 233 121 167 140 159 110 188 142  41 245 249 182  47 253 180  89
#d0: 120 152   6 106 231  70 113 186 212  37 171  66 136 162 141 250
#e0: 114   7 185  85 248 238 172  10  54  73  42 104  60  56 241 164
#f0:  64  40 211 123 187 201  67 193  21 227 173 244 119 199 128 158




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

    # print(" F_OUT  = " )
    # print(bin(F_OUT).zfill(64))
    # print( F_OUT.bit_length() )

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
                #initialisation
                block_size = 16
                encrypted_text = ""
                text_to_cipher_block = []
                encrypted_text_int_list = []
                decrypted_text_int_list = []
                text_to_cipher_complete = complete(text_to_cipher)
                block_amount = calculate_block_amount( len(text_to_cipher_complete) )
                #chiffrement
                for i in range( block_amount ):
                    text_to_cipher_block.append( text_to_cipher_complete[ (block_size*i) : ( block_size*(i+1) ) ])  # on selectionne le kloc situé aux indices [0:16] [16:32]...
                    text_to_cipher_int = int(  text_to_cipher_block[i].encode().hex(), 16  )
                    encrypted_text_int = encrypt( text_to_cipher_int , kw, ke, k ) # on chiffre ce block
                    encrypted_text_int_list.append( encrypted_text_int )    # on l'ajoute à une liste
                print(encrypted_text_int_list)
                #dechiffrement
                for i in range( block_amount ):
                    encrypted_text = encrypted_text_int_list[i]
                    decrypted_text_int = decrypt( encrypted_text , kw, ke, k ) # on déchiffre le bloc
                    decrypted_text_int_list.append( decrypted_text_int  )
                #Affichage résultat
                print ()
                print( "Texte clair (hex) : ")
                for i in range( block_amount ):
                    print( text_to_cipher_block[i].encode().hex()  )
                print ( )
                print( "Texte chiffré (hex) : ")
                for i in range( block_amount ):
                    print( hex(encrypted_text_int_list[i]) )
                print ()
                print( "Texte déchiffré (hex) : ")
                for i in range( block_amount ):
                     print( hex( decrypted_text_int_list[i] ) )
                print ()
                main()
        elif ( response_encryption == 2 ): #Cipher Block Chaining
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                #preparation des sous-clefs
                if ( key_lenght == 1 ): # 128 bits
                    key_schedule_tab = key_schedule(private_key,128)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 2 ): # 192 bits
                    key_schedule_tab = key_schedule(private_key,192)
                    k = key_schedule_tab['k']
                    ke = key_schedule_tab['ke']
                    kw = key_schedule_tab['kw']
                elif ( key_lenght == 3 ):  # 256 bits
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
                main()
        elif(response_encryption == 3): # Propagated Cipher Block Chaining
            private_key = generate_private_keys_symetric()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
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
                main()
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
                main()

        elif ( response_encryption == 2 ): #Cipher Block Chaining

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
                main()
        elif ( response_encryption == 3 ): #Propagated Cipher Block Chaining

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
                main()




def generate_private_keys_symetric():

    """Voir le TD correspondant"""

    private_key = 0x0123456789abcdeffedcba9876543210
    return {'private_key': private_key }


def generate_p_q(L, N):
    g = N  # g >= 160
    n = (L - 1) // g
    b = (L - 1) % g
    while True:
        # generate q
        while True:
            s = xmpz(randrange(1, 2 ** (g)))
            a = sha1(to_binary(s)).hexdigest()
            zz = xmpz((s + 1) % (2 ** g))
            z = sha1(to_binary(zz)).hexdigest()
            U = int(a, 16) ^ int(z, 16)
            mask = 2 ** (N - 1) + 1
            q = U | mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            V = []
            for k in range(n + 1):
                arg = xmpz((s + j + k) % (2 ** g))
                zzv = sha1(to_binary(arg)).hexdigest()
                V.append(int(zzv, 16))
            W = 0
            for qq in range(0, n):
                W += V[qq] * 2 ** (160 * qq)
            W += (V[n] % 2 ** b) * 2 ** (160 * n)
            X = W + 2 ** (L - 1)
            c = X % (2 * q)
            p = X - c + 1  # p = X - (c - 1)
            if p >= 2 ** (L - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1

def generate_probable_prime_pair_for_DSA(L ,N , seedlen, test_method):

    outlen = 256
    V = []
    W = 0

    """ Je dois demander au prof si on doit respecter ce truc
    if ( (L , N) != (1024, 160) and (L , N) != (2048, 224) and (L , N) != (2048, 256) and ( L , N) != (3072, 160)  ):
        return "invalid ( L,N ) pair"
    """

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
            U = pow( int(hashlib.sha256( (domain_name_seed ).to_bytes(seedlen, byteorder='big') ).hexdigest(), 16), 1 , 2**(N-1) )
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

    """Calcul de p, q, g par persone pour DSA, recomandation avec L=3072 et N = 256
        test_method = 'Rabin-Miller' , 'Fermat', 'Eratosthene'
    """

    """ methode naive

    q = generate_prime_number(N_lenght,test_method) # on trouve un q premier de n bits
    print('Flag 1')
    p = generate_prime_number(L_lenght,test_method) # on trouve un p premier de L bits
    print('Flag 2')
    while ( pow(p-1, 1, q) != 0 ): #tel que p-1 est un multiple de q
        print('Flag 3')
        p = generate_prime_number(L_lenght, test_method)
    """
    #p_q_pair = generate_probable_prime_pair_for_DSA(L_lenght, N_lenght, 256, test_method)
    p_q_pair = generate_p_q(1024,256)
    (p, q) = p_q_pair
    print(p)
    print(q)
    h = secrets.SystemRandom().randrange(2,p-2) #tel que p-1 est un est un multiple de q
    g = pow( h , (p-1) / q, p) # g = h **(p-1) / q [p]
    print(p)
    print(q)
    print(g)
    return {'p': p,'q': q,'g': g }




def generate_random_number_for_primality_test(bit_length):

    """
    Génere un entier d'une suite de bits, typiquement dans notre implementation
    entre 512 bits (bit de poid fort) et 512 + (1 + 2 + 4 + 8 +....) = 1023 bits

    on applique un masque pour ne garder que les impaires

    """

    h = secrets.randbits(bit_length)
    h = h | ( (1 << bit_length - 1) | 1)
    return h


def generate_prime_number(bit_length, test_method): #test method = 'Rabin-Miller', 'Fermat', 'eratostene'
    """
    On se propose de tester la primalité du nombre aléatoire spécifique généré dans la méthode ci-dessus

    """
    p = 4 # par definition, 0 et 1 ne sont pas premier, 3 et 2 non plus
    while not is_prime(p, test_method):
        p = generate_random_number_for_primality_test(bit_length)
    return p


def generate_public_private_keys_asymetric(p, q , g):

    """on retourne x,y a partir du set de parametre p, q, g"""

    """On genere un entier aléatoire x dans [1,q-1]"""
    x = secrets.SystemRandom.randrange(1,q-1)
    y = (g**x) % p



    private_key = 0x0123456789abcdeffedcba9876543210
    return {'private_key': private_key }

def rotate_left(val, r_bits, max_bits):

    """fonctionne correctement à présent"""

    return (val << r_bits%max_bits) & (2**max_bits-1) | ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def super_prime_generator():
    n = 2 ** 512
    while ( not( isPrime(n, 'Rabin-Miller' ) and isPrime( 2*n-1, 'Rabin-Miller' ) ) ) :
        n = n + 1
    return n







def is_prime(number, method):

    """Regler k le nombre d'iteration de rabin miller"""

    if method == ('Eratostene'): #cf NF04
        return eratostene_2(number)
    elif method == ('Fermat'):
        return fermat(number)
    elif method == ('Rabin-Miller'):
        return rabinMiller(number,256)


def eratostene(number):
    list = [False,False] + [True]*(number-1)
    list[2::2] = [False]*(number // 2) # on élimine déjà tous les nombres pairs
    primeList = [2] # 2 est un nombre premier
    racine = int(math.sqrt(number))
    racine = racine + [1,0][racine%2] # pour que racine soit impaire
    for i in range(3,racine+1,2):
        if list[i]:
            primeList.append(i)
            list[i::i] = [False]*(number // i) # on élimine i et ses multiples
    return primeList + [i for i in range(racine,number+1,2) if list[i]]


def eratostene_2(n): # ma version du crible d'eratostene
    if n == 1:
        return False
    d = 2
    while d**2 <= n and n%d!=0:
        d = d+1
    if d**2 > n:
        return n
    else:
        return d


def fermat(number):
    a = random.randint(1,number)
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
        s += 1
        r //= 2
    # fait k tests...
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True




def key_schedule(K, key_length):
    # print(" K = " )
    # print( K.bit_length() )
    # print(bin(K).zfill(128))

    if ( key_length ) == 128:

        KL = K
        KR = 0

    elif ( key_length ) == 192:

        print("FLAG 1")

        KL = K >> 64

        print(" KL = " )
        print(bin(KL).zfill(64))
        print( KL.bit_length() )


        KR = ((K & MASK64) << 64) | (~(K & MASK64))& MASK64

        print(" KR = " )
        print(bin(KR).zfill(64))
        print( KR.bit_length() )

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

        print("FLAG 2")

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
    return encrypt(C, kw2, ke2, k2 )



class Certificator:

  def __init__(self, PublicKey, privateKey):
    self.publicKey = publicKey
    self.privateKey = privateKey

  def signPrivc(publicKeyS):
    print(" Site public_key signed" )

class Alice:

  def __init__(self, certificatorPublicKey, privateKey):
    self.certificatorPublicKey = certificatorPublicKey
    self.privateKey = privateKey

  def sign(public_key):
    print(" Site public_key signed" )

  def requestPublicKey(certificator):
    self.certificatorPublicKey = certificator.publicKey

  def verifyCertificates(Bob):
      print('OK')

class Bob:

  def __init__(self, privateKey, private_key, certificate):

    self.publicKey = publicKey
    self.privateKey = privateKey
    self.certificate = certificate

  def sign(publicKeyS, certificator):

    return certificator.signPrivc(publicKeyS)




def main(): #programme principal
    print('  ____ ____  _ ____                                              _           _   _                          __ _                          ')
    print(' / ___/ ___|/ | ___|    ___ ___  _ __ ___  _ __ ___  _   _ _ __ (_) ___ __ _| |_(_) ___  _ __    ___  ___  / _| |___      ____ _ _ __ ___ ')
    print('| |  _\\___ \\| |___ \\   / __/ _ \\| \'_ ` _ \\| \'_ ` _ \\| | | | \'_ \\| |/ __/ _` | __| |/ _ \\| \'_ \  / __|/ _ \\| |_| __\\ \\ /\ / / _` | \'__/ _ \\')
    print('| |_| |___) | |___) | | (_| (_) | | | | | | | | | | | |_| | | | | | (_| (_| | |_| | (_) | | | | \__ \ (_) |  _| |_ \ V  V / (_| | | |  __/')
    print(' \____|____/|_|____/   \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|_|\___\__,_|\__|_|\___/|_| |_| |___/\___/|_|  \__| \_/\_/ \__,_|_|  \___|')
    print()
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


    if ( response == 1 ):

        print('OK')

    elif ( response == 2 ):


        main()
    elif ( response == 3 ):
        print ("3")
        main()
    elif ( response == 4 ):
        print ("4")
        main()
    elif ( response == 5 ):
        read_mode = prompt.integer(prompt="Voulez vous le mode Texte (1) ou Fichier Binaire (2) ? : ")
        if ( read_mode == 1 ):
            encrypt_fonction("text")
        elif ( read_mode == 2 ):
            encrypt_fonction("binary")
    elif ( response == 6 ):
        print ("6")
        main()
    elif ( response == 7 ):
        print ("7")
        main()
    elif ( response == 8 ):
        print ("8")
        main()
    elif ( response == 9 ):
        #rint( super_prime_generator() )
        print ("Fin")
    else:
        main()





main() #programme principal