"""
Client program for my networking module
"""
import socket

# Defining constants
HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

# Create a client socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(msg):
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
    client.send(send_length)
    # Sends the message
    client.send(message)


def main():
    """
    Starts a loop that allows the user to send
    messages to the server. The program ends when
    the user types END.
    """
   # Instruct user how to break the loop
    print("Type END to quit")
    # Runs a loop till the user decides to quit
    connected = True
    while connected:

        # Creates message as input from user
        message = input("Type message: ")
        # Ends the loop if the user typed end
        if message.lower() == "end":
            # Sends a disconnect message to the server
            send(DISCONNECT_MESSAGE)
            connected = False
        # Sends the typed message
        else:
            send(message)

        # Receives a message from the server
        # Starts with receiving the header, then
        # the message and prints the message
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            print(f"They said: {msg}")


# Run the program
if __name__ == "__main__":
    main()
