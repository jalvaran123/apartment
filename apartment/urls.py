from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root login
    path('', views.login_view, name='login'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Include accounts urls
    path('accounts/', include('accounts.urls')),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # API
    path('api/', include('api.urls')),

    # ✅ PWA Files (Static folder but rendered as templates)
    path('manifest.json', TemplateView.as_view(
        template_name="accounts/manifest.json",
        content_type="application/json"
    ), name='manifest'),

    path('offline.html', TemplateView.as_view(
        template_name="accounts/offline.html"
    ), name='offline'),

    path('serviceworker.js', TemplateView.as_view(
        template_name="accounts/serviceworker.js",
        content_type="application/javascript"
    ), name='serviceworker'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
