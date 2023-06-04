from django.views import View
from django.shortcuts import render
import json
import re

from ..models.post import Post

class BlogView(View):

    def get(self, request, *args, **kwargs):
        uuid_token = kwargs.get("uuid_token")
        post = Post.objects(uuid=uuid_token, status='published').first()
        body = ""
        style = ""
        title = ""
        if post:
            content = post.content
            title = post.title
            if content.get('pagesHtml')[0].get('html') and content.get('pagesHtml')[0].get('css'):
                body = content.get('pagesHtml')[0].get('html')
                body = re.sub(r'<\s*body[^>]*>', '', body)
                body = re.sub(r'<\s*/\s*body\s*>', '', body)
                style = f"<style>{content.get('pagesHtml')[0].get('css')}</style>" 
        return render(request, 'blog/blog/index.html', {'style' : style, 'body' : body, 'title' : title})
    
