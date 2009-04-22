from tddspry.django import HttpTestCase


class TestHTTP(HttpTestCase):

    def test_index(self):
        self.go('/')
        self.code(200)
        self.url('/')

        self.find('Something')
        self.find('Something++', flat=True)
