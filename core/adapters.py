from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from allauth.exceptions import ImmediateHttpResponse
from core.models import Profile

class SchoolSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        domain = email.split('@')[-1].lower() if email else ''

        # 🚫 Domain restriction removed
        # if not domain.endswith("yourdomain.com"):
        #     raise ImmediateHttpResponse(HttpResponse("Unauthorized domain"))

        # ✅ Default role assignment (you can customize this)
        role = 'student'  # Or change based on logic, if needed

        # ✅ Save or update Profile with role
        user = sociallogin.user
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)

        # 🔧 FIX: Replaced 'profile.role' with 'profile.main_role'
        # Because your model only has main_role field
        if profile.main_role != role:
            profile.main_role = role
            profile.save()

        # ✅ Store in session
        request.session['role'] = role

    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        base_username = slugify(user.email.split('@')[0])
        username = base_username
        count = 0

        # ✅ Ensures unique usernames even if emails are similar
        while User.objects.filter(username=username).exists():
            count += 1
            username = f"{base_username}{count}"

        user.username = username
        return user

    def login(self, request, sociallogin):
        return super().login(request, sociallogin)
