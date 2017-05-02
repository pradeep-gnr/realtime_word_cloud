# -*- coding: utf-8 -*-

import os
from datetime import timedelta

__basedir__ = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = 'real_time_word_cloud'

# Redis Configuration.
REDIS_HOST='localhost'
REDIS_PORT=6379
URLS_DB=1
WORD_CLOUD_DB=2
WORD_CLOUD_SET='wordcloud'

# Kafka Configuration.
# This is just a basic Kafka configuration for Demo purposes.
KAFKA_HOST='localhost'
KAFKA_PORT=9092
TOPIC_NAME='amazon_products'

# Zoo Keeper Configuration.
ZOOKEEPER_HOST='localhost'
ZOOKEEPER_PORT='2181'

#### Spark Settings ####
SPARK_HOME='/usr/local/spark/'
# Batch duration in seconds.
BATCH_DURATION=3

##### WordCloud settings #####
##### Fetch the top 100 words.
MAX_NUM_WORDS =  100




