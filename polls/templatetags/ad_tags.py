from django import template
from ..models import Ad, AdImage, TagxAd
import random

register = template.Library()


@register.inclusion_tag('polls/ad.html', takes_context=True)
def content_targeted_ad(context):
    ads = Ad.objects.all()
    try:
        tagsx_question_list = context['tagx_question_list']
        max_tag = 0
        ads_rank = dict()
        for single_ad in ads:
            tag_match = 0
            for tagx_question in tagsx_question_list:
                tags_of_ad = TagxAd.objects.filter(ad=single_ad)
                for tag_in_ad in tags_of_ad:
                    if tag_in_ad.tag == tagx_question.tag:
                        tag_match += 1
                        ads_rank[single_ad] = tag_match
                        if tag_match > max_tag:
                            max_tag = tag_match
        matched_tags = list()
        for single_ad in ads:
            if ads_rank.has_key(single_ad):
                if ads_rank[single_ad] == max_tag:
                    matched_tags.append(single_ad)
        ad = random.choice(matched_tags)

    except KeyError:
        ad = random.choice(ads)

    adimage = AdImage.objects.get(ad=ad)
    ad.impressions += 1
    ad.save()
    website = ad.website
    if not (website.startswith('http://')):
        website = 'http://' + website
    return {
        'image_source': adimage.image.url,
        'ad_url': website,
        'ad_id': ad.pk
    }