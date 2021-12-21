from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Merch, Category

# Create your views here.


def all_merchandise(request):
    """ A view to show merchandise, including sorting and searching """

    merchandise = Merch.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            merchandise = merchandise.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)


        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter criteria to search for")
                return redirect(reverse('merchandise'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            merchandise = merchandise.filter(queries)

    context = {
        'merchandise': merchandise,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'merchandise/merchandise.html', context)


def merch_details(request, merch_id):
    """ A view to show details of picked merchandise """

    merch = get_object_or_404(Merch, pk=merch_id)

    context = {
        'merch': merch,
    }

    return render(request, 'merchandise/merch_details.html', context)