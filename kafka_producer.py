import os
import json
from dto import *
from typing import Any
from aiokafka import AIOKafkaProducer


async def send_topic(producer: AIOKafkaProducer, topic: str, data: dict):
    await producer.send_and_wait(
        topic=topic,
        value=data
    )
    return


async def send_topics(producer: AIOKafkaProducer, topic: str, data: list):
    assert isinstance(data, list)    
    for elem in data:
        await producer.send(
            topic=topic,
            value=elem
        )
    producer.flush()
    return


async def send(producer: AIOKafkaProducer, topic: str, data: Any):
    if isinstance(data, list):
        await send_topics(producer=producer, topic=topic, data=data)
    await send_topic(producer=producer, topic=topic, data=data)


async def initialize_producer():
    producer = AIOKafkaProducer(
        acks=1,
        compression_type='gzip',
        bootstrap_servers=[
            f"{os.environ['KAFKA_BROKER_0']}",
            f"{os.environ['KAFKA_BROKER_1']}",
            f"{os.environ['KAFKA_BROKER_2']}"
        ],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        api_version="0.10.1"
    )
    return producer
