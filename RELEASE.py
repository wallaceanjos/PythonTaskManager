import psutil
import platform
import cpuinfo
import pygame
import random
import time
import os
import subprocess
import socket
import sys
import nmap
import threading
import socket
import pickle

HEADERSIZE = 10
# import schedule

procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
procs_list = []

pygame.init()

# ================== CPU
# Instâncias
cpuFreq = psutil.cpu_freq()
cpuCores = psutil.cpu_count()
cpuPhyCores = psutil.cpu_count(logical=False)
percentage = psutil.cpu_times_percent(interval=0.2)
cpuPercent = psutil.cpu_percent(interval=0.2, percpu=True)
infoCpu = cpuinfo.get_cpu_info()
# ================== SO - Info
wordCpu = platform.architecture()
computerName = platform.node()
soDistro = platform.platform()
soName = platform.system()
platformCpu = platform.processor()
# ================== SO - Process
# procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
# ================== Memória
memRam = psutil.virtual_memory()
memCapacity = round(memRam.total / 1024 ** 3, 2)
memAvailable = round(memRam.available / 1024 ** 3, 2)
memRamOpt1 = psutil.virtual_memory()[0]
# ======= Display Settings
white = (255, 255, 255)
black = (20, 20, 20)
gray = (120, 120, 120)
displayWidth = 1280
displayHeight = 800
# red, orange, yellow, green, blue, purple,
taskManagerBg = [(255, 89, 94), (255, 121, 0), (255, 202, 58), (138, 201, 38), (25, 130, 196), (106, 76, 147)]
taskManagerBgDark = [(205, 39, 44), (205, 71, 0), (155, 152, 58), (88, 151, 0), (0, 80, 146), (56, 26, 97)]
taskManagerBlitColor = [(255, 153, 200), (255, 191, 134), (252, 246, 189), (208, 244, 222), (169, 222, 249),
                        (228, 193, 249)]
taskManagerDisplay = pygame.display.set_mode((displayWidth, displayHeight))  # window size
taskManagerDisplay.fill(white)
pygame.display.set_caption('Wallace dos Anjos - Task Manager')  # window name
pygame.display.update()  # update the screen, as display.flip() do, but more fluid
padding_x = 50
padding_y = 50
font_size = 24
# ======= globals
navItem = 5
option_select = 0
user_text = ''
scan_results = []
catch_ports = []
# ======= disco
disk = psutil.disk_usage('.')
diskTotal = round(disk.total / 1024 ** 3, 2)
diskUsed = round(disk.used / 1024 ** 3, 2)
diskFree = round(disk.free / 1024 ** 3, 2)
diskPercent = disk.percent
# ======= netconfig
netConfig = psutil.net_if_addrs()

clock = pygame.time.Clock()
taskManagerExit = False


################################################## OVERVIEW


