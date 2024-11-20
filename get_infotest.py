''' 
This module is a test module for the get_info module. 
It is used to test the get_info module in offline mode. 
It returns the ink and paper levels of the printer
'''
def get_ink_levels():
	fondo_scala = 100
	ratio = 100.0/fondo_scala
	black = 100 * ratio
	cyano = 20 * ratio
	magenta = 80 * ratio
	yellow = 20 * ratio
	return [black,cyano,magenta,yellow]

def get_paper_levels():
	vassoi = []
	vassoi.append(100)
	vassoi.append(100)
	vassoi.append(75)
	return vassoi

def get_info():
	inkLevels = get_ink_levels()
	paperLevels = get_paper_levels()
	return [inkLevels,paperLevels]