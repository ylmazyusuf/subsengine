import logging
from django.db import connection
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.response import Response
from rest_framework import permissions

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    """
    Simple Health Check Response
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response(data={"status": "ok", "db": "ok"}, status=HTTP_200_OK)
        except Exception as exc:
            logger.exception("Health Check Failed: database connection error")
            return Response(data={"status": "fail", "db": "fail"}, status=HTTP_503_SERVICE_UNAVAILABLE)
