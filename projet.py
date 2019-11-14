import os, prompt, secrets, string, codecs, sys, base64, random

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

        return(SBOX1(x))

def SBOX3(x):
        return rotate_left(SBOX1(x),7,8)

def SBOX4(x):

        return SBOX1(rotate_left(x,1,64))


def SBOX1(x):
    #print('SBOX1')
    #print(list(hex(x)))
    #line = list(hex(x))[2]
    #column = list(hex(x))[3]
    dict =     {'0' : {     '0': 112,   '1' : 130,  '2' : 44,   '3' : 236,  '4' : 179,  '5' : 39,   '6' : 192,  '7':229,    '8':228,    '9':133,   'a':87,     'b':53,     'c':234,    'd': 12,    'e':174,    'f':65},
                '1' : {     '0': 35,    '1' : 239,  '2' : 107,  '3' : 147,  '4' : 69,   '5' : 25,   '6' : 165,  '7':33,     '8':237,    '9':14,    'a':79,     'b':78,     'c':29,     'd': 101,   'e':146,    'f':189},
                '2' : {     '0': 134,   '1' : 184,  '2' : 175,  '3' : 143,  '4' : 124,  '5' : 235,  '6' : 31,   '7':206,    '8':62,     '9':48,    'a':220,    'b':95,     'c':94,     'd': 197,   'e':11,     'f':26},
                '3' : {     '0': 166,   '1' : 225,  '2' : 57,   '3' : 202,  '4' :213, '  5' : 71,   '6' : 93,   '7':61,     '8':217,    '9':1,     'a':90,     'b':214,    'c':81,     'd': 86,    'e':108,    'f':77},
                '4' : {     '0': 139,   '1' : 13,   '2' : 154,  '3' : 102,  '4' :251,   '5' : 204,  '6' : 176,  '7':45,     '8':116,    '9':18,    'a':43,     'b':32,     'c':240,    'd': 177,    'e':132,    'f':153},
                '5' : {     '0': 223,   '1' : 76,   '2' : 203,  '3' : 194,  '4' :52,    '5' : 126,  '6' : 118,  '7':5,      '8':109,    '9':183,   'a':169,    'b':49,     'c':209,    'd': 23,    'e':4,    'f':215},
                '6' : {     '0': 20,    '1' : 88,   '2' : 58,   '3' : 97,   '4' :222,   '5' : 27,   '6' : 17,   '7':28,     '8':50,     '9':15,    'a':156,    'b':22,     'c':83,     'd': 24,    'e':242,    'f':34},
                '7' : {     '0': 254,   '1' : 68,   '2' : 207,  '3' : 178,  '4' :195,   '5' : 181,  '6' : 122,  '7':145,    '8':36,     '9':8,     'a':232,    'b':168,    'c':86,     'd': 252,    'e':105,    'f':80},
                '8' : {     '0': 170,   '1' : 208,  '2' : 160,  '3' : 125,  '4' :161,   '5' : 137,  '6' : 98,   '7':151,    '8':84,     '9':91,    'a':30,     'b':149,    'c':224,    'd': 255,    'e':100,    'f':210},
                '9' : {     '0': 16,    '1' : 196,  '2' : 0,    '3' : 72,   '4' :163,   '5' : 247,  '6' : 117,  '7':219,    '8':138,    '9':3,     'a':230,    'b':243,    'c':9,      'd': 63,    'e':221,    'f':148},
                'a' : {     '0': 135,   '1' : 92,   '2' : 131,  '3' : 2,    '4' :205,   '5' : 74,   '6' : 144,  '7':51,     '8':115,    '9':103,   'a':246,    'b':75,     'c':157,    'd': 127,    'e':191,    'f':226},
                'b' : {     '0': 82,    '1' : 155,  '2' : 216,  '3' : 38,   '4' :200,   '5' : 55,   '6' : 198,  '7':59,     '8':129,    '9':150,   'a':111,    'b':182,    'c':19,     'd': 190,    'e':99,    'f':646},
                'c' : {     '0': 223,   '1' : 121,  '2' : 167,  '3' : 140,  '4' :159,   '5' : 110,  '6' : 188,  '7':142,    '8':41,     '9':245,   'a':249,    'b':66,     'c':47,     'd': 253,    'e':180,    'f':89},
                'd' : {     '0': 120,   '1' : 152,  '2' : 6,    '3' : 106,  '4' :231,   '5' : 70,   '6' : 113,  '7':186,    '8':212,    '9':37,    'a':171,    'b':104,    'c':136,    'd': 162,    'e':141,    'f':250},
                'e' : {     '0': 114,   '1' : 7,    '2' : 185,  '3' : 85,   '4' :248,   '5' : 238,  '6' : 172,  '7':10,     '8':54,     '9':73,    'a':42,     'b':244,    'c':60,      'd': 56,    'e':241,    'f':164},
                'f' : {     '0': 64,    '1' : 40,   '2' : 211,  '3' : 123,  '4' :187,   '5' : 201,  '6' : 67,   '7':193,    '8':21,     '9':227,   'a':173,    'b':234,    'c':119,    'd': 199,    'e':128,    'f':158},
                }
    #column = str(column)
    #return dict[line][column]
    return 87

