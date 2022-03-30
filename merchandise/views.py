from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Merch, Category, Comment
from .forms import MerchForm, CommentForm

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
                messages.error(
                    request, "You didn't enter criteria to search for")
                return redirect(reverse('merchandise'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
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
    merch_category = merch.category

    # comments = Comment.objects.all().filter(merch__name=merch)
    comments = merch.comment.filter(approved=True)
    comment_form = CommentForm()
    if request.user.is_authenticated:
        username = User.objects.get(username=request.user)
    else:
        username = ''

    if request.method == 'POST' and request.user.is_authenticated:
        name = request.POST.get('name', username)
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        comments = Comment.objects.create(
            merch=merch, name=name, email=email, message=message)

    context = {
        'merch': merch,
        'merch_category': merch_category,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'merchandise/merch_details.html', context)


@login_required
def add_merch(request):
    """ Add merchandise to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry friend, only store owners can do this')
        return redirect(reverse('homepage'))

    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES)
        if form.is_valid():
            merch = form.save()
            messages.success(request, 'Successfully added merchandise!')
            return redirect(reverse('merch_details', args=[merch.id]))
        else:
            messages.error(request, 'Failed to add merch.\
                Please check form is valid.')
    else:
        form = MerchForm()

    template = 'merchandise/add_merch.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_merch(request, merch_id):
    """ Edit merchandise in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry friend, only store owners can do this')
        return redirect(reverse('homepage'))

    merch = get_object_or_404(Merch, pk=merch_id)
    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES, instance=merch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated merchandise!')
            return redirect(reverse('merch_details', args=[merch.id]))
        else:
            messages.error(request, 'Failed to update merch.\
                Check if form is valid.')
    else:
        form = MerchForm(instance=merch)
        messages.info(request, f'You are editing {merch.name}')

    template = 'merchandise/edit_merch.html'
    context = {
        'form': form,
        'merch': merch,
    }

    return render(request, template, context)


@login_required
def delete_merch(request, merch_id):
    """ Delete merchandise from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry friend, only store owners can do this')
        return redirect(reverse('homepage'))

    merch = get_object_or_404(Merch, pk=merch_id)
    merch.delete()
    messages.success(request, 'Merchandise deleted!')
    return redirect(reverse('merchandise'))
