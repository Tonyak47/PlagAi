from django.urls import path
from .views import (
    home_view, register_view_web, login_view_web, logout_view, dashboard_view,
    check_view, profile_view,
<<<<<<< HEAD
    register_view, login_view, check_text_view, check_code_view,
=======
    register_view, login_view, check_text_view, check_code_view, download_report,
>>>>>>> e1dc1b7 (Initial commit)
)

urlpatterns = [
    # Website endpoints
    path('', home_view, name='home'),
    path('web/register/', register_view_web, name='register_web'),
    path('web/login/', login_view_web, name='login_web'),
    path('web/logout/', logout_view, name='logout_web'),
    path('web/dashboard/', dashboard_view, name='dashboard_web'),
    path('web/check/', check_view, name='check_web'),
    path('web/profile/', profile_view, name='profile_web'),
<<<<<<< HEAD
=======
    path('download_report/', download_report, name='download_report'),
>>>>>>> e1dc1b7 (Initial commit)

    # API endpoints for mobile/Flutter
    path('api/register/', register_view, name='api_register'),
    path('api/login/', login_view, name='api_login'),
    path('api/check_text/', check_text_view, name='api_check_text'),
    path('api/check_code/', check_code_view, name='api_check_code'),
]