#1 112 130  44 236 179  39 192 229 228 133  87  53 234  12 174  65
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




def F(F_IN, KE):
    #print(F_IN,KE)
    x  = F_IN ^ KE
    t1 =  x >> 56
    t2 = (x >> 48) & MASK8
    t3 = (x >> 40) & MASK8
    t4 = (x >> 32) & MASK8
    t5 = (x >> 24) & MASK8
    t6 = (x >> 16) & MASK8
    t7 = (x >>  8) & MASK8
    t8 =  x        & MASK8
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
    y2 = y2 ^ (rotate_left((y1 & k1) ,1,32))
    return (y1 << 32) | y2

def encrypt_fonction(mode):
    if ( mode == "text" ):
        text_to_cipher = prompt.string(prompt="Saisir le texte à chiffrer : ")
        print ("->1<- 128 bits")
        print ("->2<- 192 bits")
        print ("->3<- 256 bits")
        key_lenght = prompt.integer(prompt="Saisir la longeur de la clef : ")
        print ("->1<- ECB Electronic Code Book")
        print ("->2<- CBC Cipher Block Chaining")
        print ("->3<- PCBC Propagated Cipher Block Chaining")
        response_encryption = prompt.integer(prompt="Choisisez votre mode de chiffrement : ")
        if ( response_encryption == 1 ): #Electronic Code Book
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                if ( key_lenght == 1 ): #128 bits
                    k = key_schedule(private_key,128)['k']
                    ke = key_schedule(private_key,128)['ke']
                    kw = key_schedule(private_key,128)['kw']
                elif ( key_lenght == 2 ):
                    k = key_schedule(private_key,192)['k']
                    ke = key_schedule(private_key,192)['ke']
                    kw = key_schedule(private_key,192)['kw']
                elif ( key_lenght == 3 ):
                    k = key_schedule(private_key,256)['k']
                    ke = key_schedule(private_key,256)['ke']
                    kw = key_schedule(private_key,256)['kw']
                encrypted_text = ""
                text_to_cipher = text_to_cipher.encode('utf-8')
                bytes_count = len(text_to_cipher)
                print ( bytes_count )
                text_to_cipher = int.from_bytes(text_to_cipher, byteorder='big')
                encrypted_text = encrypt( text_to_cipher , kw, ke, k )

                encrypted_text = encrypted_text.to_bytes(32, byteorder='big')
                print ()
                print( "Texte chiffré : ")
                print( encrypted_text.hex(' ') )
                print ()
                print( "Base64 : "  )
                print( base64.b64encode(encrypted_text) )
                print ()
                main()
        elif ( response_encryption == 2 ): #Cipher Block Chaining
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                if ( key_lenght == 1 ): #128 bits
                    k = key_schedule(private_key,128)['k']
                    ke = key_schedule(private_key,128)['ke']
                    kw = key_schedule(private_key,128)['kw']
                elif ( key_lenght == 2 ):
                    k = key_schedule(private_key,192)['k']
                    ke = key_schedule(private_key,192)['ke']
                    kw = key_schedule(private_key,192)['kw']
                elif ( key_lenght == 3 ):
                    k = key_schedule(private_key,256)['k']
                    ke = key_schedule(private_key,256)['ke']
                    kw = key_schedule(private_key,256)['kw']

                for i in range (len(text_to_cipher)):
                    encrypted_text[i] = char(encrypt( ord(text_to_cipher[i]) , kw, ke, k ))
                print(encrypted_text)
                main()
                                                                ##TODO
        elif ( response_encryption == 3 ): #Propagated Cipher Block Chaining
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                if ( key_lenght == 1 ): #128 bits
                    k = key_schedule(private_key,128)['k']
                    ke = key_schedule(private_key,128)['ke']
                    kw = key_schedule(private_key,128)['kw']
                elif ( key_lenght == 2 ):
                    k = key_schedule(private_key,192)['k']
                    ke = key_schedule(private_key,192)['ke']
                    kw = key_schedule(private_key,192)['kw']
                elif ( key_lenght == 3 ):
                    k = key_schedule(private_key,256)['k']
                    ke = key_schedule(private_key,256)['ke']
                    kw = key_schedule(private_key,256)['kw']
                for i in range (len(text_to_cipher)):
                    encrypted_text[i] = encrypt( text_to_cipher[i] , kw, ke, k )
                print(encrypted_text)                                                   ##TODO
                main()
    elif ( mode == "binary" ):
        src = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\message.dat", "rb") # source file for reading (r)b
        dst = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\cipher.dat", "wb")  # cipher destination file for writing (w)b
        key_lenght = prompt.integer(prompt="Saisir la longeur de la clef : ")
        print ("->1<- 128 bits")
        print ("->2<- 192 bits")
        print ("->3<- 256 bits")
        response_encryption = prompt.integer(prompt="Choisisez votre mode de chiffrement : ")
        print ("->1<- ECB Electronic Code Book")
        print ("->2<- CBC Cipher Block Chaining")
        print ("->3<- PCBC Propagated Cipher Block Chaining")

        if ( response_encryption == 1 ): #Electronic Code Book
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                try:
                    record = src.read( 16 ) # Read a record from source file
                                            # 16 Bytes (octet) = 128 bit (M length)
                    while record :
                        #print( record )
                        if ( key_lenght == 1 ): #128 bits
                            k = key_schedule(private_key,128)['k']
                            ke = key_schedule(private_key,128)['ke']
                            kw = key_schedule(private_key,128)['kw']
                        elif ( key_lenght == 2 ):
                            k = key_schedule(private_key,192)['k']
                            ke = key_schedule(private_key,192)['ke']
                            kw = key_schedule(private_key,192)['kw']
                        elif ( key_lenght == 3 ):
                            k = key_schedule(private_key,256)['k']
                            ke = key_schedule(private_key,256)['ke']
                            kw = key_schedule(private_key,256)['kw']
                        Message = int.from_bytes(record, byteorder='big')
                        encrypted_message = encrypt( Message, kw, ke, k )
                        encrypted_record = encrypted_message.to_bytes(16, byteorder ='big', signed=False)
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
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                try:
                    #initialization vector is a 16 Byte (16 octet, 128 bit) string
                    initialization_vector = secrets.token_bytes(16)
                    print(initialization_vector)
                    record = src.read( 16 ) # Read a record from source file
                                            # 16 Bytes  = 128 bit (M length)
                    #print( record )
                    record = byte_xor(initialization_vector,record)
                    while record :
                        if ( key_lenght == 1 ): #128 bits
                            k = key_schedule(private_key,128)['k']
                            ke = key_schedule(private_key,128)['ke']
                            kw = key_schedule(private_key,128)['kw']
                        elif ( key_lenght == 2 ):
                            k = key_schedule(private_key,192)['k']
                            ke = key_schedule(private_key,192)['ke']
                            kw = key_schedule(private_key,192)['kw']
                        elif ( key_lenght == 3 ):
                            k = key_schedule(private_key,256)['k']
                            ke = key_schedule(private_key,256)['ke']
                            kw = key_schedule(private_key,256)['kw']
                        Message = int.from_bytes(record, byteorder='big')
                        encrypted_message = encrypt( Message, kw, ke, k )
                        encrypted_record = encrypted_message.to_bytes(16, byteorder ='big', signed=False)
                        dst.write( encrypted_record )
                        record = byte_xor(src.read( 16 ),encrypted_record)
                except IOError:
                    # Your error handling here
                    # Nothing for this example
                    pass
                finally:
                    src.close()
                    dst.close()
                main()
        elif ( response_encryption == 3 ): #Propagated Cipher Block Chaining
            private_key = generate_keys()['private_key']
            try:
                private_key
            except NameError:
                print("La clé n'a pas été définie :")
            else:
                try:
                    initialization_vector = secrets.token_bytes(16) #Return a random byte string containing nbytes number of bytes.
                    record = src.read( 16 ) # Read a record from source file
                                            # 16 Byte (octet) = 128 bit (M length)
                    first_xor = byte_xor(initialization_vector,record)
                    while record :
                        if ( key_lenght == 1 ): #128 bits
                            k = key_schedule(private_key,128)['k']
                            ke = key_schedule(private_key,128)['ke']
                            kw = key_schedule(private_key,128)['kw']
                        elif ( key_lenght == 2 ):
                            k = key_schedule(private_key,192)['k']
                            ke = key_schedule(private_key,192)['ke']
                            kw = key_schedule(private_key,192)['kw']
                        elif ( key_lenght == 3 ):
                            k = key_schedule(private_key,256)['k']
                            ke = key_schedule(private_key,256)['ke']
                            kw = key_schedule(private_key,256)['kw']
                        Message = int.from_bytes(first_xor, byteorder='big')
                        encrypted_message = encrypt( Message, kw, ke, k )
                        encrypted_record = encrypted_message.to_bytes(16, byteorder ='big', signed=False)
                        first_xor = byte_xor( record,encrypted_record )
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


