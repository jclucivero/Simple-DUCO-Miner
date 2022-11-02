import socket
import time
import hashlib
from threading import Thread
import os
from multiprocessing import Process, Manager, Semaphore
from random import randint
import requests

username = input("Username: ")
mining_key = input("Mining Key: ")
efficency = int(input("Efficency(reccomended is 95): "))

accepted = 0
invalid = 0
blocks = 0


class Client:

  def getPool():
    return requests.get("http://51.15.127.80/getPool").json()

  def send(connection, message):
    connection.sendall(message.encode())

  def recv(connection):
    return connection.recv(2048).decode().strip("\n")


class Miner:

  def mine(job):
    global efficency
    eff = efficency
    time_start = time.time()
    base_hash = hashlib.sha1(job[0].encode('ascii'))
    print(f"Difficulty: {100 * int(job[2]) + 1}")
    for nonce in range(100 * int(job[2]) + 1):
      temp_h = base_hash.copy()
      temp_h.update(str(nonce).encode('ascii'))
      d_res = temp_h.hexdigest()
      if nonce % 5000 == 0:
        time.sleep(eff / 200)
      if d_res == job[1]:
        time_elapsed = time.time() - time_start
        hashrate = nonce / time_elapsed
        return [nonce, hashrate]
        break
    return [0, 0]

  def start():
    global accepted
    global blocks
    global invalid
    single_miner_id = randint(0, 2811)
    connection = socket.socket()
    connection.settimeout(600)
    pool = Client.getPool()
    connection.connect((pool['ip'], pool['port']))
    Client.send(connection, "")
    server_msg = Client.recv(connection)
    os.system("clear")
    print(f"Grantrocks Python Miner V0.1\n" +
          f"Accepted Shares: {accepted}\n" + f"Blocks Found: {blocks}\n" +
          f"Invalid Shares: {invalid}\n" +
          f"Hashrate: will update when you mine your first share")
    while True:
      Client.send(connection, f"JOB,{username},LOW,{mining_key}")
      server_msg = Client.recv(connection)
      job = server_msg.split(",")
      if "3." in job[0]:
        print("New connection started")
      elif job[0] != "":
        result = Miner.mine(job)
        data = f"{result[0]},,Official PC Miner 3.33,Custom Miner,,{single_miner_id})"
        Client.send(connection, data)
        server_msg = Client.recv(connection)
        if server_msg == "GOOD":
          accepted += 1
        elif server_msg == "BLOCK":
          blocks += 1
        elif server_msg == "BAD":
          invalid += 1
        os.system("clear")
      print(f"Grantrocks Python Miner V0.1\n" +
            f"Accepted Shares: {accepted}\n" + f"Blocks Found: {blocks}\n" +
            f"Invalid Shares: {invalid}\n" + f"Hashrate: {result[1]}H/s")


Miner.start()