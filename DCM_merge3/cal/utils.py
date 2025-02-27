from calendar import HTMLCalendar
from cal.models import Event
from django.urls import reverse 
from django.db.models import Sum
from datetime import timedelta

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	def formatday(self, day, contents):
		events_per_day = contents.filter(hikedate__day=day)
		d = ''
		for event in events_per_day:
			d += f"<li><a class='text-success text-decoration-none' href='{reverse('cal:event_detail', args=[event.id])}'>{event.mountain.name}</a></li>"

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	def formatweek(self, theweek, contents):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, contents)
		return f'<tr> {week} </tr>'

	def formatmonth(self, withyear=True, contents=True):
		cal = f'<section class="calendar-section">\n'
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, contents)}\n'
		cal += '</table>\n'
		cal += '</section>'
		return cal
	
	def total_distance(self, contents=True): 
		total_distance = contents.aggregate(Sum('distance'))['distance__sum'] or 0
		return total_distance
	
	def total_duration(self, contents=True): 
		total_duration = contents.aggregate(Sum('duration'))['duration__sum'] or timedelta() 
		return total_duration 