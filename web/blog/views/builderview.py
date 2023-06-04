from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import uuid

from ..models.post import Post

class BuilderView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        uuid_token = kwargs.get("uuid_token")
        return render(request, 'blog/builder/index.html', {'uuid_token' : uuid_token})
    
class TemplateView(View):
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwrgs):
        uuid_token = kwrgs.get("uuid_token")
        post = Post.objects(uuid=uuid_token).first()
        data = {"data": {"assets": [], "styles": [], "pages": [{"component": ""}]}}
        if post.content is not None:
            data = post.content.get('data')
        return JsonResponse(data)
    
@login_required
@csrf_exempt
def storeTemplate(request, uuid_token):
    status = {'status' : 'error'}
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects(uuid=uuid_token).update(content=data)
        status['status'] = 'success'
    return JsonResponse(status)

@login_required
@csrf_exempt
def assetUpload(request):
    status = {'status' : 'error'}
    if request.method == 'POST':
        files = request.FILES.getlist("images")
        data = []
        static_location = settings.STATIC_URL
        for file in files:
            uuid_token = uuid.uuid4()
            ext = str(file.name.split('.')[-1])
            file_name = str(uuid_token)+"."+ext
            with open('blog/static/post-images/'+file_name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                data.append(static_location+"post-images/"+file_name)
        status["status"] = "success"
        status["data"] = data
    return JsonResponse(status)


    

