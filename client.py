import threading
import time
import random
import socket
import sys

# Make sure port entered is valid
def test_port(port):
    try:
        port = int(port)
        if 1 <= int(port) <= 65535:
            return port
        else:
            raise ValueError
    except ValueError:
        print("Illegal port number")
        exit()

# Gather list of hostname strings to send to server(s)
def hns_list():
    hostnames = []
    file = open("PROJI-HNS.txt","r") 
    for line in file:
        hostnames.append(line.strip().lower())
    return hostnames

# Takes string from server(s) and formats for easy access
def process_data(data):
    formatted = []
    temp_line = data.split()
    hostname = temp_line[0].lower()
    ip = temp_line[1]
    flag = temp_line[2]
    formatted = [hostname,ip,flag]
    return formatted

# Writes resolved hosts to file_name
def output_hosts(hosts):
    try:
        file_name = "./RESOLVED.txt"
        file=open(file_name, 'w+')
        for host in hosts:
            file.write("{}\n".format(host))
        file.close()
    except:
        print("[C]: Error writing to {}".format(file_name))
    finally:
        file.close()

# Run Client
def client():
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket to DNSRS created")
    except socket.error as err:
        print("[C]: socket open error: {} \n".format(err))
        exit()
    # Gather fields from user
    rs_hostname = sys.argv[1]
    rs_port = test_port(sys.argv[2])
    ts_port = test_port(sys.argv[3])
    # Connect to the server on local machine
    rs_addr = socket.gethostbyname(rs_hostname)
    rs_binding = (rs_addr, rs_port)
    print("[C]: Connecting to RS host: {} {}".format(rs_hostname,rs_binding))
    rs.connect(rs_binding)
    # Send message(s) to server
    hostnames = hns_list()
    len = 200 #max data length
    resolved_hosts = []
    for host in hostnames:
        print("[C]: Sending {} to RS".format(host))
        rs.send(host.encode('utf-8'))
        try: 
            data = rs.recv(len).decode('utf-8')
            print("[C]: Received {} from RS".format(data))
            if (data != "skip"):
                # Format for easy access 0 = host, 1 = ip, 2 = flag
                dns_info = process_data(data)
                ret_host = dns_info[0]
                ret_ip = dns_info[1]
                ret_flag = dns_info[2]
                # Append to resolved file or proceed to ask TS
                if ret_flag == "A":
                    resolved_hosts.append(ret_host + " "  +ret_ip + " " + ret_flag)
                elif ret_flag == "NS":
                    # Not resolved. Open socket for TS
                    try:
                        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        print("[C]: Client socket to DNSTS created")
                    except socket.error as err:
                        print("[C]: socket open error: {} \n".format(err))
                        exit()
                    # Connect to the server on local machine
                    if ret_ip == "-":
                        ts_addr = socket.gethostbyname(ret_host)
                    else:
                        ts_addr = ret_ip
                    print (ret_ip)
                    ts_binding = (ts_addr, ts_port)
                    print("[C]: Connecting to TS host: {} {}".format(ret_host,ts_binding))
                    ts.connect(ts_binding)
                    # Send TS host to resolve
                    print("[C]: Sending {} to TS".format(host))
                    ts.send(host.encode('utf-8'))
                    # Receive data from TS
                    data = ts.recv(len).decode('utf-8')
                    print("[C]: Received: {}".format(data))
                    # Format for easy access 0 = host, 1 = ip, 2 = flag
                    dns_info = process_data(data)
                    # Add remaining data to resolved file
                    if dns_info[2] == "Error:HOSTNOTFOUND":
                        dns_info[2] = "Error:HOST NOT FOUND"
                    resolved_hosts.append(dns_info[0]+ " "  +dns_info[1] + " " + dns_info[2])
                    # Close socket
                    ts.close()
                    print("[C]: Client socket to DNSTS closed")
            else:
                print("[RS]: Error. TS server not found to process {}".format(host))
        except socket.error as err:
            print("[C]: Network error: {} \n".format(err))
    output_hosts(resolved_hosts)      
    # Close the rs socket
    rs.close()
    print("[C]: Client socket to DNSRS closed")
    exit()

if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print("[C]: Error.\n \tSyntax: python client.py rsHostname rsListenPort tsListenPort")
        exit()

    t1 = threading.Thread(name='client', target=client)

    t1.start()

    print("Done.")
