import os, prompt, math

def euclide(numberA,numberB):
    return (numberA // numberB, numberA%numberB)

def euclideExpanded(numberA,numberB):
    return

def fastExponentiation(numberA,numberB):
    return

def chinesseRemain(matrixA,matrixB):
    return

def primeFactorDecomposition(numberA):
    return (numberA // numberB, numberA%numberB)

def euleurFonction(numberA):
    return

def isPrime(number, method):
    if method == ('Eratostene'): #cf NF04
        if (number in eratostene(number)):
            return True
        else:
            return False
    elif method == ('Fermat'):
        return fermat(number)
    elif method == ('Rabin-Miller'):
        return rabinMiller(number,100)


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

##CT : O(sqrt(n))

def plus_petit_diviseur_premier(n):
    for i in range (2,(n//2)+1):
        if (premier(i)==True) and (n%i==0):
             return i

print(plus_petit_diviseur_premier(6))

def factoris_premier(n):
    i = 2
    l = []
    résultat = 1
    résultat2 = 1
    while résultat < n:
        if premier(i) == True:
            résultat = résultat * i
            if résultat <= n//2:
                l.append(i)
            elif résultat < n and résultat > n//2:
                i = i + 1
                l.append(i)
            else:
                i = i + 1
        else:
            i = i + 1
    for j in range (len(l)):
        résultat2 = résultat2 * (l[j])
    if résultat2 == n:
        return l



def factor(n):
    l = []
    nombre = n
    while nombre != 1:
        l.append(premier(nombre))
        nombre = (nombre)//(premier(nombre))
    return l

print(factor(172))



print(isPrime(14897,'Fermat'))
