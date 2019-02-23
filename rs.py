#Alexsandr Vobornov
import threading
import time
import random
import sys
import socket
# When populate_dns_table finds an entry with NS, store in memory
TSHost = ""
TSHost_ip = ""
# Make sure port entered is valid
def test_port(port):
    try:
        port = int(port)
        if 1 <= int(port) <= 65535:
            return port
        else:
            raise ValueError
    except ValueError:
        print("Error: Illegal port number")
        exit()

# Populate and return a table if DNS file exists.
def populate_dns_table():
    global TSHost
    global TSHost_ip
    dns_table = {}
    try:
        file_name = "PROJI-DNSRS.txt"
        file = open(file_name,"r") 
        for line in file:
            line = line.strip()
            if line:
                temp_line = line.split()
                hostname = temp_line[0].lower()
                ip = temp_line[1]
                flag = temp_line[2].upper()
                # if it's the hostname of TS, dont add to dns table, memorize it
                # eventually maybe add them to a list so that you can ask multiple TS servers
                if flag == "NS":
                    TSHost = hostname
                    TSHost_ip = ip
                else:
                    dns_table[hostname] = [ip,flag]
        return dns_table
    except:
        print("[RS]: Error. File {} error".format(file_name))
        exit()
    finally:
        file.close()

# Check to see if host is in DNS table and respond accordingly. No TS server found -> skip
def process_query(hostname,dns_table):
    if hostname in dns_table:
        ip = dns_table[hostname][0]
        flag = dns_table[hostname][1]
        return hostname+" "+ip+" "+flag
    elif TSHost:
        return TSHost + " " + TSHost_ip + " NS"
    print("[RS]: Error. Skipping record {}, TS not found".format(hostname))
    return "skip"

# Run server
def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[RS]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    port = test_port(sys.argv[1])
    server_binding = ('', port) # (sys.argv)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[RS]: Server host name is: {}".format(host))
    host_ip = (socket.gethostbyname(host))
    print("[RS]: Server IP address is: {}".format(host_ip))

    dns_table = populate_dns_table()

    while True:
        client, address = ss.accept()
        print("[RS]: Got a connection request from a client at: {}".format(address))
        try: 
            # Receive data/hostname from the client
            data_from_client = client.recv(200).decode('utf-8')
            # Continous processing of data from client
            while data_from_client or 0:
                # Send data to client
                data = process_query(data_from_client, dns_table)
                # Checks if TS server exists before processing request. If it doesnt, skip record
                print("[RS]: Client sent {} | Server sending {} to client {}".format(data_from_client,data, address))
                client.send(data.encode('utf-8'))
                # Wait for more data from client
                data_from_client = client.recv(200).decode('utf-8')
            else: 
                client.close()
        except socket.error as err:
            client.close()
            print(err.args, err.message)

    #time.sleep(10)

    # Close the server socket
    ss.close()
    exit()

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Error.\n Syntax: python rs.py tsListenPort")
        exit()

    t1 = threading.Thread(name='server', target=server)

    t1.start()
