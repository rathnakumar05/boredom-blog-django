from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..utils.decorators import verified_required

from ..models.post import Post

class HomeView(View):
    
    # @method_decorator(login_required)
    # @method_decorator(verified_required)
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status='published').order_by('-created_at')
        return render(request, 'blog/home/index.html', {'posts' : posts})
