from django.http import JsonResponse
from .models import Article
from django.contrib import auth

#
# 登录接口
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '' or password == '':
            return JsonResponse({'status': 0, 'message': 'username or password null1'})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({'status': 1, 'message': 'login success'})
        else:
            return JsonResponse({'status': 0, 'message': 'username or password error'})
    else:
        return JsonResponse({'status': 0, 'message': 'request type error'})


# 添加博客接口
def add_article(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        title = request.POST.get('title', '')
        author = request.POST.get('author', '')
        content = request.POST.get('content', '')

        if id == '' or title == '' or author == '' or content == '':
            return JsonResponse({'status': 0, 'message': 'id or title or author or content null'})

        if len(title) > 10:
            return JsonResponse({'status': 0, 'message': '文章标题过长'})
        if len(author) > 10:
            return JsonResponse({'status': 0, 'message': '作者名称过长'})
        if len(content) > 500:
            return JsonResponse({'status': 0, 'message': '文章内容过长'})

        try:
            result = Article.objects.filter(id=id)
        except ValueError:
            return JsonResponse({'status': 0, 'message': "参数类型错误"})

        if result:
            return JsonResponse({'status': 0, 'message': 'article id already exists'})
        else:
            try:
                Article.objects.create(id=id, title=title, author=author, content=content)
            except BaseException as e:
                return JsonResponse({'status': 0, 'message': e})
            finally:
                data = {
                    "id": id,
                    "title": title,
                    "author": author,
                    "content": content
                }
                return JsonResponse({'status': 1, 'data': data, 'message': 'add article success'})
    else:
        return JsonResponse({'status': 0, 'message': 'request type error'})


# 修改文章接口
def modify_article(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        title = request.POST.get('title', '')
        author = request.POST.get('author', '')
        content = request.POST.get('content', '')

        if id == '' or title == '' or author == '' or content == '':
            return JsonResponse({'status': 0, 'message': 'id or title or author or content null'})

        try:
            result = Article.objects.filter(id=id)
        except ValueError:
            return JsonResponse({'status': 0, 'message': "参数类型错误"})
        if not result:
            return JsonResponse({'status': 0, 'message': 'article not exist'})

        if len(title) > 10:
            return JsonResponse({'status': 0, 'message': '文章标题过长'})
        if len(author) > 10:
            return JsonResponse({'status': 0, 'message': '作者名称过长'})
        if len(content) > 500:
            return JsonResponse({'status': 0, 'message': '文章内容过长'})

        try:
            Article.objects.filter(id=id).update(id=id, title=title, author=author, content=content)
        except BaseException as e:
            return JsonResponse({'status': 0, 'message': e})
        finally:
            data = {
                "id": id,
                "title": title,
                "author": author,
                "content": content
            }
            return JsonResponse({'status': 1, 'data': data, 'message': 'modify article success'})
    else:
        return JsonResponse({'status': 0, 'message': 'request type error'})


# 删除文章接口
def delete_article(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        if id == '':
            return JsonResponse({'status': 0, 'message': 'id null'})
        try:
            result = Article.objects.filter(id=id)
        except ValueError:
            return JsonResponse({'status': 0, 'message': "参数类型错误"})
        if not result:
            return JsonResponse({'status': 0, 'message': 'id not exist'})
        try:
            Article.objects.filter(id=id).delete()
        except BaseException:
            return JsonResponse({'status': 0, 'message': '删除文章失败'})
        finally:
            return JsonResponse({'status': 1, 'message': 'delete article success'})
    else:
        return JsonResponse({'status': 0, 'message': 'request type error'})


# 查询文章接口
def get_article(request):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        if title == '':
            data = []
            articles = Article.objects.all()
            if articles:
                for article in articles:
                    r = {
                        "id": article.id,
                        "title": article.title,
                        "author": article.author,
                        "content": article.content
                    }
                    data.append(r)
                return JsonResponse({'status': 1, 'message': 'success', 'data': data})
        if title != '':
            data = []
            articles = Article.objects.filter(title__contains=title)
            if articles:
                for article in articles:
                    r = {
                        "id": article.id,
                        "title": article.title,
                        "author": article.author,
                        "content": article.content
                    }
                    data.append(r)
                return JsonResponse({'status': 1, 'message': 'success', 'data': data})
            else:
                return JsonResponse({'status': 0, 'message': 'query result is empty'})
    else:
        return JsonResponse({'status': 0, 'message': 'request type error'})
