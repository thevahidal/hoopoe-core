import datetime

from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives

from django.conf import settings
from django.utils import timezone

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework_api_key.permissions import HasAPIKey

from users.models import OrganizationAPIKey

from core.serializers import UpupaSerializer

class Timestamp(GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        now = timezone.now()
        beautified = now.strftime("%a, %b %d, %Y, %I:%M %p %Z")
        
        return Response(
            {
                "message": beautified,
                "error": None,
                "payload": {
                    "timestamp": now, 
                    "version": request.version
                }
            }
        )


class Upupa(GenericViewSet):
    serializer_class = UpupaSerializer
    # permission_classes = [HasAPIKey]

    def create(self, request, *args, **kwargs):
        
        key = request.META["HTTP_X_API_KEY"].split()[1]
        api_key = OrganizationAPIKey.objects.get_from_key(key)
        
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = request.data.get("message")
  
        now = timezone.now()
        context = {
            "timestamp": now.strftime("%a, %b %d, %Y, %I:%M %p %Z"),
            "message": message,
            "extra": request.data.get("extra", {}),
        }
      
        plain_version = "upupa_email_template.txt" 
        html_version = "upupa_email_template.html"

        plain_message = render_to_string(
            plain_version,
            {
                **context,
            },
        )
        html_message = render_to_string(
            html_version,
            {
                **context,
            },
        )

        with get_connection(
            username=settings.EMAIL_UPUPA_USER, 
            password=settings.EMAIL_UPUPA_PASSWORD, 
        ) as connection:
            message = EmailMultiAlternatives(
                subject="New Notification: " + message,
                body=plain_message,
                from_email=settings.EMAIL_UPUPA_USER,
                to=settings.EMAIL_RECIPIENTS,
                connection=connection
            )
            message.attach_alternative(html_message, "text/html")  # attach html version
            message.send()

        return Response(
            {
                "message": "Upupa sent successfully.",
                "error": None,
                "payload": {
                    "organization": api_key.organization.name
                },
            }
        )
