from BeautifulSoup import BeautifulSoup
import urllib
import random

'''
function to get top keywords from the whole text
'''
def getKeywords(articletext):
	common = open("common_words.txt").read().split('\n')
	word_dict = {}
	word_list = articletext.lower().split()
	for word in word_list:
		if word not in common and word.isalnum():
			if word not in word_dict:
				word_dict[word] = 1
			if word in word_dict:
				word_dict[word] += 1
	top_words =  sorted(word_dict.items(),key=lambda(k,v):(v,k),reverse=True)[0:50]
	top20 = []
	for w in top_words:
		top20.append(w)
	return top20

url = "http://sethgodin.typepad.com/"
htmltext = urllib.urlopen(url).read()
soup = BeautifulSoup(htmltext)

'''
Collect all text from url
'''
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
	size = item[1]*item[1]*item[1]%600
	if size < 100:
		size += 50
 	css += '#tag'+str(index)+'{font-size: '+ str(size) +'%;color: '+colors[int(k%4)]+'}\n'
 	css += '#tag'+str(index)+':hover{color: red}\n'
 	k += 1

f = open('wordcloud.html', 'w')
message = """<html>
<head>
<title>WordCloud | HTML</title>
<link rel='stylesheet' href='style.css'>
</head>
<body>
<div id='box'>

""" + span +  """
</div>
</body>
</html>"""
f.write(message)
f.close

f = open('style.css', 'w')
f.write(css)
f.close






















