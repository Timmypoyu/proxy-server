from socket import *
import sys, os, errno
if len(sys.argv) <= 1:
       print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP \
Address Of Proxy Server')
       sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverPort = 8881

try: 
       tcpSerSock.bind((sys.argv[1], serverPort))
except:
       print("Error: Bind failed, probably address already in use")
       sys.exit(1)

tcpSerSock.listen(1) 

while 1:

       # Start receiving data from the client
       print('Ready to serve...')
       tcpCliSock, addr = tcpSerSock.accept()
       print('Received a connection from:', addr)
       orig_message = tcpCliSock.recv(1024).decode() 
       print(orig_message)
       message = orig_message
       print(message)

       # Extract the filename from the given message
       print(message.split()[1])
       filename = message.split()[1].partition("/")[2]
       print(filename)
       fileExist = "false"
       referedFlag = "false"

       # refered or not
       if "referer" in orig_message.lower():
              print("There is a referer")
              referedFlag = "true"

       if referedFlag == "true":
             for eachLine in orig_message.split('\n'):
                    if "referer" in eachLine.lower():
                           referLine = eachLine
                           break

             # parse referLine 
             referLine = referLine.partition("//")[2].partition("/")[2]
       
       try:
             # Check wether the file exist in the cache
             f = open(filename, "r")
             outputdata = f.readlines()
             fileExist = "true"
             local_flag = "false"
  
             if "HTTP/" not in outputdata[0]: 
	            local_flag = "true" 
             
             if local_flag == "false":
                     #Content-Type:
		     for each in outputdata:
			    if "content-type:" in each.lower():
				 contentLine = each 
				 break
	   
	             contentType = contentLine.split()[1].partition(";")[0]  
  
             # ProxyServer finds a cache hit and generates a response message
             tcpCliSock.send("HTTP/1.0 200 OK\r\n")
             if local_flag == "false": 
                    tcpCliSock.send("Content-Type:" + contentType + "\r\n")
             else:
                    tcpCliSock.send("Content-Type: text/html\r\n")

             for each in outputdata:
                    tcpCliSock.send(each)
             f.close()
             
             print('Read from cache')
       # Error handling for file not found in cache
       except IOError:
             if fileExist == "false":
                    # Create a socket on the proxyserver
                    c = socket(AF_INET, SOCK_STREAM) # Fill in start.# Fill in end.
                     
                    if referedFlag == "false": 
                           hostn = filename.replace("www.","",1).split("/", 1)[0]
                           file_from_netHost = filename.partition("/")[2]
                    else: 
                           referLine = referLine.strip(' \t\r\n')
                           print("referLine: " + referLine)
                           hostn = referLine.replace("www.", "", 1).split("/", 1)[0] 
                           if referLine in filename: 
                                  file_from_netHost = filename.partition("/")[2]
                           else:
                                  file_from_netHost = filename 
                    
                    print("hostn:" + hostn)
                    print("file_from_netHost:" + file_from_netHost)
                    try:
                           # Connect to the socket to port 80
                           c.connect((hostn.strip(' \t\r\n'),80))
                           print("after connect")
                           
                           # Create a temporary file on this socket and ask port 80
                           # for the file requested by the client
                           fileobj = c.makefile('rb', 0) 
                           
                           # Instead of using send and recv, we can use makefile
                           fileobj.write("GET "+"/" + file_from_netHost.strip(' \t\r\n') + " HTTP/1.0\n\n") 
                           
                           # Read the response into buffer
                           buf = fileobj.readlines()
                           #print(buf)
                           for each in buf:  
                                  tcpCliSock.send(each)
                           print(referedFlag)
		          
                           # make directory and Caching
                           """
                           file_path = ("www." + hostn + "/" + file_from_netHost)        
                           directory = ("www." + hostn + "/" + file_from_netHost).rpartition('/')[0]         

               
                           try:
                                  os.makedirs(directory)
                           except OSError as e:
                                  if e.errno != errno.EEXIST:
                                        raise	  
                           """

                           print("caching...") 
			 
			   # Create a new file in the cache for the requested file.
			   # Also send the response in the buffer to client socket
			   # and the corresponding file in the cache

			   if referedFlag == "true":
				  tmpFile = open("./" +  file_from_netHost, "wb")
			   else:
				  tmpFile = open("./" + filename, "wb")

			   for each in buf: 
                                  tmpFile.write(each)

			   print("finish caching")
			   tmpFile.close()

                           fileobj.close()
                           c.close()
                    except:
                           print("Illegal request") 
       
       # Close the client and the server sockets
       tcpCliSock.close()
       print("SESSION STOPPED")
       # Fill in start.
       # Fill in end.
