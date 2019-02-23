# Recursive-DNS-client-and-DNS-servers
Project 1: Recursive DNS client and DNS servers
===============================================

Overview
--------

The goal of this project is to implement a simplified DNS system consisting of a
client program and two server programs: RS (a simplified root DNS server) and TS
(a simplified top-level DNS server).

One socket will be used to communicate with RS and the other with TS.

The RS and TS programs each maintain a DNS_table consisting of three fields:
- Hostname
- IP address
- Flag (A or NS)

The client always connects first to RS, sending the queried hostname as a
string. The RS program does a look up in its DNS_table, and if there is a match,
sends the entry as a string

  Hostname IPaddress A

If there is no match, RS sends the string

  TSHostname - NS

where TShostname is the name of the machine on which the TS program is running.

If the client receives a string with "A" field, it outputs the received string
as is. On the other hand, if the client receives a string with "NS" field, it
uses the TSHostname part of the received string to determine the IP address of
the machine running the TS program and connects to the TS program using a second
socket.

The client then sends the queried hostname as a string to TS. The TS program
looks up the hostname in its DNS_table, and if there is a match, sends the entry
as a string

  Hostname IP address A

to the client. Otherwise, it sends an error string

  Hostname - Error:HOST NOT FOUND

In the TS outputs above, Hostname is the queried hostname. The client outputs
the string received from TS as is.

Note that all DNS lookups are case-insensitive. If there is a hit in the local
DNS table, the server programs must respond with the version of the string that
is in their local DNS table.

Usage
--------
The programs works with the following command lines:

  python ts.py tsListenPort
  python rs.py rsListenPort
  python client.py rsHostname rsListenPort tsListenPort

Here tsListenPort (rsListenPort) is the port on which TS (RS) listens for
requests and rsHostname is the hostname of the machine running the RS program. 

The hostname strings to be queried will be given one per line in a file
PROJI-HNS.txt.

The entries of the local DNS tables, one each for RS and TS, will be strings
with fields separated by spaces. There will be one entry per line. You can see
the format in PROJI-DNSRS.txt and PROJI-DNSTS.txt. The client program outputs
to a file RESOLVED.txt, with one line per result.
