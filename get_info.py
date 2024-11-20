'''
The get_info module is used to get the ink and paper levels of the printer. It uses the requests module to get the html page of the printer and the re module to search the ink and paper levels.

This module has been developed by Davide Peressoni https://gitlab.com/DPDmancul for the prject https://gitlab.com/cominfo/botstampante and is released under the Apache 2.0 License [Copyright 2017 Davide Peressoni]. 
'''
import sys, requests, re, time

## The get_page function gets the html page of the printer
def get_page():
	res = requests.get('http://<printer-ip>/web/guest/it/websys/webArch/getStatus.cgi',)
	if res.status_code == 200:
		return res.text
	else:
		print('Error in get_info::get_page\n+-Status not 200',flush=True)#sys.exit
		return None
	
## The re_search function searches the html page for the ink and paper levels and returns them
def re_search(expr,str):
	a = re.compile(expr).search(str)
	if a is None:
		return 0
	else:
		a = a.group(1)
		if a == 'end':
			a = 0
		elif a == 'Nend':
			a = 1
		return int(a)
	
## The get_ink_levels function searches the html page for the ink levels and returns them
def get_ink_levels(page):
	fondo_scala = 160
	ratio = 100.0/fondo_scala
	black = re_search('<img[^>]*src=\"\/images\/deviceStTnBarK.gif"[^>]*width="([0-9]*)\"',page) * ratio
	cyano = re_search('<img[^>]*src=\"\/images\/deviceStTnBarC.gif"[^>]*width="([0-9]*)\"',page) * ratio
	magenta = re_search('<img[^>]*src=\"\/images\/deviceStTnBarM.gif"[^>]*width="([0-9]*)\"',page) * ratio
	yellow = re_search('<img[^>]*src=\"\/images\/deviceStTnBarY.gif"[^>]*width="([0-9]*)\"',page) * ratio
	return [black,cyano,magenta,yellow]


## The get_paper_levels function searches the html page for the paper levels and returns them
def get_paper_levels(page):
	vassoi = []
	vassoi.append(re_search('Vassoio 1<\/dt><dd[^>]*><img[^>]*src=\"\/images\/deviceStP(N?end|[0-9]*)_?16.gif\"',page))
	vassoi.append(re_search('Vassoio 2<\/dt><dd[^>]*><img[^>]*src=\"\/images\/deviceStP(N?end|[0-9]*)_?16.gif\"',page))
	vassoi.append(re_search('Vassoio 3<\/dt><dd[^>]*><img[^>]*src=\"\/images\/deviceStP(N?end|[0-9]*)_?16.gif\"',page))
	return vassoi

## The get_info function gets the html page of the printer and the ink and paper levels and returns them
def get_info():
	contatore = 0
	while True:
		page = get_page()
		inkLevels = get_ink_levels(page)
		paperLevels = get_paper_levels(page)
		if (paperLevels[0]*paperLevels[1]*paperLevels[2] != 0) or contatore >5:
			break
		contatore +=1
		time.sleep(1)
	return [inkLevels,paperLevels]