from nltk import word_tokenize
from nltk.corpus import stopwords

def tokenize(text):
	tokens = word_tokenize(text)
	words = [w.lower() for w in tokens if w.isalnum()]
	return words

def filter_stop_words(tokens):
	filtered_words = [word for word in tokens if word not in stopwords.words('english')]
	return filtered_words

if __name__=="__main__":
	print filter_stop_words(tokenize("A sample sentence to be tokenzied."))