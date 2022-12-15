from django.db import models
from django.contrib.auth.models import User
from .algo import *
class Profile(models.Model):
    """
    This class holds information for the community member. Username, password, email and contributions.
    """
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    contributions = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.user.username} Profile'


class Element(models.Model):
    """
    This class holds the individual privacy element with the simplified explanation.

    """
    smallDescription = models.CharField(max_length = 200)
    fullExplanation = models.CharField(max_length = 500, null = True)
    weight = models.FloatField(default = 0.0)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return 'ID: {} || Element: {}'.format(self.pk, self.smallDescription)


class Policy(models.Model):
    """
    This is class is used to store the text of the privacy policy. Category and an admin status are included.
    """

    CATEGORY = (
        ('Social Media', 'Social Media'),
        ('Streaming', 'Streaming'),
        ('News', 'News'),
        ('Shopping', 'Shopping'),
        ('Finance', 'Finance'),
        ('Misc', 'Misc'),
    )
    STATUS = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )
    name = models.CharField(
        'Name of Service', max_length = 100, unique = True, blank = False)
    slug = models.SlugField()
    date = models.DateField('Date of Last Update', null = True)
    fullText = models.TextField('Text', blank = False)
    link = models.URLField(blank = False)

    category = models.CharField(max_length = 20, choices = CATEGORY, blank = False)
    status = models.CharField(max_length = 20, default = 'Pending', choices = STATUS)
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    outOfDate = models.BooleanField(default = False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'
    
class Rating(models.Model):
    policy = models.ForeignKey(Policy, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)

    class Meta:
        models.UniqueConstraint(fields = ['policy', 'author'], name = 'one_rating_per_user')

    

class ElementFlag(models.Model):
    """
    This class is used to store the element, privacy policy, and text information all in one spot.
    """
    element = models.ForeignKey(Element, on_delete = models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete = models.CASCADE)
    associatedText = models.CharField(default = None, max_length = 20)
    fullSentence = models.CharField(null = True, max_length = 500)

    def __str__(self):
        return 'Policy: {} || {}'.format(self.policy.name, self.element.smallDescription)

class Edit(models.Model):
    STATUS = [
        ('Accepted', 'Accepted'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    ]
    status = models.CharField(max_length = 9, choices = STATUS, default = "Pending")
    policy = models.ForeignKey(Policy, on_delete = models.CASCADE )
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    text = models.CharField(max_length = 200),
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return 'Date: {}, Policy: {}, Element{}'.format(self.date, self.policy, self.element.id)

    class Meta:
        ordering = ['policy']
