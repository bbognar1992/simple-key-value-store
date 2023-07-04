import json
import random
import socket
import threading

with open('client_key_values.json', 'r') as file:
    client_data = json.load(file)


def simulate_client(client_n, host, port):
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data: dict = random.choice(client_data)
    # Send messages to the server
    messages = [
        "SET {k} {v}".format(k=data["key"], v=data["value"]),
        "GET {k}".format(k=data["key"]),
        "DELETE {k}".format(k=data["key"]),
    ]

    message = random.choice(messages)
    client_socket.send(message.encode())
    client_socket.shutdown(1)
    # Receive and print the response from the server
    response = client_socket.recv(102400).decode()

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