def generate_keys():
    private_key = 0x0123456789abcdeffedcba9876543210
    public_key = 0
    return {'private_key': private_key, 'public_key': public_key }

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def rotate_left(n,d,tot_bits): #This function is used to rotate the number n by d bits in the left direction
    result = (n << d) | (n >> (tot_bits - d))
    return result

def super_prime_generator():
    n = 2 ** 512
    while ( not( isPrime(n, 'Rabin-Miller' ) and isPrime( 2*n-1, 'Rabin-Miller' ) ) ) :
        n = n + 1
    return n




def isPrime(number, method):
    if method == ('Eratostene'): #cf NF04
        if (number in eratostene(number)):
            return True
        else:
            return False
    elif method == ('Fermat'):
        return fermat(number)
    elif method == ('Rabin-Miller'):
        return rabinMiller(number,2)


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

def premier(n):
    if n == 1:
        return False
    d = 2
    while d**2 <= n and n%d!=0:
        d = d+1
    if d**2 > n:
        return n
    else:
        return d


def key_schedule(K, key_length): #K as a 128 bits binary number
    if ( key_length ) == 128:
        KL = K
        KR = 0
    elif ( key_length ) == 192:
        KL = K >> 64
        KR = ((K & MASK64) << 64) | (~(K & MASK64))
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
        kw1 = ( rotate_left(KL,0,192) ) >> 64
        kw2 = ( rotate_left(KL,0,192) ) & MASK64
        k1  = ( rotate_left(KB,0,192) ) >> 64
        k2  = ( rotate_left(KB,0,192) ) & MASK64
        k3  = ( rotate_left(KR,15,192) ) >> 64
        k4  = ( rotate_left(KR,15,192) ) & MASK64
        k5  = ( rotate_left(KA,15,192) ) >> 64
        k6  = ( rotate_left(KA,15,192) ) & MASK64
        ke1 = ( rotate_left(KR,30,192) ) >> 64
        ke2 = ( rotate_left(KR,30,192) ) & MASK64
        k7  = ( rotate_left(KB,30,192) ) >> 64
        k8  = ( rotate_left(KB,30,192) ) & MASK64
        k9  = ( rotate_left(KL,45,192) ) >> 64
        k10 = ( rotate_left(KL,45,192) ) & MASK64
        k11 = ( rotate_left(KA,45,192) ) >> 64
        k12 = ( rotate_left(KA,45,192) ) & MASK64
        ke3 = ( rotate_left(KL,60,192) ) >> 64
        ke4 = ( rotate_left(KL,60,192) ) & MASK64
        k13 = ( rotate_left(KR,60,192) ) >> 64
        k14 = ( rotate_left(KR,60,192) ) & MASK64
        k15 = ( rotate_left(KB,60,192) ) >> 64
        k16 = ( rotate_left(KB,60,192) ) & MASK64
        k17 = ( rotate_left(KL,77,192) ) >> 64
        k18 = ( rotate_left(KL,77,192) ) & MASK64
        ke5 = ( rotate_left(KA,77,192) ) >> 64
        ke6 = ( rotate_left(KA,77,192) ) & MASK64
        k19 = ( rotate_left(KR,94,192) ) >> 64
        k20 = ( rotate_left(KR,94,192) ) & MASK64
        k21 = ( rotate_left(KA,94,192) ) >> 64
        k22 = ( rotate_left(KA,94,192) ) & MASK64
        k23 = ( rotate_left(KL,111,192) ) >> 64
        k24 = ( rotate_left(KL,111,192) ) & MASK64
        kw3 = ( rotate_left(KB,111,192) ) >> 64
        kw4 = ( rotate_left(KB,111,192) ) & MASK64
        kw = [kw1,kw2,kw3,kw4]
        k = [k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17,k18,k19,k20,k21,k22,k23,k24]
        ke = [ke1,ke2,ke3,ke4,ke5,ke6]
    return {'KA': KA, 'KB': KB ,'KR': KR, 'KL' : KL, 'ke' : ke, 'k' : k , 'kw' : kw}

