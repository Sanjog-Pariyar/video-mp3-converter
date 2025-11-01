import asyncio
import aio_pika
import aio_pika.abc

from app.utils.convert import convert_video_to_audio

from app.config import settings
import json


async def main(loop):
    # Connecting with the given parameters is also possible.
    # aio_pika.connect_robust(host="host", login="login", password="password")
    # You can only choose one option to create a connection, url or kw-based params.
    connection: aio_pika.abc.AbstractRobustConnection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL, loop=loop
    )

    async with connection:
        queue_name = "video"

        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            auto_delete=False
        )

        print("ready to receive messages")

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body)
                    await convert_video_to_audio(data)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()