def overview():
	taskManagerDisplay.fill(taskManagerBg[navItem])
	taskManagerText('Informação geral', taskManagerBlitColor[navItem], 10, 10, 50)  # msg, color, x, y, font size
	taskManagerText('CPU ' + str(0) + ': ' + str(cpuPercent[0]) + '%', taskManagerBlitColor[navItem], 130, 70,
	                font_size)
	pygame.draw.rect(taskManagerDisplay, taskManagerBlitColor[navItem], [10, 70, cpuPercent[0], 20])
	pygame.draw.rect(taskManagerDisplay, white, [10, 70, 100, 20], 1)
	taskManagerText('Palavra do Processador: ' + str(wordCpu[0]), taskManagerBlitColor[navItem], 10, 100,
	                font_size)  # msg, color, x, y, font size
	taskManagerText('Arquitetura: ' + str(infoCpu["arch"]), taskManagerBlitColor[navItem], 10, 130,
	                font_size)  # msg, color, x, y, font size
	taskManagerText('Processador: ' + infoCpu["brand_raw"], taskManagerBlitColor[navItem], 10, 160,
	                font_size)  # msg, color, x, y, font size
	taskManagerText(str(cpuCores) + ' Núcleos', taskManagerBlitColor[navItem], 10, 190, font_size)

	taskManagerText('RAM Consumo Atual: ' + str(memRam[2]) + '%', taskManagerBlitColor[navItem], 130, 250, font_size)
	pygame.draw.rect(taskManagerDisplay, taskManagerBlitColor[navItem], [10, 250, int(memRam[2]), 20])
	pygame.draw.rect(taskManagerDisplay, white, [10, 250, 100, 20], 1)
	taskManagerText('Armazenamento Total de Memória Ram: ' + str(memCapacity) + 'GB.', taskManagerBlitColor[navItem],
	                10, 280, font_size)
	taskManagerText('Em uso: ' + str(memAvailable) + 'GB.', taskManagerBlitColor[navItem], 10, 310, font_size)
	taskManagerText('outras informações: ' + str(memRam) + 'GB.', taskManagerBlitColor[navItem], 10, 340, font_size)

	taskManagerText('HDD usado: ' + str(diskPercent) + '%', taskManagerBlitColor[navItem], 130, 400, font_size)
	pygame.draw.rect(taskManagerDisplay, taskManagerBlitColor[navItem], [10, 400, diskPercent, 20])
	pygame.draw.rect(taskManagerDisplay, white, [10, 400, 100, 20], 1)
	taskManagerText('Total: ' + str(diskTotal) + 'GB.', taskManagerBlitColor[navItem], 10, 430, font_size)
	taskManagerText('Em uso: ' + str(diskUsed) + 'GB.', taskManagerBlitColor[navItem], 10, 460, font_size)
	taskManagerText('Livre: ' + str(diskFree) + 'GB.', taskManagerBlitColor[navItem], 10, 490, font_size)

	taskManagerText('Endereço IP: ' + str(netConfig["Wi-Fi"][1].address), taskManagerBlitColor[navItem], 130, 550,
	                font_size)
	taskManagerText('Seu Sistema Operacional é: ' + str(soName), taskManagerBlitColor[navItem], 10, 580,
	                font_size)  # msg, color, x, y, font size


################################################## PROCESSOS


def tasks():
	cpuPercent = psutil.cpu_percent(interval=0.1, percpu=True)
	taskManagerDisplay.fill(taskManagerBg[navItem])
	pygame.draw.rect(taskManagerDisplay, gray, [0, 0, 1280, 25])
	pygame.draw.rect(taskManagerDisplay, taskManagerBg[navItem], [7, 5, 103, 25])
	taskManagerText(' PROCESSOS      CPU      MEMÓRIA      DISCOS      REDE ', white, 10, 5,
	                21)  # msg, color, x, y, font size
	taskManagerText('TAREFAS EM EXECUÇÃO:' + str(len(psutil.pids())), taskManagerBlitColor[navItem], 10, 27,
	                48)  # msg, color, x, y, font size
	taskManagerText('Rodando Taskmanager em: ' + str(os.path.abspath('.')), taskManagerBlitColor[navItem], 10, 70,
	                font_size)
	taskManagerText('Os arquivos nessa pasta são: ' + str(os.listdir()), taskManagerBlitColor[navItem], 10, 130,
	                font_size)
	pos_y = 100
	core = 0
	soma = 0
	for h in range(0, cpuCores):
		soma += cpuPercent[core]
		core += 1
	cpuMediaConsumo = soma / cpuCores
	taskManagerText('Média de Consumo de CPU: ' + str(cpuMediaConsumo) + '%', taskManagerBlitColor[navItem], 130, pos_y,
	                font_size)
	pygame.draw.rect(taskManagerDisplay, taskManagerBlitColor[navItem], [10, pos_y, cpuMediaConsumo, 20])
	pygame.draw.rect(taskManagerDisplay, white, [10, pos_y, 100, 20], 1)
	taskManagerText('HD Em uso: ' + str(diskUsed) + 'GB.', taskManagerBlitColor[navItem], 10, 160, font_size)
	pygame.draw.rect(taskManagerDisplay, (225, 91, 0), [10, 190, 1260, 570])
	taskManagerText('PRESSIONE A TECLA [E] PARA EXIBIR/OCULTAR AS TAREFAS ', taskManagerBlitColor[navItem], 120, 430,
	                50)
	taskManagerText('TELA ANTERIOR [<]  |  EXIBIR TAREFAS [E]  |  PRÓXIMA TELA [>]  |  INÍCIO [/]',
	                taskManagerBlitColor[navItem], 10, 770, 24)


