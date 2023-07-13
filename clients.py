import json
import random
import socket
import threading

from client import send_message

with open('client_key_values.json', 'r') as file:
    client_data = json.load(file)


def simulate_client(client_n, host, port):
    with socket.create_connection((host, port), timeout=1) as s:
        print(f"Client {client_n} is connected to server!")

        data = random.choice(client_data)
        # Send messages to the server
        messages = [
            "SET {k} {v}\n".format(k=data["key"], v=data["value"]),
            "GET {k}\n".format(k=data["key"]),
            "DELETE {k}\n".format(k=data["key"]),
        ]
        for _ in range(3):
            send_message(s, random.choice(messages))

        send_message(s, "QUIT\n")


def simulate_multiple_clients(host, port, num_clients):
    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=simulate_client, args=(i + 1, host, port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    host = '127.0.0.1'  # Server host
    port = 12345  # Server port

    # Simulate multiple clients
    num_clients = 50

    simulate_multiple_clients(host, port, num_clients)
