# -*- coding: utf-8 -*-
import sys
from web_app.main import app
from database.redis_utils import check_redis_connection
import redis

# Initialize Redis databases.
if not check_redis_connection():
	sys.exit("Aborting: Redis Server does not seem to be running. Please start redis server.")

app.run()
