import sys
sys.path.append('../')
import json
import redis
from config import KAFKA_HOST, KAFKA_PORT, TOPIC_NAME
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT), value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_message(message):
	producer.send(TOPIC_NAME, message)
