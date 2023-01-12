from django.contrib import admin 
from .models import Match
from datetime import date

# Register your models here.

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("datetime_to_start", "started", "finalized", "automatic", 
                    "unitary_value_card", "number_cards_allowed", "value_award_all")
    
    exclude = ['date_to_start', "started", "finalized", "results"]

    def save_model(self, request, obj, form, change) -> None:
        obj.date_to_start = obj.datetime_to_start.date()
        return super().save_model(request, obj, form, change)
