from django.shortcuts import render, get_object_or_404
from .models import Merch

# Create your views here.


def all_merchandise(request):
    """ A view to show merchandise, including sorting and searching """

    merchandise = Merch.objects.all()

    context = {
        'merchandise': merchandise,
    }

    return render(request, 'merchandise/merchandise.html', context)


def merch_details(request, merch_id):
    """ A view to show details of picked merchandise """

    merch = get_object_or_404(Merch, pk=merch_id)

    context = {
        'merch': merch,
    }

    return render(request, 'merchandise/merch_details.html', context)