from django.shortcuts import render
from .models import Merch

# Create your views here.


def all_merchandise(request):
    """ A view to show merchandise, including sorting and searching """

    merchandise = Merch.objects.all()

    context = {
        'merchandise': merchandise,
    }

    return render(request, 'merchandise/merchandise.html', context)