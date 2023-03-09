import os
from typing import Any
from kafka import KafkaProducer

producer = KafkaProducer(
    acks=0,
    compression_type='gzip',
    bootstrap_servers=[
        f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}"
    ]
)

async def send_topic(topic: str, data: dict):
    producer.send(
        topic,
        data
    )
    producer.flush()
    return


async def send_topics(topic: str, data: list):
    assert isinstance(data, list)    
    for elem in data:
        producer.send(
            topic,
            elem
        )
    producer.flush()
    return


async def send(topic: str, data: Any):
    if isinstance(data, list):
        await send_topics(topic=topic, data=data)
    await send_topic(topic=topic, data=data)
