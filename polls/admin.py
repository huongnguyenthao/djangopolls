from django.contrib import admin

# Register your models here.
from .models import Question, AdImage
from .models import Choice, Visitor, Ad, Click, AdImpression



class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]


class AdImageInline(admin.TabularInline):
    model = AdImage


class AdAdmin(admin.ModelAdmin):
    inlines = [AdImageInline]


admin.site.register(Ad, AdAdmin)

class VisitorAdmin(admin.ModelAdmin):
    fields = ['ip', 'visits']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Visitor, VisitorAdmin)

admin.site.register(AdImpression)
admin.site.register(Click)