from fileTerminalInterface import FileInterface
import socket
import os
import tqdm

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
DATA = "<DATA>"

fileInterface = FileInterface()

serverSocket = socket.socket()
serverSocket.bind((SERVER_HOST,SERVER_PORT))

serverSocket.listen(5)
print(f"[*] Escutando como {SERVER_HOST}:{SERVER_PORT}")

client_socket, adress = serverSocket.accept()
print(f"[+] {adress} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
command,data = received.split(DATA)

print(f"[-] Commando Recebido:{command}")

if int(command) == 0:
    string = fileInterface.showFilesNames()
    client_socket.send(string.encode('utf-8'))

else:
    serverSocket.close()
    client_socket.close()

fileName = client_socket.recv(BUFFER_SIZE).decode('utf-8')
print(f"[+] {adress} requests {fileName}")
fileAdress = fileInterface.getFileAdress(fileName)

if fileAdress == f"{fileName} não existe no nosso banco de dados":
    print(f"[*] O arquivo {fileName} não esta disponivel no nosso banco")
    client_socket.send(fileAdress.encode('utf-8'))

else:
    fileSize = os.path.getsize(fileAdress)
    client_socket.send(f"{fileName}{SEPARATOR}{fileSize}".encode('utf-8'))
    progress = tqdm.tqdm(
        range(fileSize),
        f"enviando {fileName}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024
    )

    with open(fileAdress,"rb") as f:
        for _ in progress:
        #Lê os bytes do arquivo
            bytes_read = f.read(BUFFER_SIZE)

            if not bytes_read:
            #Final da transmissão
                break
        
            client_socket.sendall(bytes_read)
            progress.update(len(bytes_read))


serverSocket.close()
client_socket.close()
