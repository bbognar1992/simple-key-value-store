import socket
import threading


def simulate_client(client_n, host, port):
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send messages to the server
    messages = ["SET a AAA", "GET a", "DELETE a"]

    for message in messages:
        client_socket.sendall(message.encode())
        print(f"Client {client_n} sent message: {message}")
        # Receive and print the response from the server
        response = client_socket.recv(1024).decode()
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
    num_clients = 5

    simulate_multiple_clients(host, port, num_clients)
