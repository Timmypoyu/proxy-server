Name: Po-Yu (Timmy), Wu 
UNI: pw2440 
Computer Network 
-------------------------------------------
Command Line: python2.7 proxy_server.py [ip-address(localhost)] [Port #]
Testing websites: www.google.com, www.columbia.edu/~pw2440
Part 1:
This part work sa the instruction intended. 
A simple proxy server with added functionality:
(1) Nested Folders for caching: The program created nested folders 
    for cache files so that the cached items can be properly retrieved. 
(2) Catch browser's multiple requests (not referred or referred):
    The program differentiates between an intial browser http request and 
    subsequent referred http requests (such as, images and favicon.ico).
(3) Sending the http response line by line, instead for a entire chunk 

Part 2:
Error handling:
    Sometimes, the browser makes connection anticipating that some data are coming;
    therefore, the program is blocked at the recv(). The error handling set a
    timeout for the recv() function, and if two seconds passed by without receiving 
    any data, then the program will wait to accept new connections. 

Part 3:
Cache Verification: 
    Use a dictionary to keep track of file and of their last modified date (if
    there is no last-modified data, used the "Date" line), and then subsequently 
    insert the data in the dictionary in the If-Modified-Since request that is sent
    right before retrieving cache.
    If recieved "304 Not Modified", retrieve the cached data.
    If doesn't recieved "304", then retrieve the data from the original server again. 

