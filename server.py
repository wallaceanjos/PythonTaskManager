import socket
import time
import os
import pickle
import psutil
import platform
import cpuinfo


# Atribuições
cpuFreq = psutil.cpu_freq()
cpuCores = psutil.cpu_count()
cpuPhyCores = psutil.cpu_count(logical=False)
infoCpu = cpuinfo.get_cpu_info()
wordCpu = platform.architecture()

cpuBrand = f'Processador: {infoCpu["brand_raw"]} {(str(cpuCores))} Núcleos, com  {str(cpuPhyCores)} núcleos físicos e {str(int(cpuCores - cpuPhyCores))} núcleos lógicos.'
cpuArch = f'{infoCpu["arch"]} / Palavra do CPU {str(wordCpu[0])}'
netConfig = psutil.net_if_addrs()
cpuPercent = psutil.cpu_percent(interval=1, percpu=True)
memRam = psutil.virtual_memory()
disk = psutil.disk_usage('.')
diskPercent = disk.percent
files = os.path.abspath(os.getcwd())
cputasks = len(psutil.pids())
interfaces = psutil.net_if_addrs()
interfaces_nome = []
for i in interfaces:
    interfaces_nome.append(str(i))


info1 = f'Consumo da CPU {cpuPercent[0]}% '
info2 = f'Consumo de Memória {memRam[2]}% '
info3 = f'Consumo de Disco {diskPercent}% '
info4 = f'Diretório do servidor {files} '
info5 = f'CPU Brand {cpuBrand} '
info6 = f'CPU Cores {(str(cpuCores))} '
info7 = f'Arquitetura do CPU {cpuArch} '
info8 = f'Tarefas em execução {cputasks} '
info9 = f'Processos usando a Rede '
info10 = interfaces_nome

print(info1)
print(info2)
print(info3)
print(info4)
print(info5)
print(info6)
print(info7)
print(info8)
print(info9)
print(info10)

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    d = [info1, info2, info3, info4, info5, info6, info7, info8, info9, info10]
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    print(msg)
    clientsocket.send(msg)
