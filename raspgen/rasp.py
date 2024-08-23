# модуль чтения из excel

import openpyxl
from collections import defaultdict

daymap = {'пн':'понедельник','вт':'вторник','ср':'среда','чт':'четверг','пт':'пятница','сб':'суббота'}

def readrasp(fn):
	try:
		wb = openpyxl.load_workbook(fn)
		s = wb.active
		green = defaultdict(list)
		white = defaultdict(list)
		i = s.iter_rows(2)
		o = next(i)
		wday = ''
		while True:
			if type(o[1]) == openpyxl.cell.cell.MergedCell:
				o = next(i)
				continue
			o2 = s[o[0].row + 1]
			o3 = None
			if type(o2[1]) == openpyxl.cell.cell.MergedCell:
				o3 = s[o[0].row + 2]
				if type(o3[1]) != openpyxl.cell.cell.MergedCell: o3 = None
			if o[0].value != None:
				wday = o[0].value.casefold()
				if wday in daymap: wday = daymap[wday]
			ts = o[1].value
			if ts == None:
				o = next(i)
				continue
			stime = ts.split('-')[0].strip()
			etime = ts.split('-')[1].strip()
			whitesub = o[2].value
			if whitesub != None:
				whitesub = whitesub.split('\n')
				sub = whitesub[0]
				prep = None
				if o3 != None: prep = o3[2].value
				aud = str(o[3].value)
				Type = None
				if o2 != None: Type = o2[3].value
				rec = {'stime':stime,'etime':etime,'предмет':sub,'преподаватель':prep,'аудитория':aud,'тип':Type}
				white[wday].append(rec)
			greensub = o[4].value
			if greensub != None:
				greensub = greensub.split('\n')
				sub = greensub[0]
				prep = None
				if o3 != None: prep = o3[4].value
				aud = str(o[5].value)
				Type = None
				if o2 != None: Type = o2[5].value
				rec = {'stime':stime,'etime':etime,'предмет':sub,'преподаватель':prep,'аудитория':aud,'тип':Type}
				green[wday].append(rec)
			o = next(i)
	except StopIteration: pass
	td = {'white':white,'green':green}
	return td

def textrasp(r):
	print('белая неделя:\n')
	for day in ["понедельник","вторник","среда","четверг","пятница", "суббота"]:
		print(day)
		textday(r['white'][day])
		print('')
	print('\nзелёная неделя\n')
	for day in ["понедельник","вторник","среда","четверг","пятница", "суббота"]:
		print(day)
		textday(r['green'][day])
		print('')

def textday(day):
	for dis in day:
		print(f'{dis["stime"]} {dis["etime"]}')
		print(f'предмет: {dis["предмет"]}')
		print(f'тип: {dis["тип"]}')
		if dis['преподаватель'] != None: print(f'преподаватель: {dis["преподаватель"]}')
		if dis["аудитория"] != None: print(f'аудитория: {dis["аудитория"]}')
		print('')


