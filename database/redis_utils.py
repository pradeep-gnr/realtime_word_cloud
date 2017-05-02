import sys
sys.path.append('../')
import redis
from config import REDIS_HOST, REDIS_PORT, URLS_DB, WORD_CLOUD_DB, WORD_CLOUD_SET

# Initialize Redis clients.
redis_urls_cli = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=URLS_DB)
redis_wcloud_cli = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=WORD_CLOUD_DB)


def check_redis_connection():
    rs = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    try:
        rs.get(None)  # getting None returns None or throws an exception
    except (redis.exceptions.ConnectionError, 
        redis.exceptions.BusyLoadingError):
        return False
    return True

def add_url(url):
	"""
		We use a HyperLog datastructure in Redis to store visited URLS.				
	"""
	# Checks if the approximate cardinality estimation on the addition of the new url.
	# This function returns 1 of the approximate cardinality of the hyperlog data structure has changed.
	has_changed = redis_urls_cli.pfadd(url)
	if has_changed==1:
		# A new URL and not a duplicate.
		return False
	return True

def update_word_counts(word_counts):
	"""
		A list of tuples of the form [(w1,c1)...].
		This function updates the counts of words in a sorted set stored in redis.
		Each insert takes O(Log N) where N is the number of elements in the set.		
	"""
	for word, count in word_counts:
		redis_wcloud_cli.zadd(WORD_CLOUD_SET,word,count)

def fetch_top_k_words(k):
	"""
		Fetches top K words from the sorted set based on word count.
	"""
	return redis_wcloud_cli.zrange(WORD_CLOUD_SET,0,k,desc=True,withscores=True)


if __name__=="__main__":
	status = check_redis_connection()
	create_db_if_not_exists('crap')
	print status

