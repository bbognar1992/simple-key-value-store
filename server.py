import asyncio
import logging
from typing import List, Dict

logger = logging.getLogger("simple-key-value-store")
store: Dict[str, str] = {}


async def get_key(key: str) -> str:
    try:
        return store[key]
    except KeyError:
        return f"Key not found: {key}"


async def set_key(key: str, value: str) -> str:
    store[key] = value
    return "OK"


async def delete_key(key: str) -> str:
    try:
        del store[key]
    except KeyError:
        return f"Key not found: {key}"
    else:
        return "OK"


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    while True:
        # Read data from the client
        data = await reader.read(1024)

        # If no more data is received, break the loop and exit
        if not data:
            break

        # Decode the received data and remove leading/trailing whitespaces
        message = data.decode().strip()

        # Split the message into a list of strings based on spaces
        input_list: List[str] = message.split(" ")

        # Extract the command and key from the input list
        command = input_list.pop(0)
        key = input_list.pop(0)

        response: str
        try:
            if command == 'GET':
                response = await get_key(key)
            elif command == 'SET':
                response = await set_key(key, input_list.pop(0))
            elif command == 'DELETE':
                response = await delete_key(key)
            else:
                raise ValueError(f"Invalid command: {command}")
        except Exception as e:
            response = str(e)
            logger.error(response)

        logger.info(f"Received message: {message}")
        logger.info(f"Store: {store}")
        logger.info(f"Response: {response}")

        # Encode the response string and write it to the writer
        writer.write(response.encode())

        # Ensure that the response data is sent to the client
        await writer.drain()

    writer.close()


async def main() -> None:
    port = 12345
    host = '127.0.0.1'

    logging.basicConfig(level=logging.INFO)

    server = await asyncio.start_server(handle_client, host, port)
    logger.info(f'Serving on {port}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
