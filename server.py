"""
Server program for my networking module
"""
import socket
import threading

# Define the constants
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS =(SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(conn, addr):
    """
    When a connection is made with a client, begin to
    handle messages
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # While the client is connected, receive
    # and decode messages to print
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            # If a deconnect message is sent, end the connection
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            print(f"They said: {msg}")
            
        # Asks the user for a message to send
        server_message = input("Send a message: ")
        # If the message was end, close the connection
        if server_message.lower() == "end":
            # Sends a disconnect message to the server
            send(DISCONNECT_MESSAGE, conn)
            connected = False
        send(server_message, conn)
        
    conn.close()
    
def send(msg, conn):
    """
    Sends a message to the server. First sends a 
    header message to tell the server how large 
    the incoming message will be.
    """
    # Encodes the message
    message = msg.encode(FORMAT)
    # Creates the header
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    # Sends the header first
    conn.send(send_length)
    # Sends the message
    conn.send(message)

def start():
    """
    To start the server, run this function. The server will
    begin to listnen for connections and accept them.
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print("Type END if you wish to disconnect")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
   

# Print a message to show the program has started
print("[STARTING] server is starting...")
start()


