'''

Python implementation of HTML wordcloud of words collected from
a website, Paragraph Input or File Upload. Flask Web App implementation
of the same.

Author: Shivam Bansal
Email: shivam5992@gmail.com
Website: www.shivambansal.com 
Version: 0.1

'''

from flask import Flask, render_template, request, flash, redirect, url_for
from BeautifulSoup import BeautifulSoup
import urllib
import random

app = Flask(__name__)
app.secret_key = 'You will never guess'

'''
Index router function, Receive post request and displays the html wordcloud
'''
@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():

	if request.method == 'POST':
		
		''' Store post variables '''
		url = request.form['urllink']
		area = request.form['textarea']
		case = request.form['case']
		show_freq = request.form['show_freq']
		
		''' Try to connect with the URL '''
		try:
			if not url.startswith("http"):
				url = "http://" + url
			htmltext = urllib.urlopen(url).read()
		except:
			flash("Cannot connect to the requested url")
			return redirect(url_for('startover'))	
		
		''' Get all text from the html repsonse ''' 
		soup = BeautifulSoup(htmltext)
		article = ""
		for text in soup.findAll(text=True):
			article += text.encode("utf-8")
		
		''' Get top keywords '''
		freq = 50
		a = getKeywords(article, case, freq)
		random.shuffle(a)

		''' Craete html span tags and corresponding css '''
		span = ""
		css  = """#box{font-family:'calibri';max-height:1000px;max-width:1000px;border:2px solid black;}
		#box a{text-decoration : none}
		"""
		
		''' Colors for words in wordcloud '''
		colors = ['#607ec5','#002a8b','#86a0dc','#4c6db9']
		colsize = len(colors)
		k = 0
		for index,item in enumerate(a):
			index += 1
			
			if case == "upper":
				tag = str(item[0]).upper()
			else:
				tag = str(item[0])

			if show_freq == "yes":
				span += '<a href=#><span class="word'+str(index)+'" id="tag'+str(index)+'">' + tag + " (" + str(item[1]) + ") " + "</span></a>\n"
			else:
				if len(item[0]) > 1:
					span += '<a href=#><span class="word'+str(index)+'" id="tag'+str(index)+'">' + tag + "</span></a>\n"	
			
			''' Create Randomness in sizes'''
			size = item[1]*item[1]*item[1]%400
			if size < 50:
				size += 250
		 	if size > 50 and size < 100:
				size += 150
			
		 	css += '#tag'+str(index)+'{font-size: '+ str(size) +'%;color: '+colors[int(k%colsize)]+'}\n'
		 	css += '#tag'+str(index)+':hover{color: red}\n'
		 	k += 1

		
		''' Write the HTML and CSS into seperate files ''' 
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

		return render_template('index.html')

	startover()
	return render_template('index.html')

''' 
Function to get top keywords from an article 
'''
def getKeywords(articletext, case, freq):

	''' Ignoring the most common words from English Text '''
	common = open("static/common_words.txt").read().split('\n')
	
	''' Create the dictionary for output response '''
	word_dict = {}
	word_list = articletext.lower().split()
	for word in word_list:
		if word not in common and word.isalnum():
			if word not in word_dict:
				word_dict[word] = 1
			if word in word_dict:
				word_dict[word] += 1
	top_words =  sorted(word_dict.items(),key=lambda(k,v):(v,k),reverse=True)[0:freq]

	'''  Return a list of dictionaies, dictionaies contains word and their frequencies '''	
	top = []
	for w in top_words:
		top.append(w)

	return top

'''
Function to reset everthing and startover
'''
@app.route('/startover')
def startover():
	f = open("templates/wordcloud.html",'w')
	f.write("")
	f.close
	f = open("static/wordcloud.css",'w')
	f.write("")
	f.close
	return redirect(url_for('index'))

'''
Run the Flask Application
'''
if __name__ == '__main__':
	app.run(debug = True)