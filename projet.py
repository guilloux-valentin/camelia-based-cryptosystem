import os, prompt, secrets, string

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

def generate_keys():
    private_key = 0x0123456789abcdeffedcba9876543210
    public_key = 0
    return {'private_key': private_key, 'public_key': public_key }

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def rotate_left(n,d,tot_bits): #This function is used to rotate the number n by d bits in the left direction
    result = (n << d) | (n >> (tot_bits - d))
    return result


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
    D1 = FL   (D1, ke[1-1])     // FL
    D2 = FLINV(D2, ke[2-1])     // FLINV
    D2 = D2 ^ F(D1, k[7-1])     # Round 7
    D1 = D1 ^ F(D2, k[8-1])     # Round 8
    D2 = D2 ^ F(D1, k[9-1])     # Round 9
    D1 = D1 ^ F(D2, k[10-1])    # Round 10
    D2 = D2 ^ F(D1, k[11-1])    # Round 11
    D1 = D1 ^ F(D2, k[12-1])    # Round 12
    D1 = FL   (D1, ke[3-1])     // FL
    D2 = FLINV(D2, ke[4-1])     // FLINV
    D2 = D2 ^ F(D1, k[13-1])    # Round 13
    D1 = D1 ^ F(D2, k[14-1])    # Round 14
    D2 = D2 ^ F(D1, k[15-1])    # Round 15
    D1 = D1 ^ F(D2, k[16-1])    # Round 16
    D2 = D2 ^ F(D1, k[17-1])    # Round 17
    D1 = D1 ^ F(D2, k[18-1])    # Round 18
    D2 = D2 ^ kw[3-1]           # Postwhitening
    D1 = D1 ^ kw[4-1]
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
        src = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\message.dat", "rb") # source file for reading (r)b
        dst = open(r"C:\Users\val-r\OneDrive\Documents\Python Scripts\camelia-based-cryptosystem\cipher.dat", "wb")  # cipher destination file for writing (w)b
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
                try:

                    record = src.read( 16 ) # Read a record from source file
                                            # 16 Bytes (octet) = 128 bit (M length)
                    while record :
                        print( record )
                        #k = key_schedule(private_key,128)[k]
                        #ke = key_schedule(private_key,128)[ke]
                        #kw = key_schedule(private_key,128)[kw]
                        #encypted_record = encrypt( record, k, ke, kw )
                        dst.write( record )
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
                    print( record )
                    record = byte_xor(initialization_vector,record)
                    while record :
                        print( record )
                        #k = key_schedule(private_key,128)[k]
                        #ke = key_schedule(private_key,128)[ke]
                        #kw = key_schedule(private_key,128)[kw]
                        #encypted_record = encrypt( record, k, ke, kw )
                        dst.write( encypted_record )

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
                        print( record )
                        #k = key_schedule(private_key,128)[k]
                        #ke = key_schedule(private_key,128)[ke]
                        #kw = key_schedule(private_key,128)[kw]
                        encypted_record = encrypt( first_xor, k, ke, kw )
                        first_xor = byte_xor( record,encypted_record )
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
            print ("Fin")
    else:
        main()


main() #programme principal

#RoadMap

#key_schedule(K): #return Ka,Kb,Kr,Kl,ke,k,kw
#encrypt(M,D1,D2): #return cipher


##TODO:

#feistel(fin,Ke): #return fout
#sbox(num,SBoxinput)
#feistel_inv()





#def fileOperation(mode,action):



