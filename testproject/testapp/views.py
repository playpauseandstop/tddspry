from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from testproject.testapp.forms import *


def edit_hidden_fields(request):
    context = RequestContext(request, {
        'POST': request.POST,
    })
    return render_to_response('testapp/edit_hidden_fields.html', context)


def index(request):
    return render_to_response('testapp/index.html',
                              RequestContext(request))


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = LoginForm()

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response('testapp/login.html', context)


def logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    context = RequestContext(request, {
        'user_': request.user,
    })
    return render_to_response('testapp/user.html', context)


def redirect(request):
    return render_to_response('testapp/redirect.html',
                              RequestContext(request))


def user(request, username):
    context = RequestContext(request, {
        'user_': get_object_or_404(User, username=username),
    })
    return render_to_response('testapp/user.html', context)


def users(request):
    context = RequestContext(request, {
        'users': User.objects.all(),
    })
    return render_to_response('testapp/users.html', context)
