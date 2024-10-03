# -*- coding: utf-8 -*-
from django.http import JsonResponse

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import status


def handle_400(request, exception=None):
    ctx = {
        "success": False,
        "error_code": 400,
        "error_message": _("Page Not Found"),
        "error_description": _("Sorry, but the page you are looking for has note been found. Try checking the URL "
                               "for error, then hit the refresh button on your browser or try found something else "
                               "in our app.")
    }
    return JsonResponse(ctx, status=status.HTTP_400_BAD_REQUEST)


def handle_404(request, exception=None):
    ctx = {
        "success": False,
        "error_code": 404,
        "error_message": _("Page Not Found"),
        "error_description": _("Sorry, but the page you are looking for has note been found. Try checking the URL "
                               "for error, then hit the refresh button on your browser or try found something else "
                               "in our app.")
    }
    return JsonResponse(ctx, status=status.HTTP_404_NOT_FOUND)


def handle_403(request, exception=None):
    ctx = {
        "success": False,
        "error_code": 403,
        "error_message": _("Forbidden"),
        "error_description": _("Sorry, but the page you are looking for has note been forbidden.")
    }
    return JsonResponse(ctx, status=status.HTTP_403_FORBIDDEN)


def handle_500(request, exception=None):
    error_message = _("Internal Server Error")
    error_description = _("The server encountered something unexpected that didn't allow it to complete "
                          "the request. We apologize.")
    if exception:
        error_description += f" Error details: {str(exception)}"

    ctx = {
        "success": False,
        "error_code": 500,
        "error_message": error_message,
        "error_description": error_description
    }
    return JsonResponse(ctx, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
