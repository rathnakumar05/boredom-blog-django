from mongoengine import *
from datetime import datetime

class Post(Document):
    uuid = StringField(max_length=100, default=None)
    user_id = IntField(null=False, default=None)
    title = StringField(max_length=250, null=True, default=None)
    description = StringField(max_length=500, null=True, default=None)
    content = DynamicField(null=True, default=None)
    author = StringField(max_length=150, null=True, default=None)
    status = StringField(max_length=20, choices=[
        ('drafted', 'drafted'),
        ('published', 'published'),
        ('private', 'private')
    ], null=True, default="drafted")
    tumbnail = StringField(max_length=100, default=None)
    framework = StringField(max_length=20, null=True, default=None)
    extra = StringField(max_length=100, null=True, default=None)
    token = StringField(max_length=50, null=True, default=None)
    created_at = DateTimeField(default=datetime.utcnow)
    modified_at = DateTimeField(default=datetime.utcnow)
