'''
The get_counter module is used to get the counter of the printer. It uses the requests module to get the html page of the printer and the re module to search the counter.
'''

import requests, re, time

## The get_page function gets the html page of the printer
def get_page():
    res = requests.get('http://185.153.12.154:8080/web/guest/it/websys/status/getUnificationCounter.cgi',)
    if res.status_code == 200:
        return res.text
    else:
        print('Error in get_counter::get_page\n+-Status not 200',flush=True)#sys.exit
        return None
    
## The re_search function searches the html page
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

def get_color(page):
    color = re_search(r'<td[^>]*>Bianco e nero</td><td[^>]*>:</td><td[^>]*>(\d+)</td>',page)
    return color

def get_bw(page):
    bw = re_search(r'<td[^>]*>Quadricromia</td><td[^>]*>:</td><td[^>]*>(\d+)</td>',page)
    return bw

## The get_counter function searches the html page for the counter and returns it
def get_counter():
    contatore = 0
    while True:
        page = get_page()
        color = get_color(page)
        bw = get_bw(page)
        if (color*bw != 0) or contatore >5:
            break
        contatore +=1
        time.sleep(1)
    return [color,bw]

if __name__ == '__main__':
    print(get_counter())