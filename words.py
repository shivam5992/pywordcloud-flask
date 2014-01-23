from flask import Flask, render_template, request, flash
from BeautifulSoup import BeautifulSoup
import urllib
import random

app = Flask(__name__)
app.secret_key = 'You will never guess'

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
	# create word cloud if proper url is received, error handling for url
	if request.method == 'POST':
		url = request.form['urllink']
		htmltext = urllib.urlopen(url).read()
		soup = BeautifulSoup(htmltext)

		article = ""
		for text in soup.findAll(text=True):
			article += text.encode("utf-8")
		a = getKeywords(article)
		random.shuffle(a)

		span = ""
		css  = """#box{font-family:'calibri';max-height:1000px;max-width:1000px;border:2px solid black;}
		#box a{text-decoration : none}
		"""
		
		colors = ['#607ec5','#002a8b','#86a0dc','#4c6db9']
		k = 0
		for index,item in enumerate(a):
			index += 1
			span += '<a href=#><span class="word'+str(index)+'" id="tag'+str(index)+'">' + str(item[0]) + "</span></a>\n"
			size = item[1]*item[1]*item[1]%400
			if size < 50 and k%2 != 0:
				size += 150
		 	if size > 50 and size < 100 and k%2 != 0:
				size += 100
		 	css += '#tag'+str(index)+'{font-size: '+ str(size) +'%;color: '+colors[int(k%4)]+'}\n'
		 	css += '#tag'+str(index)+':hover{color: red}\n'
		 	k += 1

		f = open('templates/wordcloud.html', 'w')
		message = """
		<link rel='stylesheet' href='static/wordcloud.css'>
		<div id='box'>
			""" + span +  """
		</div>
		"""
		f.write(message)
		f.close
		
		f = open('static/wordcloud.css', 'w')
		f.write(css)
		f.close
		flash("wordcloud created")
		return render_template('index.html')
	return render_template('index.html')
def getKeywords(articletext):
	common = open("static/common_words.txt").read().split('\n')
	word_dict = {}
	word_list = articletext.lower().split()
	for word in word_list:
		if word not in common and word.isalnum():
			if word not in word_dict:
				word_dict[word] = 1
			if word in word_dict:
				word_dict[word] += 1
	top_words =  sorted(word_dict.items(),key=lambda(k,v):(v,k),reverse=True)[0:50]
	top = []
	for w in top_words:
		top.append(w)
	return top



if __name__ == '__main__':
	app.run(debug = True)
