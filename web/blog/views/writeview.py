from django.views import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import uuid

from ..utils.decorators import verified_required
from ..forms.writeform import WriteForms
from ..models.post import Post

class WriteView(View):
    
    @method_decorator(login_required)
    @method_decorator(verified_required)
    def get(self, request, *args, **kwargs):
        form = WriteForms()
        return render(request, "blog/write/index.html", { 'form' : form })
    
    @method_decorator(login_required)
    @method_decorator(verified_required)
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        form = WriteForms(request.POST, request.FILES)
        if form.is_valid():
            try: 
                title = request.POST.get("title")
                description = request.POST.get("description")
                author = request.POST.get("author")
                uuid_token = str(uuid.uuid4())
                file_name = None
                if request.FILES.get("tumbnail"):
                    file = request.FILES.get("tumbnail")
                    ext = str(file.name.split('.')[-1])
                    file_name = uuid_token+"."+ext
                    with open('blog/static/tumbnail/'+file_name, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                post = Post(user_id = user_id, title=title, description=description, author=author, uuid=uuid_token, status='drafted', tumbnail=file_name)
                post.save()
                return redirect('builder', uuid_token)
            except Exception as err:
                print(err)
        return render(request, "blog/write/index.html", { 'form' : form })
