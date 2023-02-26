import socket


def send_msg(socket: socket.socket, msg: bytes) -> None:
    """Function to write the specified byte sequence to the socket

    Args:
        socket (socket.socket): Socket
        msg (bytes): Byte sequence
    """
    total_sent_len = 0
    total_msg_len = len(msg)
    while total_sent_len < total_msg_len:
        sent_len = socket.send(msg[total_sent_len:])
        if sent_len == 0:
            raise RuntimeError("socket connection broken")
        total_sent_len += sent_len

def receive_msg(socket:socket.socket, chunk_len=1024) -> bytes:
    """Generator function that reads a string of bytes from the socket until the end of the connection

    Args:
        socket (socket.socket): Socket
        chunk_len (int, optional): Number of bytes to specify. Defaults to 1024.

    Yields:
        Iterator[bytes]: Received byte sequence
    """
    while True:
        received_chunk = socket.recv(chunk_len)
        if len(received_chunk) == 0:
            break
        yield received_chunk


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("127.0.0.1", 54321))
    server_socket.listen()
    print("start")
    client_socket, (client_address, client_port) = server_socket.accept()
    print(f"accepted from {client_address}:{client_port}")
    for received_msg in receive_msg(client_socket):
        send_msg(client_socket, received_msg)
        print(f"echo: {received_msg}")
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
