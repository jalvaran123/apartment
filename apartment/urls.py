from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root landing page
    path('', views.index, name='index'),

    # Login page
    path('login/', views.login_view, name='login'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Include accounts urls
    path('accounts/', include('accounts.urls')),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Override Django's auth login to use custom login view
    path('auth/login/', views.login_view, name='auth_login'),
    
    # Password reset endpoints
    path('auth/request-reset/', views.request_password_reset, name='request_password_reset'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    
    # Include other Django auth URLs (password reset, etc.)
    path('auth/', include('django.contrib.auth.urls')),

    # API
    path('api/', include('api.urls')),

    # ✅ PWA Files (now located in accounts/templates/)
    path('manifest.json', TemplateView.as_view(
        template_name="manifest.json",
        content_type="application/json"
    ), name='manifest'),

    path('offline.html', TemplateView.as_view(
        template_name="offline.html"
    ), name='offline'),

    path('serviceworker.js', TemplateView.as_view(
        template_name="serviceworker.js",
        content_type="application/javascript"
    ), name='serviceworker'),
]

# ✅ Static during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
