from flet import *
from services.db import db

class DosenContainer(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.width = 500
        self.bgcolor = colors.BACKGROUND
        self.border_radius = 25
        self.border = border.all(1, colors.OUTLINE)
        self.padding = padding.symmetric(vertical=80, horizontal=50)
        
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        
        self.name = TextField(
            label="Nama",
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            autofocus=True,
        )
        
        self.nip = TextField(
            label="NIP",
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            on_submit=self.submit
        )

        self.submit_button = FilledButton(
            text="Simpan",
            on_click=self.submit
        )

        self.content = Column(
            controls=[
                IconButton(
                    icon=icons.ARROW_BACK,
                    on_click=lambda e: self.page.go("/auth/role")
                ),
                Container(
                    content=Column(
                        controls=[
                            Text("Dosen", size=36, weight=FontWeight.BOLD),
                            Text("Sebelum menggunakan aplikasi ini, kami perlu mengetahui siapakah dirimu", size=15, color=colors.ON_SURFACE_VARIANT),
                            Column(
                                controls=[
                                    self.name,
                                    self.nip
                                ],
                                spacing=10
                            
                            ),
                            self.submit_button
                        ],
                        spacing=40
                    ),
                    padding=padding.symmetric(horizontal=50),
                )
            ],
            spacing=40
        )

    def submit(self, e):
        if not self.name.value:
            self.name.focus()
            return
        if not self.nip.value:
            self.nip.focus()
            return

        self.page.splash = ProgressBar()

        try:
            db.updateUser(
                email=self.page.client_storage.get("user.email"),
                data={
                    "name": self.name.value,
                    "cred_id": self.nip.value,
                    "role": "dosen"
                }
            )

            self.page.client_storage.set("user.name", self.name.value)
            self.page.client_storage.set("user.cred_id", self.nip.value)
            self.page.client_storage.set("user.role", "dosen")
    
            self.page.go("/")
        except Exception as e:
            self.page.snack_bar = SnackBar(
                content=Text("Terjadi kesalahan", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.splash = None
            self.page.update()

class DosenView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/auth/role/dosen"
        self.page = page
        self.page.splash = None
        
        # Check for redirect
        if not page.client_storage.get("user.validated") or not page.client_storage.get("user.email"):
            page.go("/auth")
        elif page.client_storage.get("user.role"):
            page.go("/")

        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.padding = 15
        self.bgcolor = colors.BACKGROUND

        self.controls = [
            DosenContainer(page)
        ]