def encrypt(M, kw, ke, k ):
    print(len(k))
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
        D2 = D2 ^ F(D1, k[8-1])
        D1 = D1 ^ F(D2, k[10-1])
        D2 = D2 ^ F(D1, k[11-1])
        D1 = D1 ^ F(D2, k[12-1])
        D1 = FL   (D1, ke[3-1])
        D2 = FLINV(D2, ke[4-1])
        D2 = D2 ^ F(D1, k[13-1])
        D1 = D1 ^ F(D2, k[14-1])5
        D2 = D2 ^ F(D1, k[15-1])
        D1 = D1 ^ F(D2, k[16-1])
        D2 = D2 ^ F(D1, k[17-1])
        D1 = D1 ^ F(D2, k[18-1])
        D1 = FL   (D1, ke[5-1])
        D2 = FLINV(D2, ke[6-1])
        D2 = D2 ^ F(D1, k[19-1])
        D1 = D1 ^ F(D2, k[20-1])
        D2 = D2 ^ F(D1, k[20-1])
        D1 = D1 ^ F(D2, k[22-1])
        D2 = D2 ^ F(D1, k[23-1])
        D1 = D1 ^ F(D2, k[24-1])
        D2 = D2 ^ kw[3-1]
        D1 = D1 ^ kw[4-1]

        #128-bit ciphertext C is constructed from D1 and D2 as follows.

        C = (D2 << 64) | D1

    return C


