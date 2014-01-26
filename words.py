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
from nltk.corpus import stopwords
import urllib, random, re, string

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
		texts = soup.findAll(text=True)
		visible_texts = filter(visible, texts)
		article = ""
		for text in visible_texts:
			article += text.encode("utf-8")
		article = str(article)
		article = BeautifulSoup(article, convertEntities=BeautifulSoup.HTML_ENTITIES)
		
		#exclude = set(string.punctuation)
		#article = str(article)
		#article = ''.join(ch for ch in article if ch not in exclude)
		
		article = str(article).replace("\n"," ")

		''' Get top keywords '''
		freq = 50
		a = getKeywords(article, case, freq)
		
		random.shuffle(a)
		b = [x[1] for x in a]
		minFreq = min(b)
		maxFreq = max(b)

		''' Create html span tags and corresponding css '''
		span = ""
		css  = """#box{font-family:'calibri';border:2px solid black;}
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
				span += '<a href=#><span class="word'+str(index)+'" id="tag'+str(index)+'">&nbsp;' + tag + " (" + str(item[1]) + ") " + "&nbsp;</span></a>\n"
			else:
				span += '<a href=#><span class="word'+str(index)+'" id="tag'+str(index)+'">&nbsp;' + tag + "&nbsp;</span></a>\n"	
			
			''' Algorithm to scale sizes'''
			freqTag = int(item[1])
			fontMax = 5.5
			fontMin = 1.5
			K = (freqTag - minFreq)/(maxFreq - minFreq)
			frange = fontMax - fontMin
			C = 4
			
			K = float(freqTag - minFreq)/(maxFreq - minFreq)
			size = fontMin + (C*float(K*frange/C))

			css += '#tag'+str(index)+'{font-size: '+ str(size) +'em;color: '+colors[int(k%colsize)]+'}\n'
		 	css += '#tag'+str(index)+':hover{color: red}\n'
		 	k += 1
		

		''' Write the HTML and CSS into seperate files ''' 

		f = open('templates/wordcloud.html', 'w')
		message = """
		<style type="text/css">
		""" + css +"""
		</style>
		<div id='box'>
			""" + span +  """
		</div>
		"""
		f.write(message)
		f.close
		f.flush()
		return render_template('index.html')

	startover()
	return render_template('index.html')

''' 
Function to get top keywords from an article 
'''
def getKeywords(articletext, case, freq):

	''' Ignoring the most common words from English Text '''
	common = open("static/assets/common_words.txt").read().split('\n')
	
	''' Create the dictionary for output response '''
	word_dict = {}
	word_list = articletext.lower().split()
	
	filtered_words = [w for w in word_list if not w in stopwords.words('english')]

	for word in filtered_words:
		if word.isalnum() and not word.isdigit() and not len(word) == 1:
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
	return redirect(url_for('index'))

def visible(element):
		    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		        return False
		    elif re.match('<!--.*-->', str(element)):
		        return False
		    return True

'''
Run the Flask Application
'''
if __name__ == '__main__':
	app.run(debug = True)