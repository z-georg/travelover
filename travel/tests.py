
from django.core.exceptions import ValidationError

# Create your tests here.
from django.test import TestCase

from travel.forms import CreatePhotoForm
from travel.models import Photo


class PhotoFormTest(TestCase):

    def test_new_pictureFormSave_whenValid_country(self):
        data = {
            'city': 'London',
            'title': 'London',
            'description': 'London',
            'county': 'UK',
        }

        with self.assertRaises(ValidationError) as context:
            photo = Photo(data)
            photo.save()
        self.assertIsNotNone(context.exception)


def all_countries_in_the_world(value):
    all_country_in_the_world = ['Bulgaria', 'UK', ]
    if value not in all_country_in_the_world:
        raise ValidationError('Country is not known.')
