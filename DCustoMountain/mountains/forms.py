from django import forms
from mountains.models import Mountain

class FilterForm(forms.Form):
    location_choices = [
        ('서울특별시', '서울특별시'),
        ('경기도', '경기도'),
        ('세종특별자치시', '세종특별자치시'),
        ('부산광역시', '부산광역시'), 
        ('인천광역시', '인천광역시'), 
        ('대구광역시', '대구광역시'), 
        ('대전광역시', '대전광역시'), 
        ('광주광역시', '광주광역시'), 
        ('울산광역시', '울산광역시'), 
        ('강원도', '강원도'), 
        ('충청북도', '충청북도'), 
        ('충청남도', '충청남도'), 
        ('전라북도', '전라북도'), 
        ('전라남도', '전라남도'), 
        ('경상북도', '경상북도'), 
        ('경상남도', '경상남도'), 
        ('제주도', '제주도'), 
        ('', '상관없음'), 
    ]
    difficulty_choices = [
        (500, '초급'),
        (1000, '중급'),
        (1500, '고급'),
        ('', '상관없음'), 
    ]
    leadtime_choices = [
        ('2시간~2시간30분미만','2시간 ~ 2시간30분'), 
        ('3시간30분~4시간미만','3시간30분 ~ 4시간미만'), 
        ('4시간~4시간30분미만','4시간 ~ 4시간30분미만'), 
        ('4시간30분~5시간미만','4시간30분 ~ 5시간미만'), 
        ('5시간이상','5시간이상'), 
        ('', '상관없음'), 
    ]
    location = forms.ChoiceField(
        choices=location_choices, 
        widget=forms.Select, 
        required=False
    )
    difficulty = forms.ChoiceField(
        choices=difficulty_choices, 
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}), 
        required=False
    )
    leadtime = forms.ChoiceField(
        choices=leadtime_choices, 
        widget=forms.RadioSelect, 
        required=False
    )