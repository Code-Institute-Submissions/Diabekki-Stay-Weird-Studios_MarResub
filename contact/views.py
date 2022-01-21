from django.shortcuts import render
from .forms import ContactForm


def contact_form(request):
    """Display the contact form"""
    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact/contact.html', context)