def task_by_pids():
	print(f'funfei')
	col = 315
	pygame.draw.rect(taskManagerDisplay, (205, 71, 0), [10, 190, 315, 570])
	pygame.draw.rect(taskManagerDisplay, (185, 51, 0), [col + 10, 190, 315, 570])
	pygame.draw.rect(taskManagerDisplay, (165, 31, 0), [2 * col + 10, 190, 315, 570])
	pygame.draw.rect(taskManagerDisplay, (145, 11, 0), [3 * col + 10, 190, 315, 570])
	i = 0
	i2 = 0
	i3 = 0
	i4 = 0
	j = 0
	for proc in psutil.process_iter():
		i += 10
		j += 1
		info = proc.as_dict(attrs=['pid', 'name'])
		if j < 58:
			taskManagerText(str(j) + ' Proc:' + str(info['pid']) + ' Pid:' + str(info['name']) + str(time.ctime()),
			                taskManagerBlitColor[navItem], 10, int(i + 180), 14)
		elif j > 57 and j <= 114:
			i2 += 10
			taskManagerText(str(j) + ' Proc:' + str(info['pid']) + ' Pid:' + str(info['name']) + str(time.ctime()),
			                taskManagerBlitColor[navItem], col + 10, int(i2 + 180), 14)
		elif j > 114 and j <= 171:
			i3 += 10
			taskManagerText(str(j) + ' Proc:' + str(info['pid']) + ' Pid:' + str(info['name']) + str(time.ctime()),
			                taskManagerBlitColor[navItem], 2 * col + 10, int(i3 + 180), 14)
		elif j > 171 and j <= 228:
			i4 += 10
			taskManagerText(str(j) + ' Proc:' + str(info['pid']) + ' Pid:' + str(info['name']) + str(time.ctime()),
			                taskManagerBlitColor[navItem], 3 * col + 10, int(i4 + 180), 14)


################################################## CPU


