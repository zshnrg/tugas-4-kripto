import re
from flet import *

class AuthContainer(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.width = 500
        self.bgcolor = colors.BACKGROUND
        self.border_radius = 25
        self.border = border.all(1, colors.OUTLINE)
        self.padding = padding.symmetric(vertical=80, horizontal=100)
        
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        
        self.email = TextField(
            label="Email",
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            helper_text="Masukan email Pak Bas untuk menjadi kaprodi",
            autofocus=True,
            on_submit=self.submit
        )

        self.submit_button = FilledButton(
            text="Masuk atau Daftar",
            on_click=self.submit
        )

        self.content = Column(
            controls=[
                Text("Masuk", size=36, weight=FontWeight.BOLD),
                Text("Masuk dengan email Anda untuk mulai mengakses XIS dan gunakan layanan sistem akademik", size=15, color=colors.ON_SURFACE_VARIANT),
                self.email,
                self.submit_button,
            ],
            spacing=40
        )

    def submit(self, e):
        if self.email.value == "":
            return
        
        self.page.splash = ProgressBar()
        self.email.disabled = True
        self.submit_button.disabled = True
        self.page.update()

        # Validate email with regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email.value):
            self.page.splash = None
            self.email.disabled = False
            self.submit_button.disabled = False

            self.page.snack_bar = SnackBar(
                content=Text("Email tidak valid", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            self.page.snack_bar.open = True


            self.page.update()
            return

        self.page.client_storage.set("user.email", self.email.value)

        self.page.go("/auth/otp")
        
class AuthView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/auth"
        self.page = page

        # Check for redirect
        if page.client_storage.get("user.role"):
            page.go("/")
        if page.client_storage.get("user.validated"):
            page.go("/auth/role")
        
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.padding = 15
        self.bgcolor = colors.BACKGROUND
        
        self.controls = [
            AuthContainer(page)
        ]