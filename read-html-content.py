from lxml import html
import string
import requests
f = open('lieu.txt', 'w')
for c in list(string.ascii_lowercase):
	url="http://www.toutes-les-villes.com/villes-az/"	
	url=url+c+".html"
	#print url
	page = requests.get(url)
	tree = html.fromstring(page.content)
	#This will create a list of prices
	ville = tree.xpath('//a[@class="HomeTxtVert"]/text()')
	v=""
	k=""
	vec=[]
	for j,i in enumerate(ville):
		if (j%2==0):
			k=i
		else:
			v=i	
		if(j%2==0):
			vec.append(v + " (" + k +")")	
	for i in vec:
		f.write(i.encode('utf-8').upper()+'\n')
 


