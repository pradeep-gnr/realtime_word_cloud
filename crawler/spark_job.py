import json
import os
from operator import add
import sys
sys.path.append('../')
from config import SPARK_HOME, BATCH_DURATION, KAFKA_HOST, KAFKA_PORT, TOPIC_NAME, ZOOKEEPER_HOST, ZOOKEEPER_PORT
from parse_page import crawl_amazon_url
from database import redis_utils

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = SPARK_HOME

if os.path.join(SPARK_HOME,'python') not in sys.path:
    sys.path.insert(0, os.path.join(SPARK_HOME, 'python'))

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

sc = SparkContext(appName="AmazonWordCloud")
#sc.setLogLevel("DEBUG")

ssc = StreamingContext(sc, BATCH_DURATION)

# Must add checkPointing feature to make streaming more resilient.
ssc.checkpoint("checkpoint")
kafkaStream = KafkaUtils.createStream(ssc, '{}:{}'.format(ZOOKEEPER_HOST, ZOOKEEPER_PORT), 'spark-streaming-consumer', {TOPIC_NAME:1})
parsed = kafkaStream.map(lambda v: json.loads(v[1]))

parsed.pprint()
parsed = parsed.map(crawl_amazon_url)
parsed.pprint()
# Get WordCount for the minibatch.
counts = parsed.flatMap(lambda x:x).map(lambda x: (x,1)).reduceByKey(lambda a, b: a + b)

def write_rdd_to_redis(counts):	
	counts = counts.collect()
	print counts
	for word, count in counts:
		redis_utils.update_word_counts([(word, count)])

counts.pprint()
counts.foreachRDD(write_rdd_to_redis)
ssc.start()
ssc.awaitTermination()