def processor():
	print('CPU atualizado!!!')
	cpuPercent = psutil.cpu_percent(interval=0.1, percpu=True)
	taskManagerDisplay.fill(taskManagerBg[navItem])
	pygame.draw.rect(taskManagerDisplay, gray, [0, 0, 1280, 25])
	pygame.draw.rect(taskManagerDisplay, taskManagerBg[navItem], [120, 5, 40, 25])  # x, y, width, height
	taskManagerText(' PROCESSOS      CPU      MEMÓRIA      DISCOS      REDE ', white, 10, 5,
	                21)  # msg, color, x, y, font size
	taskManagerText('Processador: ' + infoCpu["brand_raw"], taskManagerBlitColor[navItem], 10, 27, 48)  # msg, color, x, y, font size
	taskManagerText(str(cpuCores) + ' Núcleos, com ' + str(cpuPhyCores) + ' núcleos físicos e ' + str(
		int(cpuCores - cpuPhyCores)) + ' núcleos lógicos.', taskManagerBlitColor[navItem], 10, 70, font_size)
	taskManagerText(str(cpuPercent[0:]), taskManagerBlitColor[navItem], 130, 800, font_size)
	taskManagerText('Palavra do Processador: ' + str(wordCpu[0]), taskManagerBlitColor[navItem], 250, 100, font_size)
	taskManagerText('Arquitetura: ' + str(infoCpu["arch"]), taskManagerBlitColor[navItem], 250, 130, font_size)
	taskManagerText('Frequência máxima do CPU: ' + str(int(cpuFreq[2]) / 1000) + 'GHz', taskManagerBlitColor[navItem],
	                250, 160, font_size)
	taskManagerText('Seu Sistema Operacional é: ' + str(soName), taskManagerBlitColor[navItem], 250, 190, font_size)
	taskManagerText('Sua distribuição é ' + str(soDistro), taskManagerBlitColor[navItem], 250, 220, font_size)
	taskManagerText('O nome do seu computador é: ' + str(computerName), taskManagerBlitColor[navItem], 250, 250,
	                font_size)
	pos_y = 100
	core = 0
	for i in range(0, cpuCores):
		taskManagerText('CPU ' + str(i) + ': ' + str(cpuPercent[core]) + '%', taskManagerBlitColor[navItem], 130, pos_y,
		                font_size)
		pygame.draw.rect(taskManagerDisplay, taskManagerBlitColor[navItem], [10, pos_y, cpuPercent[core], 20])
		pygame.draw.rect(taskManagerDisplay, white, [10, pos_y, 100, 20], 1)
		pos_y += 30
		core += 1
	taskManagerText('TELA ANTERIOR [<]  |  EXIBIR TAREFAS [E]  |  PRÓXIMA TELA [>]  |  INÍCIO [/]', taskManagerBlitColor[navItem], 10, 770, 24)


################################################## MEMÓRIA


def memory():
	taskManagerDisplay.fill(taskManagerBg[navItem])
	pygame.draw.rect(taskManagerDisplay, gray, [0, 0, 1280, 25])
	pygame.draw.rect(taskManagerDisplay, taskManagerBg[navItem], [174, 5, 77, 25])  # x, y, width, height
	taskManagerText(' PROCESSOS      CPU      MEMÓRIA      DISCOS      REDE ', white, 10, 5, 21)  # msg, color, x, y, font size
	taskManagerText('INFORMAÇÕES DE MEMÓRIA', taskManagerBlitColor[navItem], 10, 27, 48)  # msg, color, x, y, font size
	print('atualizei')
	taskManagerText('Consumo Atual: ' + str(memRam[2]) + '%', taskManagerBlitColor[navItem], 10, 70, font_size)
	pygame.draw.rect(taskManagerDisplay, taskManagerBlitColor[navItem], [10, 100, int(memRam[2]), 20])
	pygame.draw.rect(taskManagerDisplay, white, [10, 100, 100, 20], 1)
	taskManagerText('Armazenamento Total de Memória Ram: ' + str(memCapacity) + 'GB.', taskManagerBlitColor[navItem],
	                10, 130, font_size)
	taskManagerText('Em uso: ' + str(memAvailable) + 'GB.', taskManagerBlitColor[navItem], 10, 160, font_size)
	pos_y = 190
	mem_legenda = ['Total ', 'Disponível ', 'Porcentagem ', 'Usado ', 'Livre ']
	for i in range(0, len(memRam)):
		taskManagerText(str(mem_legenda[i]) + str(memRam[i]) + 'GB.', taskManagerBlitColor[navItem], 10, pos_y,
		                font_size)
		pos_y += 30
	taskManagerText('outras informações: ' + str(memRam) + 'GB.', taskManagerBlitColor[navItem], 10, 360, 14)
	taskManagerText('TELA ANTERIOR [<]  |  PRÓXIMA TELA [>]  |  INÍCIO [/]', taskManagerBlitColor[navItem], 10, 770, 24)


################################################## DISCOS


