from distutils.util import strtobool

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from testproject.testapp.forms import *


def edit_hidden_fields(request):
    context = RequestContext(request, {
        'POST': request.POST,
    })
    return render_to_response('testapp/edit_hidden_fields.html', context)


def error(request):
    """
    If view does not return ``HttpResponse`` Django raises an error.
    """


def fast_redirect(request):
    next = request.GET.get('next', '/')
    permanent = strtobool(request.GET.get('permanent', 'no'))

    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    return redirect_class(next)


def index(request):
    context = RequestContext(request, {
        'query': request.GET.get('query', u''),
    })
    return render_to_response('testapp/index.html', context)


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


def multiply_forms(request):
    first_form_submitted = 'first_form_field' in request.POST
    second_form_submitted = 'second_form_field' in request.POST

    context = RequestContext(request, {
        'first_form_submitted': first_form_submitted,
        'second_form_submitted': second_form_submitted,
    })
    return render_to_response('testapp/multiply_forms.html', context)


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
