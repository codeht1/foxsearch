import urllib
import mechanize
from bs4 import BeautifulSoup
import re


from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
# Create your views here.
from .forms import SearchForm
from .models import Searchreq

#from .program import complete

import os
BASE_DIR = os.path.dirname(__file__)

##
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
def error404(request):
 	context={}
 	template = "404.html"
 	return render(request,template,context,status=404)

def error400(request):
 	context={}
 	template = "400.html"
 	return render(request,template,context,status=400)

def error403(request):
 	context={}
 	template = "403.html"
 	return render(request,template,context,status=403)

def error500(request):
 	context={}
 	template = "500.html"
 	return render(request,template,context,status=500)

def get_ip(request):
	try:
		x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip=x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = "" 
	return ip


def home(request):
	form = SearchForm(request.POST or None)
 	context={"form":form}
 	template = "home.html"
 	return render(request,template,context)

def result(request):
	#print request
	#form1 = ResultForm()
	#resultToQuery=complete()
	form = SearchForm(request.POST or None)
	result="Oops, looks like you forgot to fill all inputs. Please Search again"
	email = "abc@abc.com"
	if form.is_valid():
		email = form.cleaned_data['email']
		query = form.cleaned_data['query']
		ip = get_ip(request)
		new_searchreq,created = Searchreq.objects.get_or_create(email=email,ip_address=ip,query=query)
		#print new_searchreq,created
		result = mhello(str(form.cleaned_data['query']))
	response = result
 	context={"response":response}
 	template = "result.html"
 	return render(request,template,context)

def about(request):
 	context={}
 	template = "about.html"
 	return render(request,template,context)

def contact(request):
 	context={}
 	template = "contact.html"
 	return render(request,template,context)

def mhello(Query):
	if(Query):
		mtext=searchQuery(Query)
		if(mtext):
			return mtext
		else:
			return "Error","Don't mock me! Enter something relevant"
	else:
		return "Error","Please enter something to search"




def getLinks(link):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent','chrome')]

	term = link.replace(" ","+")
	query= "http://www.google.com/search?num=10&q="+term
	htmltext = br.open(query).read()
	soup= BeautifulSoup(str(htmltext))
	search = soup.findAll('div',attrs={'id':'search'})
	searchtext = str(search[0])
	soup1 = BeautifulSoup( str(searchtext))  
	list_items = soup1.findAll('li',attrs={'class':'g'})

	regrex = "q=http.*?&amp"
	pattern = re.compile(regrex)
	regrex1=".*en.wikipedia.*"
	pattern1=re.compile(regrex1)

	wiki_link_array = []
	source_link_array = []
	if(list_items):
		for li in list_items:
			soup2 = BeautifulSoup(str(li))
			links = soup2.findAll('a');
			if(links):
				source_link = links[0]
				#print source_link
				source_url = re.findall(pattern,str(source_link))
				#print source_url
				wiki_url=re.findall(pattern1,str(source_url))
				#print wiki_url
				if(len(source_url)>0):
					source_link_array.append(str(source_url[0].replace("q=","").replace("&amp","")))
				if len(wiki_url)>0:
					wiki_link_array.append(str(source_url[0].replace("q=","").replace("&amp","")))
			else: pass
	else:
		return 0

	#print source_link_array
	#print wiki_link_array
	if(wiki_link_array):
		return wiki_link_array[0]
	#elif(source_link_array):
		#return source_link_array[0]
	else: return 0


def translate(home_language,target_language,text):
	text = text.replace(" ","%20")
	get_url = "https://translate.google.com/translate_a/single?client=t&sl="+home_language+"&tl="+target_language+"&hl="+home_language+"&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=sw&ie=UTF-8&oe=UTF-8&prev=btn&rom=1&ssel=3&tsel=4&q="+text
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.addheaders = [('User-agent','Chrome')]
	translate_text = browser.open(get_url).read().decode('UTF-8')
	translate_text = translate_text.split("]]")
	return translate_text[0].replace("[[[","").replace('"','').split(",")[0]

