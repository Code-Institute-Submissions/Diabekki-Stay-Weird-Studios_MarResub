from django.shortcuts import render
from .forms import FeedbackForm


def feedback_form(request):
    """Display the feedback form"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feedback/success.html')
    form = FeedbackForm()
    context = {'form': form}
    return render(request, 'feedback/feedback.html', context)