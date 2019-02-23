0. Please write down the full names and netids of both your team members.
	Alexsandr Vobornov - av510
1. Briefly discuss how you implemented your recursive client functionality.
	Both the top-level and root servers stay open to process client requests and the DNS tables are dictionaries. 
	The RS DNS table knows, by coming across an NS flag, it's the name of a TS server and stores it in a global variable TSHost. 
	The client passes a host name to the RS server. If the RS server see's an A record in the dictionary by looking at the flag it passes the record back to the client where the client formats the string and places it in resolved_hosts.
	If RS cannot resolve the host, it will send back the NS record with the name and ip of the host. If ip is not specified it will try to fetch the ip by socket.gethostbyname(). 
	If no TS server is specified, it will skip the record and resolve the ones that the RS server knows. When the client finds out the record sent back from RS is the name of the TS server (by reading the flag), it will 
	open a socket to the TS server and attempt to establish a connection. If a connection is successful, it will ask the TS if it knows the record that RS could not resolve. 
	It outputs appropriately; the client then deals with the data and closes the connection, proceeding to process other hosts.
2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.
   Not that I was able to find. I tested my program by running the client, TS, and RS on various ilab machines and my computer. I was able to communicate back and forth as long as the ports were right.
3. What problems did you face developing code for this project?
	For python troubles I used stackoverflow (syntax, etc.), the algorithm for servers/client was easy to implement by reading the instructions.
	It was actually really fun and I've gained an appreciation for python just because of how easy it is to write and test code. I previously did this project in C and it was a NIGHTMARE that wouldn't run. In python I was able to get it to run on all machines with no issue 
	in a few days without getting a headache.
4. What did you learn by working on this project?
	I learned how to properly implement sockets, their logic, and how root and top-level DNS works. Re-learning python was quite nice, after many semesters of C I'm thankful this project was in python.