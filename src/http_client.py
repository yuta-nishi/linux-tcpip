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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 80))
    request_text = "GET / HTTP/1.0\r\n\r\n"
    request_bytes = request_text.encode("ASCII")
    send_msg(client_socket, request_bytes)
    received_bytes = b"".join(receive_msg(client_socket))
    received_text = received_bytes.decode("ASCII")
    print(received_text)
    client_socket.close()

if __name__ == "__main__":
    main()
