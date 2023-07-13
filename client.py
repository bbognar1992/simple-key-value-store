import socket


def send_message(client, message):
    client.sendall(message.encode())

    response = ""
    while True:
        try:
            chunk = client.recv(1024).decode()
            if not chunk:
                break
            response += chunk
        except socket.timeout:
            break
    print(f"Send to server: {message}")
    print(f"Client received: {response}")


if __name__ == '__main__':
    host = '127.0.0.1'  # Server host
    port = 12345  # Server port

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        s.connect((host, port))
        send_message(s, "SET a b\n")
        send_message(s, "GET a\n")
        send_message(s, "DELETE a\n")
        send_message(s, "QUIT\n")
        send_message(s, "SET a b\n")
