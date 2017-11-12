from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from .models import Topic
from .models import Entry
from .forms import TopicForm
from .forms import EntryForm
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
import json


def index(request):
    """学习笔记主页"""
    return render(request, 'learning_logs/index.html')


@login_required
def get_all_topics(request):
    """显示所有主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def get_topic_entries(request, topic_id):
    """显示单个主题的所有列表"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求主题属于当前用户
    if request.user != topic.owner:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def add_topic(request):
    """创建新的主题"""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # Post提交的数据，对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@csrf_exempt
@login_required
def is_empty_topic(request):
    """查询topic下是否有条目"""
    if not request.user.is_authenticated():
        return Http404
    if request.is_ajax():
        # print(request.POST.get('topic_id'))
        topic_id = json.loads(request.POST.get('topic_id'))
        topic = Topic.objects.get(id=topic_id)
        entries = topic.entry_set.all()
        if len(entries) != 0:
            return HttpResponse(json.dumps({'result': 'NoEmpty'}))
        else:
            return HttpResponse(json.dumps({'result': 'Empty'}))


@csrf_exempt
@login_required
def del_topic(request):
    """删除一条主题"""
    if not request.user.is_authenticated:
        return Http404
    if request.is_ajax():
        topic_id = json.loads(request.POST.get('topic_id'))
        Topic.objects.filter(id=topic_id).delete()
        topics = Topic.objects.filter(owner=request.user).all()
        template = get_template('learning_logs/t_topic.html')
        html = template.render({'topics': topics})
        return HttpResponse(json.dumps({'result': 'succeed', 'html': html}))


@login_required
def add_entry(request, topic_id):
    """创建新纪录"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑既定条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确保编辑的条目属于当前登陆的用户
    if request.user != topic.owner:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
@csrf_exempt
def del_entry(request):
    """删除既定条目"""
    if not request.user.is_authenticated():
        return Http404
    if request.is_ajax():
        entry_id = json.loads(request.POST.get('entry_id'))
        topic = Entry.objects.get(id=entry_id).topic
        Entry.objects.filter(id=entry_id).delete()
        entries = topic.entry_set.order_by('-date_added')
        template = get_template('learning_logs/entry.html')
        html = template.render({'get_topic_entries': topic, 'entries': entries})
        return HttpResponse(json.dumps({'result': 'succeed', 'html': html}))
