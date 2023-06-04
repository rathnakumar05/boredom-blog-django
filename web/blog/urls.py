from django.urls import path

from .views import RegisterView, LoginView, LogoutView, SendVerifyView, VerifyView, ForgotPasswordView, ForgotPasswordChangeView, ChangePassword
from .views import HomeView
from .views import WriteView
from .views import BuilderView, TemplateView, storeTemplate, assetUpload
from .views import ProfileView, ProfileEdit
from .views import PublishedView, DraftedView, EditPostView, PublishPostView, DraftPostView
from .views import BlogView


urlpatterns = [
    #auth
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("send-verify-token", SendVerifyView.as_view(), name="send-verify-token"),
    path("verify-token", VerifyView.as_view(), name="verify-token"),
    path("forgot-password", ForgotPasswordView.as_view(), name="forgot-password"),
    path("forgot-password-change", ForgotPasswordChangeView.as_view(), name="forgot-password-change"),
    path("password-change", ChangePassword.as_view(), name="password-change"),

    #home
    path("", HomeView.as_view(), name="home"),
    path("home", HomeView.as_view(), name="home"),

    #write
    path("write", WriteView.as_view(), name="write"),

    #builder
    path("builder/<str:uuid_token>", BuilderView.as_view(), name="builder"),
    path("load/<str:uuid_token>", TemplateView.as_view(), name="load"),
    path("store/<str:uuid_token>", storeTemplate, name="store"),
    path("asset-upload", assetUpload, name="asset_upload"),

    #profile
    path("profile", ProfileView.as_view(), name='profile'),
    path("profile/published", PublishedView.as_view(), name='profile_published'),
    path("profile/drafted", DraftedView.as_view(), name="profile_drafted"),
    path("profile/edit", ProfileEdit.as_view(), name="profile_edit"),
    
    #post
    path("post/edit/<str:uuid_token>", EditPostView.as_view(), name='post_edit'),
    path("post/publish/<str:uuid_token>", PublishPostView.as_view(), name="post_publish"),
    path("post/draft/<str:uuid_token>", DraftPostView.as_view(), name="post_draft"),

    #blog
    path("<str:uuid_token>", BlogView.as_view(), name="blog")

]