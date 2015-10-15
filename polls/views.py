from django.http import Http404, HttpRequest

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Choice
from django.views import generic
from django.db import models

from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.

from .models import Question, Visitor, Ad, Click, TagxQuestion, Tag, TagxAd
from django.template import RequestContext, loader
from django.db.models.loading import get_model
from django.db.models.expressions import RawSQL


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        request = self.request
        ip = get_ip_address(request)
        try:
            v = Visitor.objects.get(ip=ip)
        except Visitor.DoesNotExist:
            v = Visitor(ip=ip, visits=0)
        v.visits += 1
        v.save()
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        question = Question.objects.get(pk=self.kwargs.get('pk', None))
        context['tagx_question_list'] = TagxQuestion.objects.filter(question=question)
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
            'tagx_question_list': TagxQuestion.objects.filter(question=p)
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def tag(request, tag_id):
    try:
        tag = Tag.objects.get(pk=tag_id)
        print(tag.tag_name)
        tagx_questions = TagxQuestion.objects.filter(tag=tag)
        for tagxquestion in tagx_questions:
            print tagxquestion.question.question_text
        latest_tagx_question_list = tagx_questions
        template = loader.get_template('polls/tag.html')
        context = RequestContext(request, {
            'latest_tagx_question_list': latest_tagx_question_list,
        })
        return HttpResponse(template.render(context))
    except Tag.DoesNotExist:
        return HttpResponse('No tag found')


def ad_click(request):
    clicked_ad = Ad.objects.get(pk=int(request.POST['ad_id']))
    ip = get_ip_address(request)
    v = Visitor.objects.get(ip=ip)

    try:
        c = Click.objects.get(visitor=v, ad=clicked_ad)
    except Click.DoesNotExist:
        c = Click(visitor=v, ad=clicked_ad)
    c.clicks += 1
    c.save()
    return HttpResponseRedirect(clicked_ad.get_absolute_url())


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip