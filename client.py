import random
import socket
import threading


def simulate_client(client_n, host, port):
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send messages to the server
    messages = [
        f"SET a {client_n}", "GET a", "DELETE a",
        f"SET b {client_n}", "GET b", "DELETE b",
        f"SET c {client_n}", "GET c", "DELETE c",
        f"SET d {client_n}", "GET d", "DELETE d",
        f"SET e {client_n}", "GET e", "DELETE e",
        f"SET f {client_n}", "GET f", "DELETE f",

    ]

    for _ in range(2):
        message = random.choice(messages)
        client_socket.sendall(message.encode())
        # Receive and print the response from the server
        response = client_socket.recv(1024).decode()

        print(f"Client {client_n} sent message: {message}")
        print(f"Client {client_n} received message: {response}")

    # Close the connection
    client_socket.close()


def simulate_multiple_clients(host, port, num_clients):
    for i in range(num_clients):
        threading.Thread(target=simulate_client, args=(i + 1, host, port)).start()


if __name__ == '__main__':
    host = '127.0.0.1'  # Server host
    port = 12345  # Server port

    # Simulate multiple clients
    num_clients = 20

    simulate_multiple_clients(host, port, num_clients)
