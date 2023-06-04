from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from ..models.post import Post
from ..forms.writeform import WriteForms

class PublishedView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        posts = Post.objects.filter(user_id=user_id, status='published').order_by('-created_at')
        return render(request, 'blog/profile/index.html', { 'posts' : posts })
    
class DraftedView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        posts = Post.objects.filter(user_id=user_id, status='drafted').order_by('-created_at')
        return render(request, 'blog/profile/index.html', { 'posts' : posts })
    
class EditPostView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        uuid_token = kwargs.get('uuid_token')
        post = Post.objects.filter(uuid=uuid_token).first()
        form = WriteForms(instance=post)
        return render(request, "blog/write/index.html", { 'form' : form })
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        uuid_token = kwargs.get('uuid_token')
        post = Post.objects(uuid=uuid_token).first()
        form = WriteForms(request.POST, request.FILES, instance=post)
        if form.is_valid():
            try: 
                post.title = request.POST.get("title")
                post.description = request.POST.get("description")
                post.author = request.POST.get("author")
                if request.FILES.get("tumbnail"):
                    file = request.FILES.get("tumbnail")
                    ext = str(file.name.split('.')[-1])
                    file_name = uuid_token+"."+ext
                    with open('blog/static/tumbnail/'+file_name, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    post.tumbnail = file_name
                post.save()
            except Exception as err:
                pass
        return redirect('builder', uuid_token)
    
class PublishPostView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        status = {'status' : 'error'}
        uuid_token = kwargs.get("uuid_token")
        post = Post.objects.filter(uuid=uuid_token).update(status="published")
        if post==1:
            status['status'] = 'success'
        return JsonResponse(status)

class DraftPostView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        status = {'status' : 'error'}
        uuid_token = kwargs.get("uuid_token")
        post = Post.objects.filter(uuid=uuid_token).update(status="drafted")
        if post==1:
            status['status'] = 'success'
        return JsonResponse(status)
