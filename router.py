from flet import *
from pages.auth.auth import AuthView
from pages.auth.otp.otp import OTPView
from pages.auth.role.role import RoleView
from pages.auth.role.mahasiswa import MahasiswaView
from pages.auth.role.dosen import DosenView
from pages.menu.menu import MenuView
from pages.settings import SettingsView
from pages.menu.database.database import DatabaseView
from pages.menu.database.add import AddView
from pages.menu.transcript.transcript import TranscriptView
from pages.menu.transcript.create import CreateTranscriptView
from pages.menu.open import OpenView
from pages.menu.validate import ValidateView

def router(page: Page, route: str):
    troute = TemplateRoute(route)
    if troute.match('/'):
        return MenuView(page)
    elif troute.match('/auth'):
        return AuthView(page)
    elif troute.match('/auth/otp'):
        return OTPView(page)
    elif troute.match('/auth/role'):
        return RoleView(page)
    elif troute.match('/auth/role/mahasiswa'):
        return MahasiswaView(page)
    elif troute.match('/auth/role/dosen'):
        return DosenView(page)
    elif troute.match('/settings'):
        return SettingsView(page)
    elif troute.match('/database'):
        return DatabaseView(page)
    elif troute.match('/database/e'):
        return DatabaseView(page)
    elif troute.match('/database/d'):
        return DatabaseView(page)
    elif troute.match('/database/add'):
        return AddView(page)
    elif troute.match('/transcript'):
        return TranscriptView(page)
    elif troute.match('/transcript/create/:nim'):
        return CreateTranscriptView(page, troute.nim)
    elif troute.match('/open'):
        return OpenView(page)
    elif troute.match('/validate'):
        return ValidateView(page)
    else:
        return MenuView(page)