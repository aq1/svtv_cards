import os
import json

from django.shortcuts import render

with open(os.path.join(os.path.dirname(__file__), 'attachments.json')) as f:
    a = json.load(f)


def get_attachments(author):
    return a.get(author, [])


def vk(request):
    return render(
        request,
        'test_constructor/vk.html',
        context={
            'attachments': get_attachments(request.GET.get('a')),
        }
    )