def post_request(home_language,target_language,text):
	post_url="https://translate.google.com/translate_a/t"
	parameters = {
			'client':'t',
			'text':text,
			'sl':home_language,
			'tl':target_language,
			'hl':home_language,
			'ie':'UTF-8',
			'oe':'UTF-8',
			'prev':'btn',
			'ssel':'0',
			'tsel':'0'
		}
	try:
		data = urllib.urlencode(parameters)
	except:
		#print "error encoding parameters"
		pass
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.addheaders = [('User-agent','Chrome')]
	response = browser.open(post_url,data).read().decode('UTF-8')
	#print response
	translate_array = response.split(',,"en",,')
	translate_array1=translate_array[0].replace("[[[","").replace('["',"$$$").replace('"]',"$$$").split("$$$,$$$")
	trans_string = ""
	translit_string=""
	for block in translate_array1:
		trans_string += block.split('","')[0]
		translit_string+=block.split('","')[2]
	result= trans_string[1:]+"\n"+translit_string
	return result

def spinner(text,through_language):
	return translate(through_language,"en",translate("en",through_language,text).encode('UTF-8'))


def scrapWikiInfo(link):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent','chrome')]
	query= link
	htmltext = br.open(query).read()
	if(htmltext):
		soup= BeautifulSoup(str(htmltext))
		searchtext = soup.findAll('div',attrs={'id':'mw-content-text'})
		soup1 = BeautifulSoup( str(searchtext)) 
		paragraphs = soup1.findAll('p')
		soup2 = BeautifulSoup( str(paragraphs[0])) 
		text = soup2.get_text()
		regrex3=".*may refer to:.*"
		pattern3=re.compile(regrex3)
		checkOtherOptions=re.findall(pattern3,text)
		if(checkOtherOptions):
			print checkOtherOptions
			titles=""
			singleOptionLinks=""
			regrex4=".*[/]wiki[/].*"
			pattern4=re.compile(regrex4)
			count=1
			abbreviationOptions = soup1.findAll('ul')
			for option in abbreviationOptions:
				soup3 = BeautifulSoup(str(option))
				singleOptionInfo = soup3.findAll('li');
				soup4 = BeautifulSoup(str(singleOptionInfo[0]))
				linkForThis=str(soup4.findAll('a'))
				temp = linkForThis.split("href=")
				temp1 = temp[1].split()
				#print temp
				linkForOne=temp1[0].replace('"','')
				validLink=re.findall(pattern4,linkForOne)
				if(validLink):
					singleOptionLinks =singleOptionLinks+linkForOne+"$$"
					titles=titles+soup4.get_text()+"$$"
					#print str(count)+" "+soup4.get_text()
					count=count+1
				
			#choice=input("Enter corresponding no for Abbreviation to search\n")
			partsOfSingleLinks=singleOptionLinks.split("$$")
			linkForParticularAbbr="http://en.wikipedia.org"+partsOfSingleLinks[0]
			#print linkForParticularAbbr
			text = wikiAbbrInfo(linkForParticularAbbr)
			return text
		else:
			return text
	else:
		return 0

def searchThroughDatabase(Abbreviation):
	path=os.path.join(BASE_DIR,"Abbreviations.txt")
	searchFile=open(path,"r")
	expandedForm=""
	for line in searchFile:
		searchAbbreviation=" "+Abbreviation+" "
		if searchAbbreviation in line:
			expandedForm=expandedForm+line+"0"
	searchFile.close()
	if(expandedForm):
		firstExpanded=expandedForm.split("0")
		partsOfAbbr=firstExpanded[0].split("-")
		justFullForm=partsOfAbbr[1];
		return justFullForm
	else:
		return 0

def checkForHindi(word):
	path=os.path.join(BASE_DIR,"DictionaryofHindi.txt")
	searchFile=open(path,"r")
	flag=0
	for line in searchFile:
		searchWord=" "+word+" "
		if searchWord in line:
			flag=1
	searchFile.close()

	if(flag):
		#print "hindi found"
		return 1
	else:
		return 0

