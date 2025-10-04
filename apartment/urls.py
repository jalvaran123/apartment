# apartment/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views  # <-- import built-in auth views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root login
    path('', views.login_view, name='login'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Include accounts urls
    path('accounts/', include('accounts.urls')),

    # ✅ Logout route (so {% url 'logout' %} works)
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
