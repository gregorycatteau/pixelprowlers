from django.http import HttpResponse
from .abuse import allow


class AdminLoginThrottle:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path == "/admin/login/":
            if not allow(request, "admin-login", 10, 900):
                response = HttpResponse("Trop de tentatives de connexion. Réessayez dans quinze minutes.", status=429)
                response["Retry-After"] = "900"
                response["Cache-Control"] = "no-store"
                return response
        return self.get_response(request)