def checkWikiOfAbbr(Query):
	singleAbbr=Query.upper().split(" ")
	abbrInfo =""
	flag1=0
	for block in singleAbbr:
		if(block):
			flag1=checkForHindi(block)
			if(flag1 != 1):
				expandedForm=searchThroughDatabase(block)
				#print expandedForm
				if(expandedForm):
					#linkOfAbbr=expandedForm.strip().replace(" ","_")
					#print linkOfAbbr
					completeURL="http://en.wikipedia.org/wiki/"+block
					#print completeURL
					abbrInfo = abbrInfo+scrapWikiInfo(completeURL)
					#print abbrInfo
	if(abbrInfo):
		return abbrInfo
	else:
		return 0

def scrapGoogleInfo(term):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent','chrome')]
	term = term.replace(" ","+")
	query= "http://www.google.com/search?num=5&q="+term
	htmltext = br.open(query).read()
	soup= BeautifulSoup(str(htmltext))
	search = soup.findAll('div',attrs={'id':'search'})
	searchtext = str(search[0])
	soup1 = BeautifulSoup( str(searchtext))  
	list_items = soup1.findAll('li',attrs={'class':'g'})
	info="";
	
	if(list_items):
		for li in list_items:
			soup2 = BeautifulSoup(str(li))
			temp_info = soup2.findAll('span',attrs={'class':'st'});
			soup3 = BeautifulSoup(str(temp_info)) 
			temp_text = soup3.get_text()
			info+=temp_text+"\n"
		return info
	else:
		return 0


def remove_non_ascii(text):
    return ''.join(i for i in text if(ord(i)<128 and ord(i)>31))

def replaceCorrectWord(text):
	text_low=text.lower()
	modified_text=text_low.replace("a","").replace("e","").replace("i","").replace("o","").replace("u","")
	regrex2 = ".*[+,-,*,/,%]*.*"
	pattern2 = re.compile(regrex2)
	flag=0
	found=re.findall(pattern2,str(modified_text))
	#print found
	if(found[1]):
		flag=1
		modified_text1=modified_text.replace("+"," add ").replace("-"," subtract ").replace("*"," multiply ").replace("/"," divide ").replace("%"," mod ")

	if(modified_text):
		if(flag==1):ret_text=modified_text1
		elif(modified_text=="ky"):ret_text="kya"
		elif(modified_text=="kn"):ret_text="kaun"
		elif(modified_text=="ks"):ret_text="kaise"
		elif(modified_text=="kyn"):ret_text="kyon"
		elif(modified_text=="h"):ret_text="hai"
		elif(modified_text=="khn"and text_low!="khan"):ret_text="kahan"
		else:ret_text=text_low
	else: 
		ret_text=text_low
	ret_text=ret_text+" "
	return ret_text


def correctingQuery(text):
	str_arr=text.split()
	correct_Query="";
	for block in str_arr:
		correct_Query+=replaceCorrectWord(block)
	correct_Query=correct_Query+"?"
	return correct_Query

def searchQuery(hitext):
	correct_Query=correctingQuery(hitext)
 	queryInEng = spinner(correct_Query,"hi")
 	#print queryInEng
 	get_link = getLinks(queryInEng)
 	if(not get_link):
 		wiki_Abbr_information=checkWikiOfAbbr(correct_Query)
 	error="Link Not found,Try searching something else!"
 	if(get_link):
	 	#print get_link
	 	wiki_information=scrapWikiInfo(get_link)
	 	#print wiki_information
	 	wiki_inform=remove_non_ascii(wiki_information)
	 	#print wiki_inform
	 	return post_request("en","hi",wiki_inform)
	elif(wiki_Abbr_information):
		wiki_Abbr_inform=remove_non_ascii(wiki_Abbr_information)
		#print wiki_Abbr_inform
	 	return post_request("en","hi",wiki_Abbr_inform)
	else: 
		google_information=scrapGoogleInfo(queryInEng)
		#print google_information
		if(google_information):
			#print google_information
			google_inform=remove_non_ascii(google_information)
			return "Wiki Link Not found and No Abbreviation detected. So we are giving you google info!"+"\n"+post_request("en","hi",google_inform)
		else:
			return 0
 