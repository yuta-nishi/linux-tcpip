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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 54321))
    operand1, operand2 = 1000, 2000
    print(f"operand1: {operand1}, operand2: {operand2}")
    request_msg = struct.pack("!ii", operand1, operand2)
    send_msg(client_socket, request_msg)
    print(f"sent: {request_msg}")
    received_msg = b"".join(receive_msg(client_socket, total_msg_size=8))
    print(f"received: {received_msg}")
    (added_value, ) = struct.unpack("!q", received_msg)
    print(f"result: {added_value}")
    client_socket.close()


if __name__ == "__main__":
    main()
