import asyncio
import logging
from typing import Dict

logger = logging.getLogger("simple-key-value-store")
store: Dict[str, str] = {}
store_lock = asyncio.Lock()


async def get_key(key: str) -> str:
    async with store_lock:
        try:
            return store[key]
        except KeyError:
            return f"Key not found: {key}"


async def set_key(key: str, value: str) -> str:
    async with store_lock:
        store[key] = value
    return "OK"


async def delete_key(key: str) -> str:
    async with store_lock:
        try:
            del store[key]
        except KeyError:
            return f"Key not found: {key}"
        else:
            return "OK"


async def read_data(reader: asyncio.StreamReader) -> str:
    data = b''
    while True:
        chunk = await reader.read(1024)
        data += chunk
        if not chunk:
            break
    return data.decode().strip()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        command = (await reader.readuntil(b' ')).decode().strip()
        if command not in {"GET", "SET", "DELETE"}:
            raise ValueError(f"Invalid command: {command}")

        if command == "SET":
            key = (await reader.readuntil(b' ')).decode().strip()
        else:
            key = (await reader.read(257)).decode().strip()

        if command == "SET":
            data = await read_data(reader)
            response = await set_key(key, data)
        elif command == 'GET':
            response = await get_key(key)
        elif command == 'DELETE':
            response = await delete_key(key)

        logger.info(f"Received message: {command} {key}")
        logger.debug(f"Store: {store}")

    except Exception as e:
        response = str(e)
        logger.error(response)
    finally:
        # Encode the response string and write it to the writer
        writer.write(response.encode())
        # Ensure that the response data is sent to the client
        await writer.drain()
        writer.write_eof()
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
