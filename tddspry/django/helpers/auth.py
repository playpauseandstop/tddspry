from django.contrib.auth.models import User


__all__ = ('EMAIL', 'PASSWORD', 'USERNAME', 'create_profile', 'create_staff',
           'create_superuser', 'create_user')


EMAIL = 'test_email@domain.com'
PASSWORD = 'test_password'
USERNAME = 'test_username'


def create_profile(obj, user, klass, **kwargs):
    """
    Create profile for given user.
    """
    kwargs.update({'user': user})
    return klass.objects.create(**kwargs)


def create_staff(obj, username=None, password=None, email=None, raw=False):
    """
    Create Django user with staff rights.
    """
    return create_user(obj, username, password, email, staff=True, raw=raw)


def create_superuser(obj, username=None, password=None, email=None, raw=False):
    """
    Create Django user with superuser and staff rights.
    """
    return create_user(obj, username, password, email, staff=True,
                       superuser=True, raw=raw)


def create_user(obj, username=None, password=None, email=None, active=True,
                staff=False, superuser=False, raw=False):
    """
    Create Django user with given names or with default if absent.
    """
    user = User(username=username or USERNAME,
                email=email or EMAIL)

    user.is_active = active
    user.is_staff = staff
    user.is_superuser = superuser

    if raw:
        user.password = password or PASSWORD
    else:
        user.set_password(password or PASSWORD)

    user.save()
    return user
