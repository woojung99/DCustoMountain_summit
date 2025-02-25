from django import forms
from mountains.models import Mountain

class FilterForm(forms.Form):
    location_choices = [
        ('', '전체'), 
        ('서울', '서울'),
        ('강원', '강원'),
        ('제주', '제주'),
    ]
    height_choices = [
        ('', '전체'), 
        (500, '500m 미만'),
        (1000, '500m 이상 1000m 미만'),
        (1500, '1000m 이상 1500m 미만'),
        (2000, '1500m 이상'),
    ]
    location = forms.ChoiceField(
        choices=location_choices, 
        widget=forms.Select, 
        required=False
    )
    height = forms.ChoiceField(
        choices=height_choices, 
        widget=forms.RadioSelect, 
        required=False
    )