def decrypt(C, kw, ke, k):
                        #indicies are lowered to minus 1 to improve readability
    if (len(ke) == 4): #128bits key
        kw[1-1], kw[3-1] = kw[3-1], kw[1-1]
        kw[2-1], kw[4-1] = kw[4-1], kw[2-1]
        k[1-1], k[18-1] = k[18-1], k[1-1]
        k[2-1], k[17-1] = k[17-1], k[2-1]
        k[3-1], k[16-1] = k[16-1], k[3-1]
        k[4-1], k[15-1] = k[15-1], k[4-1]
        k[5-1], k[14-1] = k[14-1], k[5-1]
        k[6-1], k[13-1] = k[13-1], k[6-1]
        k[7-1], k[12-1] = k[12-1], k[7-1]
        k[8-1], k[11-1] = k[11-1], k[8-1]
        k[9-1], k[10-1] = k[10-1], k[9-1]
        ke[1-1], ke[4-1] = ke[4-1], ke[1-1]
        ke[2-1], ke[3-1] = ke[3-1], ke[2-1]
    elif (len(ke) == 6): #192-256 bits key
        kw[1-1], kw[3-1] = kw[3-1], kw[1-1]
        kw[2-1], kw[4-1] = kw[4-1], kw[2-1]
        k[1-1], k[24-1] = k[24-1], k[1-1]
        k[2-1], k[23-1] = k[23-1], k[2-1]
        k[3-1], k[22-1] = k[22-1], k[3-1]
        k[4-1], k[21-1] = k[21-1], k[4-1]
        k[5-1], k[20-1] = k[20-1], k[5-1]
        k[6-1], k[19-1] = k[19-1], k[6-1]
        k[7-1], k[18-1] = k[18-1], k[7-1]
        k[8-1], k[17-1] = k[17-1], k[8-1]
        k[9-1], k[16-1] = k[16-1], k[9-1]
        k[10-1], k[15-1] = k[15-1], k[10-1]
        k[11-1], k[14-1] = k[14-1], k[11-1]
        k[12-1], k[13-1] = k[13-1], k[12-1]
        ke[1-1], ke[6-1] = ke[6-1], ke[1-1]
        ke[2-1], ke[5-1] = ke[5-1], ke[2-1]
    return encrypt(C, kw, ke, k )



class Certificator:
  def __init__(self, public_key, private_key):
    self.public_key = public_key
    self.private_key = private_key

  def sign(public_key):
    print(" Site public_key signed" )

class Visitor:
  def __init__(self, public_key, private_key):
    self.public_key = public_key
    self.private_key = private_key

  def sign(public_key):
    print(" Site public_key signed" )


class Site:
  def __init__(self, public_key, private_key):
    self.public_key = public_key
    self.private_key = private_key

  def sign(public_key):
    print(" Site public_key signed" )


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
    response = prompt.integer(prompt="Choisisez votre action : ")
    if ( response == 1 ):
        print(generate_keys())
    elif ( response == 2 ):
        print ("2")
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
        print( super_prime_generator() )
        print ("Fin")
    else:
        main()





main() #programme principal




