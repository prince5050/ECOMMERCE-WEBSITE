from django.shortcuts import render
from django.views import View
# from store.models.partners import Partners
from store.models.events import Event_year
from store.models.partners import Partners as PartnersModels
from django.conf import settings


class Partners(View):
    def get(self, request):
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        partners_list = PartnersModels.objects.filter(status=1).order_by('id')
        return render(request, 'partners.html', {'partners': partners_list, 'cart_count': cart_count, 'event_year': event_year})