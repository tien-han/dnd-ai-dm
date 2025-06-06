# app/views/__init__.py

"""Make our view modules accessible from app.views."""

from .welcome_view import WelcomeView
from .app_view import AppView

__all__ = ["WelcomeView", "AppView"]