def harddisk():
	taskManagerDisplay.fill(taskManagerBg[navItem])
	pygame.draw.rect(taskManagerDisplay, gray, [0, 0, 1280, 25])
	pygame.draw.rect(taskManagerDisplay, taskManagerBg[navItem], [264, 5, 67, 25])  # x, y, width, height
	taskManagerText(' PROCESSOS      CPU      MEMÓRIA      DISCOS      REDE ', white, 10, 5,
	                21)  # msg, color, x, y, font size
	taskManagerText('INFORMAÇÕES DE DISCO', taskManagerBlitColor[navItem], 10, 27, 48)  # msg, color, x, y, font size
	taskManagerText('Você usou ' + str(diskPercent) + '% do seu Disco.', taskManagerBlitColor[navItem], 10, 70,
	                font_size)
	pygame.draw.rect(taskManagerDisplay, taskManagerBlitColor[navItem], [10, 100, diskPercent, 20])
	pygame.draw.rect(taskManagerDisplay, white, [10, 100, 100, 20], 1)
	taskManagerText('Total: ' + str(diskTotal) + 'GB.', taskManagerBlitColor[navItem], 10, 130, font_size)
	taskManagerText('Em uso: ' + str(diskUsed) + 'GB.', taskManagerBlitColor[navItem], 10, 160, font_size)
	taskManagerText('Livre: ' + str(diskFree) + 'GB.', taskManagerBlitColor[navItem], 10, 190, font_size)
	taskManagerText('TELA ANTERIOR [<]  |  PRÓXIMA TELA [>]  |  INÍCIO [/]',
	                taskManagerBlitColor[navItem], 10, 770, 24)


################################################## REDE


def get_nmap(options, ip):
	global catch_ports
	# escrevo o comando
	command = "nmap " + options + " " + ip
	# executo o comando
	process = os.popen(command)
	catch_ports = str(process.read())
	return catch_ports


