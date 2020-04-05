from django.http import HttpResponse
from django.shortcuts import render
from Model.preprocess_data import Question

que = Question()

def question_answer(request):
    id = request.POST['id']
    print(id)
    if id == "bei":
        question = request.POST['q']
        print(question)

        answer = deal_question(question)

        print(answer)
        return HttpResponse(answer)
    else:
        return render(request, 'index.html')



def deal_question(question):
    return que.question_process(question)