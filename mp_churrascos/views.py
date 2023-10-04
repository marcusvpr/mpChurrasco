from django.shortcuts import render
from .models import MpTopic, MpEntry
from .forms import MpTopicForm, MpEntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """Página Principal"""
    return render(request, 'mp_churrascos/index.html')

@login_required
def topics(request):
    """Página Topics"""
    topics = MpTopic.objects.order_by('date_added')
    context = { 'topics': topics }
    return render(request, 'mp_churrascos/topics.html', context)

@login_required
def topic(request, topic_id):
    """Página Topic/Entries"""
    topic = MpTopic.objects.get(id = topic_id)
    entries = topic.mpentry_set.order_by('-date_added')
    context = { 'topic': topic, 'entries': entries }
    return render(request, 'mp_churrascos/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona Novo Assunto"""
    if request.method != 'POST':
        form = MpTopicForm()
    else:
        form = MpTopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))

    context = { 'form': form }
    return render(request, 'mp_churrascos/new_topic.html', context)
    
@login_required
def new_entry(request, topic_id):
    """Adiciona Nova Entrada"""
    topic = MpTopic.objects.get(id = topic_id)

    if request.method != 'POST':
        form = MpEntryForm()
    else:
        form = MpEntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args = [topic_id]))

    context = { 'topic': topic, 'form': form }
    return render(request, 'mp_churrascos/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Altera Entrada"""
    entry = MpEntry.objects.get(id = entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = MpEntryForm(instance = entry)
    else:
        form = MpEntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args = [topic.id]))

    context = { 'entry': entry, 'topic': topic, 'form': form }
    return render(request, 'mp_churrascos/edit_entry.html', context)
