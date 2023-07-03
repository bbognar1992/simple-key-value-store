import asyncio

store = dict()


async def get_key(key):
    global store
    return store.get(key)


async def set_key(key, value):
    global store
    store.update({key: value})


async def delete_key(key):
    global store
    del store[key]


async def handle_client(reader, writer):
    global store
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode().strip()

        input_list: list = message.split(" ")
        command = input_list.pop(0)
        key = input_list.pop(0)
        response: str = "Not OK!"
        if command == 'GET':
            value = await get_key(key)
            if value:
                response = value
            else:
                response = f"Key not exists: {key}"
        elif command == 'SET':
            await set_key(key, input_list.pop(0))
            response = "OK"
        elif command == 'DELETE':
            if key in store:
                await delete_key(key)
                response = "OK"
            else:
                response = f"Key not exists: {key}"
        else:
            print(f"Wrong command: {command}")

        print(f"Received message: {message}")

        print(f"Store: {store}")
        print(response)
        writer.write(response.encode())
        await writer.drain()

    writer.close()


async def main():
    port = 12345
    host = '127.0.0.1'
    server = await asyncio.start_server(
        handle_client, host, port
    )
    print(f'Serving on {port}')
    async with server:
        await server.serve_forever()


asyncio.run(main())