def netinfo():
	taskManagerDisplay.fill(taskManagerBg[navItem])
	pygame.draw.rect(taskManagerDisplay, gray, [0, 0, 1280, 25])
	pygame.draw.rect(taskManagerDisplay, taskManagerBg[navItem], [341, 5, 54, 25])  # x, y, width, height
	taskManagerText(' PROCESSOS      CPU      MEMÓRIA      DISCOS      REDE ', white, 10, 5, 21)  # msg, color, x, y, font size
	taskManagerText('INFORMAÇÕES DO HOST', taskManagerBlitColor[navItem], 10, 27, 48)  # msg, color, x, y, font size
	pygame.draw.rect(taskManagerDisplay, taskManagerBgDark[navItem], [440, 190, 830, 570])
	taskManagerText('TELA ANTERIOR [<]  |  ESCANEAR A REDE [E]  |  REQUISITAR SERVIDOR [R]  |  PRÓXIMA TELA [>]  |  INÍCIO [/]', taskManagerBlitColor[navItem], 10, 770, 24)
	io_status = psutil.net_io_counters(pernic=True)
	net_proc_status = psutil.net_connections()
	host_list_name = []
	host_list_ip = []
	host_list_mask = []
	nomes = []
	traffic = []
	net_proc = []
	pos_y = 100
	for i in netConfig:
		host_list_name.append(i)
		host_list_ip.append(str(netConfig[str(i)][1].address))
		host_list_mask.append(str(netConfig[str(i)][1].netmask))

	for i in io_status:
		nomes.append(str(i))

	for j in nomes:
		print(j)
		print("\t" + str(io_status[j]))
		print("\t" + str(io_status[j][0]))
		print("\t" + str(io_status[j][1]))
		traffic.append(io_status[j])

	for i in psutil.net_connections():
		net_proc.append(i)

	for i in range(0, len(host_list_ip)):
		taskManagerText(host_list_name[i] + ': ' + host_list_ip[i], white, 10, pos_y, font_size)
		taskManagerText('Máscara de sub rede' + ': ' + host_list_mask[i], taskManagerBlitColor[navItem], 10, pos_y + 20, font_size-6)
		taskManagerText(str(len(net_proc_status)) + ' Processos Ativos na Rede', taskManagerBlitColor[navItem], 10, pos_y + 40, font_size-6)
		taskManagerText('Trafego Sent/Recv' + str(traffic[i][0]) + ' / ' + str(traffic[i][1]) + ' bytes', taskManagerBlitColor[navItem], 10, pos_y + 60, font_size-6)
		pos_y += 90

	if option_select == 0:
		taskManagerText('[E] ESCANEAR SUB-REDE | [R] REQUISIÇÕES AO SERVIDOR', taskManagerBlitColor[navItem], 460, 200, 36)
		if os.path.isfile('scan_results.txt'):
			with open('scan_results.txt', 'r') as f:
				ip_target = f.read().split("', '")
			clean_first_ip = ip_target[0].split("['")
			ip_target[0] = clean_first_ip[1]
			clean_last_ip = ip_target[-1].split("']")
			ip_target[-1] = clean_last_ip[0]
			print(ip_target)
			pos_y2 = 250
			for i in range(0, len(ip_target)):
				taskManagerText('Ip conectado na sub rede: ' + str(ip_target[i]), taskManagerBlitColor[navItem], 460, pos_y2,
				                font_size)
				pos_y2 += 30

	if option_select == 1:
		taskManagerText('Resultado da busca na sub rede', taskManagerBlitColor[navItem], 520, 400, 50)
		pos_y2 = 250
		for i in range(0, len(scan_results)):
			taskManagerText('Ip conectado na sub rede: ' + str(scan_results[i]), taskManagerBlitColor[navItem], 520, pos_y2, font_size)
			# taskManagerText('Ips encontrados: ' + str(catch_ports), taskManagerBlitColor[navItem], 520, 30 + pos_y2, font_size)
			print(f'de dentro da função netinfo optionselect1{catch_ports}')
			pos_y2 += 30

	if option_select == 2:
		taskManagerText('INFORMAÇÕES OBTIDAS DO SERVIDOR', taskManagerBlitColor[navItem], 460, 200, 36)
		pos_y2 = 250
		for i in range(0, len(print_request)):
			taskManagerText(str(print_request[i]), taskManagerBlitColor[navItem], 460, pos_y2,
			                font_size-4)
			pos_y2 += 30



def client_request():
	global print_request
	pygame.draw.rect(taskManagerDisplay, taskManagerBgDark[navItem], [440, 190, 830, 570])
	# cliente
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((socket.gethostname(), 1243))

	while True:
		full_msg = b''
		new_msg = True
		while True:
			msg = s.recv(16)
			if new_msg:
				print("new msg len:", msg[:HEADERSIZE])
				msglen = int(msg[:HEADERSIZE])
				new_msg = False

			print(f"full message length: {msglen}")
			full_msg += msg
			print(len(full_msg))
			if len(full_msg) - HEADERSIZE == msglen:
				print("full msg recvd")
				print(full_msg[HEADERSIZE:])
				print(pickle.loads(full_msg[HEADERSIZE:]))
				print_request = str(pickle.loads(full_msg[HEADERSIZE:]))
				print(type(print_request))
				print_request = print_request.split("', '")
				clean_first_print_request = print_request[0].split("['")
				print_request[0] = clean_first_print_request[1]
				clean_last_print_request = print_request[-1].split("']")
				print_request[-1] = clean_last_print_request[0]
				print(f'print de dentro da função client_request{print_request[0]}')
				print(f'print de dentro da função client_request{print_request[1]}')
				print(f'print de dentro da função client_request{print_request[2]}')
				print(f'print de dentro da função client_request{print_request[3]}')
				print(f'print de dentro da função client_request{print_request[4]}')
				print(f'print de dentro da função client_request{print_request[5]}')
				new_msg = True
				full_msg = b""


