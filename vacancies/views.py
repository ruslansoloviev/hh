
# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .db_manage import DBManage

import json


@csrf_exempt
def index(request):
    for header, value in request.POST.items():
        print("POST", header, value)
    for header, value in request.GET.items():
        print("GET", header, value)

    return HttpResponse("Start page")


def show_log(request):
    filename = request.GET.get('filename', 'hh.log')
    lines = request.GET.get('lines')
    lines = int(lines) if lines else lines

    with open(filename) as f:
        data = f.readlines()

    return HttpResponse(data[-lines:], content_type='text/plain; charset=utf8')


def show_json(request):
    with open('response.json') as f:
        data = json.load(f)

    return HttpResponse(json.dumps(data, ensure_ascii=False, sort_keys=True),
                        content_type='application/json')


def response(request):
    with open('response.json') as f:
        data = json.load(f)

    dbm = DBManage(data)

    return HttpResponse('New records: {}'.format(dbm.records_created))
