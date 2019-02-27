from socket import *
import sys, os, errno



if len(sys.argv) <= 1:
       print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP \
Address Of Proxy Server')
       sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverPort = int(sys.argv[2])

# Error check bind()
try: 
       tcpSerSock.bind((sys.argv[1], serverPort))
except:
       print("Error: Bind failed, probably address already in use")
       sys.exit(1)

tcpSerSock.listen(1)
# Data structure to store cache date (website as key, time as value)
cache_dict = {} 
 
while 1:

       # Start receiving data from the client
       print('Ready to serve...')
       tcpCliSock, addr = tcpSerSock.accept()
       print('Received a connection from:', addr)
       tcpCliSock.settimeout(2)

       # recv() to non-blocking      
       try: 
              orig_message = tcpCliSock.recv(1024).decode()
       except timeout:
              print("recv() timed out, reconnecting...")
              tcpCliSock.close()
              continue 
      
       #print(orig_message)
       message = orig_message
       #print(message)

       # Extract the filename from the given message
       #print(message.split()[1])
       print(message)
       filename = message.split()[1].partition("/")[2].strip(' \t\n\r')

       # Appends index.html if request ends with "/"
       if filename.endswith("/"):
              filename = filename + "index.html"

       print("filename:" + filename)
       fileExist = "false"
       referedFlag = "false"
       modifiedFlag = "false" 

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
              referLine = referLine.strip(' \t\r\n')
              #print("referLine: " + referLine)
              hostn = referLine.replace("www.", "", 1).split("/", 1)[0].strip(' \t\r\n') 
              print("referLine: " + referLine)
              if referLine in filename: 
                     file_from_netHost = filename.partition("/")[2].strip(' \t\r\n')
                     print("refer in filename: " + file_from_netHost) 
              else:
                     print("hi")
                     file_from_netHost = filename.strip(' \t\r\n')
                   
       else:
              hostn = filename.replace("www.","",1).split("/", 1)[0].strip(' \t\r\n')
              file_from_netHost = filename.partition("/")[2].strip(' \t\r\n') 
 
       # Parse out file_path and directory       
       file_path = hostn + "/" + file_from_netHost
       print(file_path)
       directory = file_path.rpartition('/')[0]

       try:
             getConditional = socket(AF_INET, SOCK_STREAM)                                       
             getConditional.connect((hostn, 80))
             fileobj = getConditional.makefile('rb', 0) 

             # Check wether the file exist in the cache
             if file_from_netHost != "":
                    # Get Conditional
                    print("HIHIHIH")
                    print(file_path)
                    print(cache_dict)
                    if file_path not in cache_dict:
                           print("conditional throw exception")
                           raise Exception  
                    print("GET "+"/" + file_from_netHost + " HTTP/1.0\n" \
                                 + "If-Modified-Since: " + cache_dict[file_path] + "\n\n" )
                    fileobj.write("GET "+"/" + file_from_netHost + " HTTP/1.0\n" \
                                 + "If-Modified-Since: " + cache_dict[file_path] + "\n\n" ) 
                    
                    buf = fileobj.read()
                    print(buf)
                    if "304 Not Modified" not in buf:
                           print("HIHIHIH@@@@")
                           raise Exception 
                    
                    openFile = file_path
             else:
                    # Get Conditional
                    print("BYEBYEBYE") 
                    print(filename)
                    print(cache_dict)
                    if filename not in cache_dict:
                           raise Exception  
                    fileobj.write("GET "+"/" + file_from_netHost + " HTTP/1.0\n" \
                                 + "If-Modified-Since: " + cache_dict[filename] + "\n\n" ) 
                    buf = fileobj.read()
                    print(buf)
                    if "304 Not Modified" not in buf:
                           raise Exception 
                           
                    openFile = filename

             f = open(openFile, "r")

             outputdata = f.readlines()
             fileExist = "true"
             local_flag = "false"
  
             # if this is a local flag 
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
             # tcpCliSock.send("HTTP/1.0 200 OK\r\n")
             
	     if local_flag == "false": 
                    for each in outputdata:
                           tcpCliSock.send(each)
             else:
                    #if in outputdata[0]
                    tcpCliSock.send("HTTP/1.0 200 OK\r\n")
                    tcpCliSock.send("Content-Type: text/html\r\n")
                    for each in outputdata:
                           tcpCliSock.send(each)

             f.close()
             
             print('Read from cache')
       # Error handling for file not found in cache
       except (IOError, Exception):
             if fileExist == "false":
                    # Create a socket on the proxyserver
                    c = socket(AF_INET, SOCK_STREAM) # Fill in start.# Fill in end.
                                       
                    print("hostn:" + hostn)
                    print("file_from_netHost:" + file_from_netHost)
                    try:
                           # Connect to the socket to port 80
                           c.connect((hostn, 80))
                           print("after connect")
                           
                           # Create a temporary file on this socket and ask port 80
                           # for the file requested by the client
                           fileobj = c.makefile('rb', 0) 
                           
                           # Instead of using send and recv, we can use makefile
                           fileobj.write("GET "+"/" + file_from_netHost + " HTTP/1.0\n\n") 
                           
                           # Read the response into buffer
                           buf = fileobj.readlines()
                           fullBuf = fileobj.read()
                           #print(buf)
                           
                           for each in buf:  
                                  tcpCliSock.send(each)
                             #     print(each)

                           #print(referedFlag)
		           #for each in buf:
                           #      print(each)                    

			   print("caching...")
			  
			   # Parse Last-Modified Date:
		           if "Last-Modified" in fullBuf:
		                  for each in buf:
                                         if "Last-Modified" in each: 
                                                date = each.split(' ', 1)[1].strip('\t\r\n')
				                break
                           else:
                                  for each in buf:
                                         if "Date" in each:
                                                date = each.split(' ', 1)[1].strip('\t\r\n')
                                                break
 
                           """
                           # makes directory 			
                  	   try:
			          print("making directory")
			          print(directory)
			          os.makedirs(directory)
			   except OSError as e:
			          if e.errno != errno.EEXIST:
			                 raise
                           """
			   # Create a new file in the cache for the requested file.
			   if file_from_netHost != "":
			          
                                  # makes directory 			
                  	          try:
			                 print("making directory")
			                 print(directory)
			                 os.makedirs(directory)
			          except OSError as e:
			                 if e.errno != errno.EEXIST:
			                       raise
                                  
                       	          print("Directory created") 
				  print("create file: " + file_path)
				  print(date)
				  cache_dict[file_path] = date
				  print("create file: " + file_path)
				  tmpFile = open(file_path, "wb")
			   else:  
                                  print("KIKIKI")
                                  print(date)
                                  cache_dict[filename] = date
                                  print("AFTER")
				  tmpFile = open("./" + filename, "wb")
				  print("create file: " + "./" + filename)

			   for each in buf: 
				  tmpFile.write(each)

			   print("finish caching")
			   tmpFile.close()

                           fileobj.close()
                           c.close()
                    except:
                           print("Illegal request")
                         #  tcpCliSock.send("HTTP/1.0 400 Bad Request\r\n")

       # Close the client and the server sockets
       print(cache_dict)
       tcpCliSock.close()
       print("SESSION STOPPED")
