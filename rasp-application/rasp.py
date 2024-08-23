# модуль чтения из файла базы данных приложения

def readrasp(fn):
	import json
	
	def geti(o,id):
		for i in o:
			if i['id'] == id: return i
		raise KeyError('not found')
	
	with open(fn,encoding='utf-8') as f: table = json.load(f)
	from collections import defaultdict
	green = defaultdict(list)
	white = defaultdict(list)
	days = {1:'воскресенье',2:'понедельник',3:'вторник',4:'среда',5:'четверг',6:'пятница',7:'суббота'}
	
	for i in table['dayWeekList']:
		ii = i.copy()
		tt = geti(table['timetableList'],ii['timetableId'])
		tt = tt.copy()
		tt['lesson'] = geti(table['lessonList'],tt['lessonId'])['name']
		del tt['lessonId']
		time = geti(table['timeList'],tt['timeId'])
		tt['start'] = time['start']; tt['end'] = time['end']
		del tt['timeId']
		if 'teacherId' in tt:
			tt['teacher'] = geti(table['teacherList'],tt['teacherId'])['name']
			del tt['teacherId']
		if 'roomId' in tt:
			tt['room'] = geti(table['roomList'],tt['roomId'])['name']
			del tt['roomId']
		if 'typeId' in tt:
			tt['type'] = geti(table['typeList'],tt['typeId'])['name']
			del tt['typeId']
		ii['timetable'] = tt
		del ii['timetableId']
		rec = {'предмет':tt['lesson'],'преподаватель':None,'аудитория':None,'тип':None}
		if 'room' in tt: rec['аудитория'] = tt['room']
		if 'teacher' in tt: rec['преподаватель'] = tt['teacher']
		if 'type' in tt: rec['тип'] = tt['type']
		rec['stime'] = tt['start'].replace('-',':')
		rec['etime'] = tt['end'].replace('-',':')
		o = None
		if ii['week'] == 0: o = white
		elif ii['week'] == 1: o = green
		day = days[ii['day']]
		o[day].append(rec)
	
	for o in [white,green]:
		for d in o.values():
			def sortkey(k):
				t = k['stime']
				t = t.split(':')
				a,b = int(t[0],10),int(t[1],10)
				return (a,b)
			d.sort(key=sortkey)
	
	r = {'white':white,'green':green}
	
	return r


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


