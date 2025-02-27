from datetime import datetime, timedelta, date 
from django.shortcuts import render, redirect 
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from cal.forms import EventForm
from cal.models import *
from cal.utils import Calendar 
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required

@login_required 
def calendar_view(request): 
    d = get_date(request.GET.get('day', None))
    user_events = Event.objects.filter(user=request.user, 
                                                    hikedate__year=d.year, 
                                                    hikedate__month=d.month)
    cal = Calendar(d.year, d.month) 
    html_cal = cal.formatmonth(withyear=True, contents=user_events)
    context = {
        "calendar" : mark_safe(html_cal), 
        "prev_month" : prev_month(d), 
        "next_month" : next_month(d), 
    }
    return render(request, "cal/calendar.html", context)

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

def event_detail(request, event_id): 
    event = Event.objects.get(id = event_id)
    events = Event.objects.filter(user = request.user)
    context = {
        "event" : event, 
        "events" : events, 
    }
    return render(request, "cal/event_detail.html", context)

def back_calendar(request, event_id): 
    event = Event.objects.get(id=event_id) 
    base_url = reverse("cal:calendar") 
    query_params = urlencode({"day" : event.hikedate})
    url = f"{base_url}?{query_params}"
    return redirect(url)

def add_event(request): 
    if request.method == "POST": 
        form = EventForm(request.POST) 
        if form.is_valid(): 
            event = form.save(commit=False) 
            event.user = request.user 
            event.save() 
            base_url = reverse("cal:calendar") 
            query_params = urlencode({"day" : event.hikedate})
            url = f"{base_url}?{query_params}"
            return redirect(url)
    else: 
        form = EventForm() 
    context = {"form" : form}
    return render(request, "cal/add_event.html", context)

def edit_event(request, event_id): 
    event = Event.objects.get(id = event_id) 
    if request.method == "POST": 
        form = EventForm(request.POST, instance=event) 
        if form.is_valid(): 
            edited_event = form.save() 
            return redirect(reverse("cal:event_detail", kwargs={"calendar_id":edited_event}))
    else: 
        form = EventForm(instance=event) 
    context = {
        "form" : form, 
        "event" : event, 
    }
    return render(request, "cal/edit_event.html", context)

def delete_event(request, event_id): 
    event = Event.objects.get(id=event_id) 
    event.delete() 
    base_url = reverse("cal:calendar") 
    query_params = urlencode({"day" : event.hikedate})
    url = f"{base_url}?{query_params}"
    return redirect(url)

