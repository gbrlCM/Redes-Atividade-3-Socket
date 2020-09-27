import socket
from fileInterfaceClientSide import generateInterfaceString
import tqdm
import os


SEPARATOR = "<SEPARATOR>"
DATA = "<DATA>"
BUFFER_SIZER = 4096 #envia 4096 bytes a cada passo

#Config do Server
host = "172.25.164.188"
port = 5002

s = socket.socket()
print(f"[+] Conectando em: {host}:{port}")
s.connect((host, port))
print("[+] Conectado")

#Recebendo que está pronto para receber a lista de dados
s.send(f"0{DATA}".encode())
data = s.recv(BUFFER_SIZER).decode('utf-8')
arr = data.split(DATA)
generateInterfaceString(arr)

#Enviando que nome do arquivo que ira receber
fileName = input("Digite o numero do arquivo que voce quer receber: ")
s.send(f"{fileName}".encode('utf-8'))

data = s.recv(BUFFER_SIZER).decode('utf-8')

if data == f"{fileName} não existe no nosso banco de dados":
    print(data)

else:
    fileName, fileSize = data.split(SEPARATOR)
    fileName = os.path.basename(fileName)
    fileSize = int(fileSize)

    progress = tqdm.tqdm(
        range(fileSize),
        f"Recebendo {fileName}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024
    )

    with open(fileName, "wb") as f:
        for _ in progress:
        #Lê 1024 bytes recebindo pelo socket
            bytes_read = s.recv(BUFFER_SIZER)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))


s.close()

