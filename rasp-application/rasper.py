# выводит расписание за текущую дату, либо за какую-то другую, если передать в аргументе
from rasp import *
import sys
import datetime as dt

r = readrasp('table.json')


tampl = dt.date(2024,1,29)

d = None
datedesc = ''
if len(sys.argv) <= 1:
	d = dt.date.today()
	datedesc = 'сегодня'
else:
	a = sys.argv[1]
	if a == 'tomorrow':
		d = dt.date.today() + dt.timedelta(days=1)
		datedesc = 'завтра'
	else:
		d = dt.datetime.strptime(sys.argv[1], '%Y-%m-%d').date()

R = (d - tampl) // dt.timedelta(weeks=1)
ndl = ''
if R % 2 == 0: ndl = 'white'
else: ndl = 'green'

rumonth = 'январь февраль март апрель май июнь июль август сентябрь октябрь ноябрь декабрь'.split(' ')

weekdays = {0:'понедельник',1:'вторник',2:"среда",3:"четверг",4:"пятница",5:"суббота",6:"воскресенье"}

Ndl = ''
if ndl == 'green': Ndl = 'зелёная неделя'
elif ndl == 'white': Ndl = 'белая неделя'
wd = weekdays[d.weekday()]



print(f'{datedesc} {d.day} {rumonth[d.month - 1]}, {wd}, {Ndl}')


if wd in r[ndl]: textday(r[ndl][weekdays[d.weekday()]])
else: print('выходной день')