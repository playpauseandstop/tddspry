from django.db import models
from django.db.models import permalink


__all__ = ('UserProfile', )


class UserProfile(models.Model):

    user = models.OneToOneField('auth.User', related_name='profile')
    bio = models.TextField()

    def __unicode__(self):
        return u'Profile for "%s" user' % self.user.username

    @permalink
    def get_absolute_url(self):
        return ('user', [self.user.username])
