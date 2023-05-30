import socket

def scan_ports():
    domain = input("Entrez le nom de domaine à scanner : ")
    start_port = int(input("Entrez le numéro de port de départ : "))
    end_port = int(input("Entrez le numéro de port de fin : "))

    print(f"\nScanning ports for domain: {domain}\n")
    
    # Résolution inverse pour obtenir l'adresse IP du domaine
    ip_address = socket.gethostbyname(domain)
    print(f"IP address for {domain}: {ip_address}\n")
    
    # Boucle sur les numéros de port à scanner
    for port in range(start_port, end_port + 1):
        try:
            # Crée une socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Définit un délai d'attente de 1 seconde
            sock.settimeout(1)
            
            # Tente de se connecter au port
            result = sock.connect_ex((domain, port))
            
            # Si le port est ouvert, affiche un message
            if result == 0:
                service_name = socket.getservbyport(port)
                print(f"Port {port} ({service_name}) is open")
            
            # Ferme la socket
            sock.close()
        
        except socket.error:
            print(f"Couldn't connect to port {port}")
            continue

# Exemple d'utilisation
scan_ports()
