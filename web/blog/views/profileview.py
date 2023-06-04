from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from ..models.post import Post
from ..models import Profile
from ..forms.profileform import ProfileForm

class ProfileView(View):
    
    @method_decorator(login_required)
    def get(self, request,*args, **kwargs):
        user_id = request.user.id
        posts = Post.objects.filter(user_id=user_id, status='published').order_by('-created_at')
        try:
            profile = request.user.profile
        except ObjectDoesNotExist:
            profile = None
        return render(request, 'blog/profile/index.html', { 'posts' : posts, 'profile': profile })
    

class ProfileEdit(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_profile = Profile.objects.get_or_create(user=request.user)[0]
        form = ProfileForm(instance=user_profile)
        return render(request, 'blog/profile/edit.html', {'form' : form})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user_profile = Profile.objects.get_or_create(user=request.user)[0]
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
        else:
            form = ProfileForm(instance=user_profile)
        return render(request, 'blog/profile/edit.html', {'form': form})