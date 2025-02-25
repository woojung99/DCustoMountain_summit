from datetime import datetime, timedelta, date 
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from cal.models import *
from cal.utils import Calendar
from mountains.models import Mountain
from users.models import User
from django.urls import reverse

class CalendarView(generic.ListView):
    model = CalendarContents
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d) 
        context['next_month'] = next_month(d) 
        return context

def get_date(req_day):
    try: 
        if req_day:
            year, month, day = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
    except (ValueError, TypeError): 
        pass 
    return datetime.today().date() 

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    day = 'day=' + str(prev_month.year) + '-' + str(prev_month.month) + '-' + str(prev_month.day) 
    return day

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    day = 'day=' + str(next_month.year) + '-' + str(next_month.month) + '-' + str(next_month.day) 
    return day 

# class CalendarDetailView(generic.DetailView): 
#     model = CalendarContents 
#     template_name = "cal/calendar_detail.html"
#     context_object_name = "hike" 

