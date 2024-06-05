"""
URL configuration for djangoProject5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_up/', log_up),
    path('log_in/', log_in),
    path('post_task/', post_task),
    path('get_user/', get_user),
    path('update_userInfo/',update_userInfo),
    path('get_tasks/',get_tasks),
    path('admin_submit_review/',admin_submit_review),
    path('get_messages/',get_messages),
    path("terminate_task/",terminate_task),
    path("get_subtasks/",get_subtasks),
    path("update_subtask_receiver/",update_subtask_receiver),
    path("submit_subtask_answer/",submit_subtask_answer),
    path("report_subtask/",report_subtask),
    path("process_report/",process_report),
    path("top_up/",top_up),
    path("send-verify-code/",send_verify_code),
    path("reset_password/",reset_password),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

