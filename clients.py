import json
import random
import socket
import threading
from time import sleep

from client import send_message

with open('client_key_values.json', 'r') as file:
    client_data = json.load(file)


def simulate_client(client_n, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        s.connect((host, port))
        print(f"Client {client_n} is connected to server!")

        data: dict = random.choice(client_data)
        # Send messages to the server
        messages = [
            "SET {k} {v}\n".format(k=data["key"], v=data["value"]),
            "GET {k}\n".format(k=data["key"]),
            "DELETE {k}\n".format(k=data["key"]),
        ]
        sending_messages = []
        for _ in range(3):
            sending_messages.append(random.choice(messages))
        str_messages = "".join(sending_messages)
        send_message(s, str_messages)

        sleep(5)
        send_message(s, "QUIT\n")


def simulate_multiple_clients(host, port, num_clients):
    threads = []
    for i in range(num_clients):
        threads.append(
            threading.Thread(target=simulate_client, args=(i + 1, host, port))
        )
        threads[-1].start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    host = '127.0.0.1'  # Server host
    port = 12345  # Server port

    # Simulate multiple clients
    num_clients = 20

    simulate_multiple_clients(host, port, num_clients)
