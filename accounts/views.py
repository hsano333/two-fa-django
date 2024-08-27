from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .backend import FtTmpUserBackend


from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required
from django.db import IntegrityError
from .models import FtUser, FtTmpUser
from datetime import datetime, timezone, timedelta
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from .two_fa import TwoFA
from django.http import (
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseForbidden,
)
from .forms import SignUpForm, SignUpTmpForm
from io import BytesIO
import qrcode
import qrcode.image.svg
import base64


def make_qr(url):
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer)
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")


# Create your views here.
@method_decorator(login_not_required, name="dispatch")
class FtSignupView(CreateView):

    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:signup-two-fa")
    usable_password = None

    def form_invalid(self, form):
        res = super().form_invalid(form)
        res.status_code = 400
        return res

    def form_valid(self, form):
        try:
            form = SignUpTmpForm(self.request.POST)
            rval = super().form_valid(form)
            if rval.status_code >= 300 and rval.status_code < 400:
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password1"]
                backend = FtTmpUserBackend()
                user = backend.authenticate(
                    self.request, email=email, password=password
                )
                if user is None:
                    return HttpResponseServerError(f"Server Error:{e}")

                self.request.session["is_provisional_signup"] = True
                self.request.session["user_id"] = user.id
                tmp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=300)
                self.request.session["exp"] = str(tmp_time.timestamp())  # 5minutes

                url = TwoFA().app(user)
                data = {"qr": make_qr(url)}
                return render(self.request, "registration/signup-two-fa.html", data)

            else:
                rval.satus_code = 400
                return rval
        except Exception as e:
            return HttpResponseServerError(f"Server Error:{e}")


@method_decorator(login_not_required, name="dispatch")
class SignupTwoFAView(TemplateView):
    def copy_user(self, user):
        src_user = FtTmpUser.objects.get(email=user.email)
        if src_user is None:
            raise Exception()
        FtUser.objects.create(
            username=src_user.username,
            password=src_user.password,
            email=src_user.email,
            first_name=src_user.first_name,
            last_name=src_user.last_name,
            app_secret=src_user.app_secret,
        )

    def get(self, request):
        is_provisional_signup = False
        if "is_provisional_signup" in request.session:
            is_provisional_signup = request.session["is_provisional_signup"]
        if is_provisional_signup is False:
            return HttpResponseForbidden()

        id = request.session["user_id"]
        user = FtTmpUser.objects.get(id=id)
        url = TwoFA().app(user)
        data = {"qr": make_qr(url)}
        return render(self.request, "registration/signup-two-fa.html", data)

    def post(self, request):
        is_provisional_signup = False
        if "is_provisional_signup" in request.session:
            is_provisional_signup = request.session["is_provisional_signup"]
        if is_provisional_signup is False:
            return HttpResponseForbidden()

        try:
            id = request.session["user_id"]
            code = request.POST.get("code")
            user = FtTmpUser.objects.get(id=id)
            if user is None:
                return HttpResponseForbidden()
            if TwoFA().verify_app(user, code):
                self.copy_user(user)
            else:
                return HttpResponseBadRequest()

            new_user = FtUser.objects.get(email=user.email)
            if new_user is None:
                return HttpResponseForbidden()
            login(
                request,
                new_user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            # user.delete()

            return render(self.request, "registration/login.html")
        except IntegrityError as e:
            return HttpResponseServerError(f"Server Error:{e}")
        except Exception as e:
            return HttpResponseServerError(f"Server Error:{e}")


@method_decorator(login_not_required, name="dispatch")
class FtLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"

    def form_valid(self, form):
        """
        Login認証が成功時の戻り値をオーバーライド
        """

        try:
            username = self.request.POST.get("username")
            password = self.request.POST.get("password")
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                return HttpResponseBadRequest()

            tmp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=300)
            self.request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
            self.request.session["is_provisional_login"] = True
            self.request.session["user_id"] = user.id

            return render(self.request, "accounts/login-two-fa.html")
        except Exception as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")

    # def form_invalid(self, form):
    # pass


@method_decorator(login_not_required, name="dispatch")
class LoginTwoFAView(TemplateView):

    def get(self, request):
        is_provisional_login = False
        if "is_provisional_login" in request.session:
            is_provisional_login = request.session["is_provisional_login"]
        if is_provisional_login is False:
            return HttpResponseForbidden()
        return render(self.request, "registration/two-fa.html")

    def post(self, request):
        is_provisional_login = False
        if "is_provisional_login" in request.session:
            is_provisional_login = request.session["is_provisional_login"]
        if is_provisional_login is False:
            return HttpResponseForbidden()

        try:
            id = request.session["user_id"]
            code = request.POST.get("code")
            user = FtUser.objects.get(id=id)
            if user is None:
                return HttpResponseForbidden()
            if TwoFA().verify_app(user, code):
                pass
            else:
                return HttpResponseBadRequest()

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return render(self.request, "registration/login.html")
        except IntegrityError as e:
            return HttpResponseServerError(f"Server Error:{e}")
        except Exception as e:
            return HttpResponseServerError(f"Server Error:{e}")
