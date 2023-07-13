# simple-key-value-store

## Task
The task is to build a TCP server that acts as a simple key-value store. The server should handle multiple client connections concurrently using asyncio.

## Supported commands
`GET <key>`: Retrieves the value associated with a given key.

`SET <key> <value>`: Sets the value for a given key.

`DELETE <key>`: Deletes the key-value pair associated with a given key.


## Requirements:
1. Server should handle multiple connections
2. Clients should be able to get the value of a key, set the value of a key, and delete a key-value pair.
3. Server should send appropriate error messages to the client if there is any issue
4. The server should persist the key-value stored in memory (e.g., using a dictionary).
## Usage
Following would start a server in background.

```$ python server.py & ```

 Once server is started run single client or multiple clients as follows:

```$ python client.py ```

```$ python clients.py ```