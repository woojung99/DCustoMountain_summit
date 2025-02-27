from datetime import datetime, timedelta, date 
from django.shortcuts import render, redirect 
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from cal.forms import CalendarContentsForm
from cal.models import *
from cal.utils import Calendar
from django.urls import reverse
from urllib.parse import urlencode

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

def calendar_detail(request, calendar_id): 
    calendar = CalendarContents.objects.get(id = calendar_id)
    events = CalendarContents.objects.filter(user = request.user)
    context = {
        "calendar" : calendar, 
        "events" : events, 
    }
    return render(request, "cal/calendar_detail.html", context)

def add_calendar(request): 
    if request.method == "POST": 
        form = CalendarContentsForm(request.POST) 
        if form.is_valid(): 
            calendar = form.save(commit=False) 
            calendar.user = request.user 
            calendar.save() 
            base_url = reverse("cal:calendar") 
            query_params = urlencode({"day" : calendar.hikedate})
            url = f"{base_url}?{query_params}"
            return redirect(url)
    else: 
        form = CalendarContentsForm() 
    context = {"form" : form}
    return render(request, "cal/add_calendar.html", context)

def edit_calendar(request, calendar_id): 
    calendar = CalendarContents.objects.get(id = calendar_id) 
    if request.method == "POST": 
        form = CalendarContentsForm(request.POST, instance=calendar) 
        if form.is_valid(): 
            edited_calendar = form.save() 
            return redirect(reverse("cal:calendar_detail", kwargs={"calendar_id":edited_calendar.id}))
    else: 
        form = CalendarContentsForm(instance=calendar) 
    context = {"form" : form}
    return render(request, "cal/add_calendar.html", context)

def delete_calendar(request, calendar_id): 
    calendar = CalendarContents.objects.get(id=calendar_id) 
    calendar.delete() 
    base_url = reverse("cal:calendar") 
    query_params = urlencode({"day" : calendar.hikedate})
    url = f"{base_url}?{query_params}"
    return redirect(url)
