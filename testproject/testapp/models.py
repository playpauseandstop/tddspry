from django.db import models


__all__ = ('UserProfile', )


class UserProfile(models.Model):

    user = models.OneToOneField('auth.User', related_name='profile')
    bio = models.TextField()

    def __unicode__(self):
        return u'Profile for "%s" user' % self.user.username
