_A='libducohasher.so'
import socket,time,os
from random import randint
import requests
from platform import machine as osprocessor
server='https://server.duinocoin.com/'
try:import libducohasher
except:
	if os.name=='nt':
		r=requests.get(server+'fasthash/libducohashWindows.pyd')
		with open('libducohasher.pyd','wb')as f:f.write(r.content)
	elif os.name=='posix':
		if osprocessor()=='aarch64':url=server+'fasthash/libducohashPi4.so'
		elif osprocessor()=='armv7l':url=server+'fasthash/libducohashPi4_32.so'
		elif osprocessor()=='armv6l':url=server+'fasthash/libducohashPiZero.so'
		elif osprocessor()=='x86_64':url=server+'fasthash/libducohashLinux.so'
		if not os.path.isfile(_A):
			r=requests.get(url)
			with open(_A,'wb')as f:f.write(r.content)
	else:print('You will have to manually compile fasthash. Go to the duino coin github then wiki and click on how to compile fasthash.')
username=input('Username: ')
mining_key=input('Mining Key: ')
rig_id=input('Rig Name: ')
efficency=int(input('Efficency(reccomended is 95): '))
eff=0
if 99>efficency>=90:eff=0.005
elif 90>efficency>=70:eff=0.1
elif 70>efficency>=50:eff=0.8
elif 50>efficency>=30:eff=1.8
elif 30>efficency>=1:eff=3
print('Mining details will show the details of what you are mining, but can significantly slow down the mining process.')
display_mining_details=input('Display Mining Details (y/n)? ')
accepted=0
invalid=0
blocks=0
speed=100
class Client:
	def getPool():return requests.get('http://51.15.127.80/getPool').json()
	def send(connection,message):connection.sendall(message.encode())
	def recv(connection):return connection.recv(2048).decode().strip('\n')
class Miner:
	def mine(job,display_mining_details):global speed;global eff;print(f"Difficulty: {100*int(job[2])+1}\n");time_start=time.time();hasher=libducohasher.DUCOHasher(bytes(job[0],encoding='ascii'));nonce=hasher.DUCOS1(bytes(bytearray.fromhex(job[1])),int(job[2]),int(eff));time_elapsed=time.time()-time_start;hashrate=nonce/time_elapsed;return[nonce,hashrate]
	def start():
		D='port';C='ip';B='clear';A='';global accepted;global blocks;global invalid;global rig_id;global speed;global display_mining_details;single_miner_id=randint(0,2811);connection=socket.socket();connection.settimeout(20);pool=Client.getPool();connection.connect((pool[C],pool[D]));Client.send(connection,A);server_msg=Client.recv(connection);os.system(B);print(f"Grantrocks Python Miner V0.1\n"+f"Accepted Shares: {accepted}\n"+f"Blocks Found: {blocks}\n"+f"Invalid Shares: {invalid}\n"+f"Hashrate: will update when you mine your first share\n")
		while True:
			Client.send(connection,f"JOB,{username},MEDIUM,{mining_key}");server_msg=Client.recv(connection);job=server_msg.split(',')
			if'3.'in job[0]:print('New connection started')
			elif job[0]!=A:
				result=Miner.mine(job,display_mining_details);data=f"{result[0]},{result[1]},Official PC Miner 3.33,{rig_id},,{single_miner_id})";Client.send(connection,data);server_msg=Client.recv(connection)
				if server_msg=='GOOD':accepted+=1
				elif server_msg=='BLOCK':blocks+=1
				elif server_msg=='BAD':invalid+=1
				os.system(B)
			elif job==A:connection.close();connection=socket.socket();connection.settimeout(20);connection.connect((pool[C],pool[D]));Client.send(connection,A);os.system(B);print('Reconnected')
			print(f"Grantrocks Python Miner V0.1\n"+f"Accepted Shares: {accepted}\n"+f"Blocks Found: {blocks}\n"+f"Invalid Shares: {invalid}\n"+f"Hashrate: {round(float(result[1])/1000,2)}KH/s")
Miner.start()