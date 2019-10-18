import os, prompt


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
            print ("1")
            main()
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
            print ("5")
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