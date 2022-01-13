from django.shortcuts import render

def user(request):
    template = 'user_profiles/user.html'
    context = {}

    return render(request,template, context)