def retorna_codigo_ping(hostname):
	# Usa o utilitario ping do sistema operacional para encontrar o host. ('-c 5') indica, em sistemas linux, que deve mandar 5 pacotes. ('-W 3') indica, em sistemas linux, que deve esperar 3 milisegundos por uma resposta. Esta funcao retorna o codigo de resposta do ping
	plataforma = platform.system()
	args = []
	if plataforma == "Windows":
		args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]
	else:
		args = ['ping', '-c', '1', '-W', '1', hostname]
	ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
	return ret_cod


def verifica_hosts(base_ip):
	# Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com todos os host que tiveram resposta 0 (ativo)
	host_validos = []
	return_codes = dict()
	for i in range(1, 255):
		return_codes[base_ip + '{0}'.format(i)] = retorna_codigo_ping(base_ip + '{0}'.format(i))
		if i % 20 == 0:
			print(".", end="")
		if return_codes[base_ip + '{0}'.format(i)] == 0:
			host_validos.append(base_ip + '{0}'.format(i))
	print("\nMapping ready...")
	return host_validos


def start_scan():
	global scan_results
	# Chamadas
	# print(f'seu ip é {str(netConfig["Wi-Fi"][1].address)}')
	ip_string = str(netConfig["Wi-Fi"][1].address)  # word_label
	ip_lista = ip_string.split('.')
	base_ip = ".".join(ip_lista[0:3]) + '.'
	print('O teste será feito na sub rede: ', base_ip)
	scan_results = verifica_hosts(base_ip)
	print(f'Ips encontrados na sub rede {scan_results}')
	with open('scan_results.txt', 'w') as f:
		f.write(f'{scan_results}')


def port_scanner():
	if os.path.isfile('scan_results.txt'):
		with open('scan_results.txt', 'r') as f:
			ip_target = f.read().split("', '")
		clean_first_ip = ip_target[0].split("['")
		ip_target[0] = clean_first_ip[1]
		clean_last_ip = ip_target[-1].split("']")
		ip_target[-1] = clean_last_ip[0]
		for i in range(0, len(ip_target)):
			try:
				get_nmap('-F', ip_target[i])
			# print('---------------')
			# print(f'Protocolo: {prot}')
			# lport = nm[ip_target[i]][prot].keys()
			# for port in lport:
			# 	print(f'Porta: {port} |\n Estado: {nm[ip_target[i]][prot][port]["State"]}')
			except:
				pass
		# nm = nmap.PortScanner()
		# for i in range(0, len(ip_target)):
		# 	# print(f'get command line used for the scan : nmap -oX - -p 22-443 {ip_target[i]} {nm.command_line()}')
		# 	# print(f'get nmap scan informations {nm.scaninfo()}')  # {'tcp': {'services': '22-443', 'method': 'connect'}}
		# 	# print(f'get all hosts that were scanned {nm.all_hosts()}')
		# 	# print(f'get one hostname for host {ip_target[i]}, usualy the user record {nm[ip_target[i]].hostname()}')
		# 	# print(f'get list of hostnames for host {ip_target[i]} as a list of dict {nm[ip_target[i]].hostnames()}')
		# 	# print(f'get hostname for host {ip_target[i]} {nm[ip_target[i]].hostname()}')
		# 	# print(f'get state of host {ip_target[i]} (up|down|unknown|skipped) {nm[ip_target[i]].state()}')
		# 	# print(f'get all scanned protocols tcp, udp in (ip|tcp|udp|sctp) {nm[ip_target[i]].all_protocols()}')
		# 	# print(f'get all ports for tcp protocol {nm[ip_target[i]]["tcp"].keys()}')
		# 	# print(f'get all ports for tcp protocol (sorted version) {nm[ip_target[i]].all_tcp()}')
		# 	# print(f'get all ports for udp protocol (sorted version) {nm[ip_target[i]].all_udp()}')
		# 	# print(f'get all ports for ip protocol (sorted version) {nm[ip_target[i]].all_ip()}')
		# 	# print(f'get all ports for sctp protocol (sorted version) {nm[ip_target[i]].all_sctp()}')
		# 	# print(f'is there any information for port 22/tcp on host {ip_target[i]} {nm[ip_target[i]].has_tcp(22)}')
		# 	# print(f'get infos about port 22 in tcp on host {ip_target[i]} {nm[ip_target[i]].tcp(22)}')
		# 	# print(f'{i} try...')
		# 	# print(nm.scan(ip_target[i], '22-443'))  # scan host 127.0.0.1, ports from 22 to 443
		# 	# print(ip_target[i])
		# 	#nm.scan(ip_target[i])
		# 	#print(nm[ip_target[i]].hostname())



