from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),

]