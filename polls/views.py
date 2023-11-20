from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from .forms import QuestionForm, ChoiceForm

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5]
        

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
        
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=f'choice_{i}') for i in range(3)]

        if question_form.is_valid() and all([form.is_valid() for form in choice_forms]):
            question = question_form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            for i, form in enumerate(choice_forms):
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
            return redirect('polls/success_page')

    else:
        question_form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=f'choice_{i}') for i in range(3)]

    return render(request, 'polls/add_question.html', {'question_form': question_form, 'choice_forms': choice_forms})

def success_page(request):
    return render(request, 'polls/success_page.html')

def update_question(request,question_id):
    question  = get_object_or_404(Question, pk = question_id)
    #update question
    if request.method == 'POST':
        question.question_text=request.POST['question_text']
        question.save()
        #update choices
        for choice in question.choice_set.all():
            choice_text = request.POST.get(f'choice_{choice.id}')
            choice.choice_text = choice_text
            choice.save()
    
        return redirect('polls:detail',question_id = question_id)
    return render(request,'polls/update_question.html',{'question':question})

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('polls:index')  # Use 'polls:index' instead of 'polls/index'

    return render(request, 'polls/delete_question.html', {'question': question})

def delete_choice(request,question_id,choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice,pk = choice_id)

    if request.method == 'POST':
        choice.delete()
        return redirect('polls:detail', question_id = question_id)
    return render(request,'polls/delete_choice.html',{'question': question,'choice' : choice})
    