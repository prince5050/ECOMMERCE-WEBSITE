from django.shortcuts import render
from django.views import View

from store.models.events import Event_year
from store.models.tenders import Tenders as TendersModels
from django.conf import settings

class Tenders(View):
    def get(self, request):
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        tenders_list = TendersModels.objects.filter(status=1).order_by('id')
        return render(request, 'tenders.html', {'tenders': tenders_list, 'cart_count': cart_count, 'event_year': event_year})



