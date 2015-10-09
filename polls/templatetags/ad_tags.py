from django import template
from ..models import Ad, AdImage
from random import randint

register = template.Library()


@register.inclusion_tag('polls/ad.html', takes_context=True)
def specific_ad(context):
    count = Ad.objects.count()
    rand = randint(1, count)
    ad = Ad.objects.get(pk=rand)
    adimage = AdImage.objects.get(ad=ad)
    ad.impressions += 1
    ad.save()
    return {
        'image_source': adimage.image.url
    }