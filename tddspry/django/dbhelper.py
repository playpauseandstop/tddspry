"""
Custom test helpers for regular database operations in Django.

(C) Copyright 2007-2009 KDS Software Group http://www.kds.com.ua/
"""

def check_model_create(klass, **kwargs):
    """
    Create Django instance for given klass with given kwargs and check
    if it is created correctly.

    Example:

        check_model_create(User,
                           username='USERNAME',
                           password='PASSWORD_HASH',
                           email='EMAIL@DOMAIN.COM')

    """
    old_counter = klass.objects.count()
    klass.objects.create(**kwargs)
    new_counter = klass.objects.count()

    assert new_counter - old_counter == 1, \
           'Could not to create only one new %r instance. ' \
           'New counter is %d, when old counter is %d.' % (klass.__name__,
                                                           new_counter,
                                                           old_counter)

def check_model_delete(instance):
    """
    Delete Django instance and check if it is deleted correctly.

    Example:

        user = User.objects.get(username='USERNAME')
        check_model_delete(user)

    """
    pk = instance.pk

    old_counter = klass.objects.count()
    instance.delete()
    new_counter = klass.objects.count()

    klass = type(instance)

    assert old_counter - new_counter == 1, \
           'Could not to delete only one %r instance. ' \
           'New counter is %d, when old counter is %d.' % (klass.__name__,
                                                           new_counter,
                                                           old_counter)

    try:
        klass.objects.get(pk=pk)
    except klass.DoesNotExist:
        pass
    else:
        assert False, 'Could not to delete %r instance with %d pk.' % (
            klass.__name__, pk
        )

def check_model_update(instance, **kwargs):
    """
    Update Django instance with given kwargs and check if it is updated
    correctly.

    Example:

        user = User.objects.get(username='USERNAME')
        check_model_update(user,
                           username='NEW_USERNAME')

    """
    for name, value in kwargs.items():
        setattr(instance, name, value)
    instance.save()

    ret_instance = type(instance).objects.get(pk=instance.pk)
    for name, value in kwargs.items():
        assert getattr(ret_instance, name) == value, \
               'Could not to update %r field.' % name
