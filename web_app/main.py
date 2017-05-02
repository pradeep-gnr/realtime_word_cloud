import sys
sys.path.append("../")
from config import MAX_NUM_WORDS
from crawler.parse_page import crawl_amazon_url
from database import redis_utils, kafka_utils
from flask import Flask, render_template, request
from flask import jsonify
from functools import wraps

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.route("/index.html")
def hello():
    return render_template('static/index.html')

@app.route("/get_word_cloud_data",methods=['GET'])
def get_word_cloud_data():
	word_cloud_data = redis_utils.fetch_top_k_words(MAX_NUM_WORDS)
	return jsonify(word_cloud_data)

@app.route("/", methods=['GET','POST'])
def crawl_url():
	url = request.args.get('url')
	if redis_utils.add_url(url):
		# Duplicate. URL already exists in Redis
		print "URL: {} is a Duplicate and has already been crawled.".format(url)
		return jsonify({'status': 'success', 'is_duplicate': True})
	try:
		# Send URLS to Kafka.
		print "Putting Messages in Kafka topics"
		kafka_utils.send_message(url)
		response = jsonify({'status': 'success', 'is_duplicate': False})
	except Exception as error:
		print('Exception: {}' + repr(error))
		response = jsonify({'status': 'failure', 'is_duplicate': False})
	
	return response
		

if __name__ == "__main__":
    app.run()
