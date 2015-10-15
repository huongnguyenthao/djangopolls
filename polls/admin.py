from django.contrib import admin

# Register your models here.
from .models import Question, AdImage, Tag, TagxAd, TagxQuestion
from .models import Choice, Visitor, Ad, Click, AdImpression


class TagxQuestionInline(admin.TabularInline):
    model = TagxQuestion


class QuestionAdmin(admin.ModelAdmin):
    inlines = [TagxQuestionInline]
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]


class AdImageInline(admin.TabularInline):
    model = AdImage


class TagxAdInline(admin.TabularInline):
    model = TagxAd


class AdAdmin(admin.ModelAdmin):
    inlines = [AdImageInline, TagxAdInline]


admin.site.register(Ad, AdAdmin)

class VisitorAdmin(admin.ModelAdmin):
    fields = ['ip', 'visits']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Visitor, VisitorAdmin)

admin.site.register(AdImpression)
admin.site.register(Click)

admin.site.register(Tag)