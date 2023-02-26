import socket
import struct


def send_msg(socket: socket.socket, msg: bytes) -> None:
    """Function to write the specified byte sequence to the socket

    Args:
        socket (socket.socket): Socket instance
        msg (bytes): Byte sequence
    """
    total_sent_len = 0
    total_msg_len = len(msg)
    while total_sent_len < total_msg_len:
        sent_len = socket.send(msg[total_sent_len:])
        if sent_len == 0:
            raise RuntimeError("socket connection broken")
        total_sent_len += sent_len

def receive_msg(socket:socket.socket, total_msg_size: int) -> bytes:
    """Generator function that reads a string of bytes from the socket until the end of the connection

    Args:
        socket (socket.socket): Socket instance
        total_msg_size (int): Byte sequence length

    Yields:
        Iterator[bytes]: Received byte sequence
    """
    total_recv_size = 0
    while total_recv_size < total_msg_size:
        received_chunk = socket.recv(total_msg_size - total_recv_size)
        if len(received_chunk) == 0:
            raise RuntimeError("socket connection broken")
        yield received_chunk
        total_recv_size += len(received_chunk)



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("127.0.0.1", 54321))
    server_socket.listen()
    print("start")
    client_socket, (client_address, client_port) = server_socket.accept()
    print(f"accepted from {client_address}:{client_port}")
    received_msg = b"".join(receive_msg(client_socket, total_msg_size=8))
    print(f"received: {received_msg}")
    (operand1, operand2) = struct.unpack("!ii", received_msg)
    print(f"operand1: {operand1}, operand2: {operand2}")
    result = operand1 + operand2
    print(f"result: {result}")
    result_msg = struct.pack("!q", result)
    send_msg(client_socket, result_msg)
    print(f"sent: {result_msg}")
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
