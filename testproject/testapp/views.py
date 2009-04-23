from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext


def edit_hidden_fields(request):
    context = RequestContext(request, {
        'POST': request.POST,
    })
    return render_to_response('testapp/edit_hidden_fields.html', context)


def index(request):
    return render_to_response('testapp/index.html',
                              RequestContext(request))


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
