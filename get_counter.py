'''
The get_counter module is used to get the counter of the printer. It uses the requests module to get the html page of the printer and the re module to search the counter.
'''

import requests, re, time

## The get_page function gets the html page of the printer
def get_page2():
    res = requests.get('http://94.91.27.74/web/guest/it/websys/status/getUnificationCounter.cgi',)
    if res.status_code == 200:
        return res.text
    else:
        print('Error in get_counter::get_page\n+-Status not 200',flush=True)#sys.exit
        return None

def get_page():
    with open("Contatore.html", "r", encoding="utf-8") as file:
        return file.read()
    
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

# Funzione per estrarre la sezione "Stampante"
def get_printer_section(page):
    if not page:
        return None
    # Regex per catturare "Stampante" e tutte le tabelle seguenti
    pattern_stampante = (
        r'<div class="standard" style="font-weight:bold;">Stampante</div>.*?'
        r'(<table.*?>.*?</table>\s*<table.*?>.*?</table>)'
    )
    match = re.search(pattern_stampante, page, re.S)
    return match.group(1) if match else None

# Funzione per ottenere il contatore di "Bianco e nero"
def get_bw(page):
    section = get_printer_section(page)
    if not section:
        print("Sezione 'Stampante' non trovata.")
        return 0
    # Regex per "Bianco e nero"
    pattern_bw = r'<td[^>]*>Bianco e nero</td><td[^>]*>:</td><td[^>]*>(\d+)</td>'
    match = re.search(pattern_bw, section)
    return int(match.group(1)) if match else 0

# Funzione per ottenere il contatore di "Quadricromia"
def get_color(page):
    section = get_printer_section(page)
    if not section:
        print("Sezione 'Stampante' non trovata.")
        return 0
    # Regex per "Quadricromia"
    pattern_color = r'<td[^>]*>Quadricromia</td><td[^>]*>:</td><td[^>]*>(\d+)</td>'
    match = re.search(pattern_color, section)
    return int(match.group(1)) if match else 0

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
    [color,bw] = get_counter()
    print('Color:',color)
    print('B/W:',bw)