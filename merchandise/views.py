from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Merch, Category

# Create your views here.


def all_merchandise(request):
    """ A view to show merchandise, including sorting and searching """

    merchandise = Merch.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                merchandise = merchandise.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            merchandise = merchandise.order_by(sortkey)


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
    
    current_sorting = f'{sort}_{direction}'

    context = {
        'merchandise': merchandise,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'merchandise/merchandise.html', context)


def merch_details(request, merch_id):
    """ A view to show details of picked merchandise """

    merch = get_object_or_404(Merch, pk=merch_id)

    context = {
        'merch': merch,
    }

    return render(request, 'merchandise/merch_details.html', context)