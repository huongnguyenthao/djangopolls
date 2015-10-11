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

from .models import Question, Visitor, Ad, Click


class IPRecordingView(generic.View):
    pass


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        request = self.request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            v = Visitor.objects.get(ip = ip)
        except Visitor.DoesNotExist:
            v = Visitor(ip = ip, visits = 0)
        v.visits +=1;
        v.save()
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView, IPRecordingView):
    model = Question
    template_name = 'polls/detail.html'


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
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def ad_click(request):
    adID = request.POST['ad_id']
    print (adID)
    clicked_ad = Ad.objects.get(pk=int(request.POST['ad_id']))
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    v = Visitor.objects.get(ip = ip)

    try:
        c = Click.objects.get(visitor=v, ad=clicked_ad)
    except Click.DoesNotExist:
        c = Click(visitor=v, ad=clicked_ad)
    c.clicks += 1
    c.save()
    return HttpResponseRedirect(clicked_ad.get_absolute_url())