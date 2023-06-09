import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters


logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})


from wxcloudrun.models import User,Event
# 登录
def login(request):
    postBody = request.body
    json_result = json.loads(postBody)
    username = json_result["username"]
    password = json_result["password"]
    print(json_result,username,password)
    username_obj = User.objects.filter(username=username).first()
    if not username_obj:
        return JsonResponse({"code":-1,"errorMsg":"用户不存在"})
    user_obj = User.objects.filter(**{"username":username,"password":password}).first()
    if not user_obj:
        return JsonResponse({"code":-1, "errorMsg": "用户名或密码错误"})
    return JsonResponse({"code":0,"user_info":{"user_type":user_obj.user_type,"username":username}})
#注册
def register(request):
    postBody = request.body
    json_result = json.loads(postBody)
    username = json_result["username"]
    password = json_result["password"]
    user_type = json_result["user_type"]
    username_obj = User.objects.filter(username=username).first()
    if username_obj:
        return JsonResponse({"code": -1, "errorMsg": "用户已存在"})
    User.objects.create(username=username,password=password,user_type=user_type)
    return JsonResponse({"code":"0","user_info":{"user_type":user_type,"username":username}})



# 文件上传
def file_upload(request):
    pass



# Event 管理
def event_list(request):
    status_id = int(request.GET.get("status_id"))
    if status_id == 1:
        event_list = Event.objects.filter(status=1).order_by("-create_time")
    elif status_id == 0:
        event_list = Event.objects.all().order_by("-create_time")
    else:
        event_list = Event.objects.exclude(status=1).order_by("-create_time")
    data_info = []
    for event in event_list:
        content = {}
        content["id"] = event.id
        content["content"] = event.content
        content["comment"] = event.comment
        content["create_time"] = event.create_time
        content["status"] = event.status
        data_info.append(content)
    return JsonResponse({"code": 0, "event_list": data_info})

import datetime
def event_add(request):
    postBody = request.body
    json_result = json.loads(postBody)

    content =json_result["content"]
    comment = json_result["comment"]
    status = json_result["status"]
    create_time = datetime.datetime.now()
    Event.objects.create(content=content, comment=comment, status=status,create_time=create_time)
    return JsonResponse({"code": 0})

def event_delete(request):
    postBody = request.body
    json_result = json.loads(postBody)

    id = json_result["id"]
    user_type = json_result["user_type"]
    Event.objects.filter(id=id).delete()
    return JsonResponse({"code": 0, "user_type": user_type})

def event_edit(request):
    postBody = request.body
    json_result = json.loads(postBody)
    id = json_result["id"]

    comment = json_result["comment"]

    user_type = json_result["user_type"]
    Event.objects.filter(id=id).update(comment=comment,status=user_type)
    return JsonResponse({"code":0,"user_type": user_type})


def event_search():
    pass
