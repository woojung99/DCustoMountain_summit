from django import forms
from cal.models import Event
import datetime

class EventForm(forms.ModelForm):
    year = forms.ChoiceField(
        choices=[(y, y) for y in range(2000, datetime.date.today().year + 1)],
        label="연도",
    )
    month = forms.ChoiceField(
        choices=[(m, m) for m in range(1, 13)],
        label="월",
    )
    day = forms.ChoiceField(
        choices=[(d, d) for d in range(1, 32)],
        label="일",
    )

    hours = forms.ChoiceField(
        choices=[(h, f"{h}") for h in range(0, 24)],
        label="소요 시간 (시간)",
    )
    minutes = forms.ChoiceField(
        choices=[(m, f"{m}") for m in range(0, 60, 5)], 
        label="소요 시간 (분)",
    )

    def clean(self):
        cleaned_data = super().clean()
        year = int(cleaned_data.get("year"))
        month = int(cleaned_data.get("month"))
        day = int(cleaned_data.get("day"))
        cleaned_data["hikedate"] = datetime.date(year, month, day)

        hours = int(cleaned_data.get("hours", 0))
        minutes = int(cleaned_data.get("minutes", 0))
        cleaned_data["duration"] = datetime.timedelta(hours=hours, minutes=minutes)

        distance = cleaned_data.get("distance")
        if distance is None or distance == "":
            cleaned_data["distance"] = 0
        return cleaned_data
    
    def save(self, commit=True): 
        instance = super().save(commit=False) 
        cleaned_data = self.cleaned_data 
        instance.hikedate = cleaned_data["hikedate"]
        instance.duration = cleaned_data["duration"]
        if commit: 
            instance.save() 
        return instance
    
    class Meta:
        model = Event
        fields = [
            "mountain", 
            "distance", 
            "memo", 
            "year", 
            "month", 
            "day", 
            "hours", 
            "minutes", 
        ] 
        widgets = {
            "distance": forms.NumberInput(
                attrs={"placeholder": "등산 거리 (km)"}
            ),
            "memo": forms.Textarea(
                attrs={"placeholder": "메모 입력..."}
            ),
        }
