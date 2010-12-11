from django.db import models
from django.db.models import permalink


__all__ = ('UserProfile', )


class Contact(models.Model):

    city = models.CharField(max_length=128)
    address = models.TextField(blank=True)

    def __unicode__(self):
        result = self.city

        if self.address:
            result += u', ' + self.address

        return result


class UserProfile(models.Model):

    user = models.OneToOneField('auth.User', related_name='profile')
    contacts = models.ManyToManyField('Contact', blank=True, null=True,
        related_name='profiles')
    bio = models.TextField(blank=True)

    def __unicode__(self):
        return u'Profile for "%s" user' % self.user.username

    @permalink
    def get_absolute_url(self):
        return ('user', [self.user.username])
