import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) <= now


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class Visitor(models.Model):
    ip = models.CharField(max_length=50)
    visits = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ip


class Ad(models.Model):
    ad_text = models.CharField(max_length=500)
    clicks = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)
    website = models.URLField(default='github.com/huongnguyenthao/djangopolls')

    def get_absolute_url(self):
        if not(self.website.startswith('http://')):
            return 'http://' + self.website
        return self.website

    def __unicode__(self):
        return self.ad_text


class AdImage(models.Model):
    image = models.ImageField(upload_to="images/")
    ad = models.ForeignKey(Ad)


class Click(models.Model):
    visitor = models.ForeignKey(Visitor)
    ad = models.ForeignKey(Ad)
    clicks = models.IntegerField(default=0)


class AdImpression(models.Model):
    visitor = models.ForeignKey(Visitor)
    ad = models.ForeignKey(Ad)
    impressions = models.IntegerField(default=0)


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.tag_name


class TagxAd(models.Model):
    ad = models.ForeignKey(Ad)
    tag = models.ForeignKey(Tag)

    class Meta:
        unique_together = ("ad", "tag")


class TagxQuestion(models.Model):
    tag = models.ForeignKey(Tag)
    question = models.ForeignKey(Question)

    class Meta:
        unique_together = ("tag", "question")