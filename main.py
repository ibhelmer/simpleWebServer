# Example of a simple web server
# This web server only supports one client at a time an one request per client
# It only supports GET requests and HTTP/1.0
# Ib helmer Nielsen, UCN october 2023

#import socket module
from socket import *    # Import socket module
import sys              # In order to terminate the program
import logging as DEBUG # For debugging purposes make a log file

def main() -> int:
   DEBUG.basicConfig(filename='websrv.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=DEBUG.INFO)
   serverSocket = socket(AF_INET, SOCK_STREAM)
   # Prepare a sever socket
   HOST = "127.0.0.1"               # Only runs on Local loop back interface
   PORT = 7913                      # User Port number
   serverSocket.bind(('', PORT))    # Bind the server to te port
   serverSocket.listen()            # Listen for connections

   while True:
      # Establish the connection
      DEBUG.info('Ready to serve...')
      connectionSocket, addr = serverSocket.accept() # Accept a connection
      DEBUG.info(addr)                               # Print the address of the client to log file
      try:
         message = connectionSocket.recv(1024)       # Receive the request message from the client
         filename = message.split()[1]               # Extract the path of the requested object from the message
         flen = len(filename)                        # Get the length of the filename
         if  flen <= 1:                              # If the filename is empty
            filename=b'/index.html'                  # Set the filename to index.html in no other is given
         if filename!= b'/favicon.ico':              # If the filename is not favicon.ico
            with open(filename[1:], "rb") as f:      # Open the file  in binary mode
               data = f.read()                       # Read the file
            #Send one HTTP header line into socket
            response='HTTP/1.0 200 OK\r\n\r\n'.encode('utf-8')+data+"\r\n".encode() # Create the response
            connectionSocket.sendall(response)       # Send the response
            connectionSocket.close()                 # Close the connection
         else:
           with open(filename[1:], "rb") as f:       # If filenamen given is favicon.ico Open the file in binary mode
               data = f.read()                       # Read the file
           response = 'HTTP/1.1 200 OK\r\nContent-Type: image/vnd.microsoft.icon\r\n\r\n'.encode('utf-8') + data + "\r\n".encode()
           connectionSocket.sendall(response)        # Send the response
           connectionSocket.close()                  # Close the connection
      except IOError:
      #Send response message for file not found
         connectionSocket.send('HTTP/1.0 404 OK\r\n\r\n'.encode('utf-8'))
         connectionSocket.send('404 Not Found'.encode())
         connectionSocket.send("\r\n".encode())
         print("404 send")
         connectionSocket.close()       # Close client socket
if __name__ == '__main__':
   main()                               # Run the main function
   serverSocket.close()                 # Close the socket
   sys.exit()                           # Terminate the program after sending the corresponding data

