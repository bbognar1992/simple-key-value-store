import asyncio


async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode().strip()
        print(f"Received message: {message}")

        response = "OK"
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
