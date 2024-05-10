from flet import *
from pages.auth.auth import AuthView
from pages.auth.otp.otp import OTPView
from pages.auth.role.role import RoleView
from pages.auth.role.mahasiswa import MahasiswaView
from pages.auth.role.dosen import DosenView
from pages.menu import MenuView

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
    