##################################################


def taskManagerText(msg, color, padding_x, padding_y, font_size, ):
	font_style = pygame.font.SysFont(None, font_size, False, False)
	screen_text = font_style.render(msg, True, color)
	taskManagerDisplay.blit(screen_text, [padding_x, padding_y])


def taskManagerLoop():
	global navItem
	global taskManagerExit
	global option_select
	taskManagerDisplay.fill(taskManagerBg[navItem])
	time_refresh = 0
	while not taskManagerExit:
		time_updated = time.localtime()
		# esse evento dispara as trocas de tela
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				taskManagerExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SLASH:
					navItem = 0
					# Zera os valores das opções na troca da tela
					option_select = 0
					taskManagerDisplay.fill(taskManagerBg[navItem])
				if event.key == pygame.K_KP_DIVIDE:
					navItem = 0
					# Zera os valores das opções na troca da tela
					option_select = 0
					taskManagerDisplay.fill(taskManagerBg[navItem])
				if event.key == pygame.K_RIGHT:
					if navItem < 5:
						navItem += 1
						# Zera os valores das opções na troca da tela
						option_select = 0
						taskManagerDisplay.fill(taskManagerBg[navItem])
					else:
						navItem = 1
						# Zera os valores das opções na troca da tela
						option_select = 0
						taskManagerDisplay.fill(taskManagerBg[navItem])
				if event.key == pygame.K_LEFT:
					if navItem > 1:
						navItem -= 1
						# Zera os valores das opções na troca da tela
						option_select = 0
						taskManagerDisplay.fill(taskManagerBg[navItem])
					else:
						navItem = 5
						# Zera os valores das opções na troca da tela
						option_select = 0
						taskManagerDisplay.fill(taskManagerBg[navItem])

				if event.key == pygame.K_e:
					# Opção E de Processos para exibir threads
					if navItem == 1:
						if option_select == 0:
							option_select = 1
						else:
							option_select = 0

					# Opção E de Redes para atualizar hosts encontrados
					if navItem == 5:
						if option_select == 0:
							option_select = 1
							start_scan()
							try:
								port_scanner()

							except:
								pass
						else:
							option_select = 0

				if event.key == pygame.K_r:
					# Opção R de redes para acionar requisição ao servidor
					if navItem == 5:
						if option_select == 0:
							threading.Thread(target=client_request).start()
							option_select = 2
						else:
							option_select = 0

		if navItem == 0:
			overview()

		elif navItem == 1:
			if time_refresh != time_updated:
				tasks()
				if option_select == 1:
					task_by_pids()
				time_refresh = time_updated

		elif navItem == 2:
			if time_refresh != time_updated:
				processor()
				time_refresh = time_updated

		elif navItem == 3:
			if time_refresh != time_updated:
				memory()
				time_refresh = time_updated

		elif navItem == 4:
			harddisk()

		elif navItem == 5:
			if time_refresh != time_updated:
				netinfo()
				time_refresh = time_updated

		pygame.display.update()


taskManagerLoop()