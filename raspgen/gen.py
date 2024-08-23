from rasp import *

r = readrasp('r.xlsx')


days = []
tables = []
lessons = []
types = []
rooms = []
teachers = []
times = []
dayweeks = []

def newid(o):
	if len(o) == 0: return 2
	return max(i['id'] for i in o) + 1

def add(o,v):
	for cv in o:
		ccv = cv.copy()
		del ccv['id']
		if ccv == v: return cv['id']
	vv = v.copy()
	ni = newid(o)
	vv['id'] = ni
	o.append(vv)
	return ni

ddays = {'воскресенье': 1, 'понедельник': 2, 'вторник': 3, 'среда': 4, 'четверг': 5, 'пятница': 6, 'суббота': 7}

for w in ['white','green']:
	if w == 'white': week = 0
	elif w == 'green': week = 1
	for d in ['понедельник','вторник','среда','четверг','пятница','суббота','воскресенье']:
		day = ddays[d]
		for rec in r[w][d]:
			stime = rec['stime']
			etime = rec['etime']
			time = {'start':stime,'end':etime}
			timeid = add(times,time)
			lesson = {'name':rec['предмет']}
			lessonid = add(lessons,lesson)
			teacherid = None
			if 'преподаватель' in rec and rec['преподаватель'] != None:
				teacher = {'name':rec['преподаватель']}
				teacherid = add(teachers,teacher)
			roomid = None
			if 'аудитория' in rec and rec['аудитория'] != None:
				room = {'name':rec['аудитория']}
				roomid = add(rooms,room)
			typeid = None
			if 'тип' in rec and rec['тип'] != None:
				Type = {'name':rec['тип']}
				typeid = add(types,Type)
			tt = {'timeId':timeid,'lessonId':lessonid}
			if teacherid != None: tt['teacherId'] = teacherid
			if roomid != None: tt['roomId'] = roomid
			if typeid != None: tt['typeId'] = typeid
			ttid = add(tables,tt)
			dayweek = {'week':week,'day':day,'timetableId':ttid}
			add(dayweeks,dayweek)

db = {'dayWeekList':dayweeks,'lessonList':lessons,'roomList':rooms,'teacherList':teachers,'timeList':times,'typeList':types,'timetableList':tables,'version':3}

otherkeys = ['attendList', 'dateList', 'examGroupList', 'examList', 'gradeList', 'gradeStatisticList', 'homeworkList', 'imageList', 'noteList', 'weekendList']

for key in otherkeys:
	if not (key in db): db[key] = []

import json
jdb = json.dumps(db,ensure_ascii=False)
import zipfile


with zipfile.ZipFile('out.zip', 'w') as zipf:
	zipf.writestr('timetable_data.json', jdb)




print('success')