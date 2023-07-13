import asyncio
import logging
from typing import Dict

logger = logging.getLogger("simple-key-value-store")
store: Dict[str, str] = {}


class QuitCommand(Exception):
    pass


async def process_get_command(line: str) -> str:
    key = line.removeprefix("GET ").strip()
    return store.get(key, f"Key not found: {key}")


async def process_set_command(line: str) -> str:
    tmp = line.removeprefix("SET ")
    index_sep = tmp.index(" ")
    key = tmp[:index_sep].strip()
    value = tmp[index_sep:].strip()
    store[key] = value
    return "OK"


async def process_delete_command(line: str) -> str:
    key = line.removeprefix("DELETE ").strip()
    try:
        del store[key]
    except KeyError:
        return f"Key not found: {key}"
    else:
        return "OK"


async def process_line(line: str) -> str:
    if line.startswith("GET "):
        response = await process_get_command(line)
    elif line.startswith("SET "):
        response = await process_set_command(line)
    elif line.startswith("DELETE "):
        response = await process_delete_command(line)
    elif line.startswith("QUIT"):
        raise QuitCommand()
    else:
        raise ValueError(f"Invalid command in line: {line}")
    return response


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        buffer = ""
        while True:
            chunk = await asyncio.wait_for(
                reader.read(1024), timeout=60 * 5
            )
            if not chunk:
                break

            buffer += chunk.decode()
            while "\n" in buffer:
                index = buffer.index("\n")
                line = buffer[:index]
                buffer = buffer[index + 1:]

                response = await process_line(line)
                response += "\n"
                writer.write(response.encode())

                logging.info(
                    f"Input:\n{line}\n"
                    f"Output:\n{response}\n"
                    f"Store:\n{store}"
                )

    except QuitCommand:
        logger.info("Client close connection!")
        writer.write(b'OK\n')
    except ConnectionError:
        logger.error("Abrupt disconnections from client")
    except asyncio.TimeoutError:
        logger.error("Client is inactive!")
    except Exception as err:
        response = str(err)
        logger.error(response)
        writer.write(response.encode())
    finally:
        writer.close()
        await writer.wait_closed()


async def main() -> None:
    port = 12345
    host = '127.0.0.1'

    logging.basicConfig(level=logging.INFO)

    server = await asyncio.start_server(handle_client, host, port)
    logger.info(f'Serving on {port}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
