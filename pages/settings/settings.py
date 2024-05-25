import random
import base64
from flet import *

class SettingsContainer(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.width = 600
        self.bgcolor = colors.BACKGROUND
        self.border_radius = 25
        self.border = border.all(1, colors.OUTLINE)
        self.padding = padding.symmetric(vertical=80, horizontal=50)

        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        # Getting user info
        self.name = page.client_storage.get("user.name")
        self.role = page.client_storage.get("user.role")
        self.cred_id = page.client_storage.get("user.cred_id")
        self.saved_key = page.client_storage.get("user.key")

        self.name = TextField(
            label="Nama",
            value=self.name,
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            read_only=True,
        )

        self.cred_id = TextField(
            label="NIM" if self.role == "mahasiswa" else "NIP",
            value=self.cred_id if self.cred_id else "Tidak ada",
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            read_only=True,
        )

        self.key = TextField(
            value=base64.b64encode(self.saved_key.encode()).decode() if self.saved_key else "Tidak ada",
            label="Key",
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
        )

        self.random_key_button = IconButton(
            icon=icons.REFRESH,
            on_click=self.generate_random_key
        )

        if self.role == "kaprodi":
            self.column = Column(
                controls=[
                    self.name,
                    self.cred_id,
                    Row(
                        controls=[
                            self.key,
                            self.random_key_button
                        ],
                        spacing=10
                    )
                ],
                spacing=10
            )
        elif self.role == "dosen":
            self.column = Column(
                controls=[
                    self.name,
                    self.cred_id,
                    Row(
                        controls=[
                            self.key,
                            self.random_key_button
                        ],
                        spacing=10
                    )
                ],
                spacing=10
            )
        else:
            self.column = Column(
                controls=[
                    self.name,
                    self.cred_id
                ],
                spacing=10
            )

        self.content = Column(
            controls=[
                IconButton(
                    icon=icons.ARROW_BACK,
                    on_click=lambda e: page.go("/")
                ),
                Container(
                    Column(
                        controls=[
                            Text("Settings", size=36, weight=FontWeight.BOLD),
                            self.column,
                            Row(
                                controls=[
                                    FilledButton(
                                        text="Keluar",
                                        on_click=self.logout,
                                        style=ButtonStyle(
                                            bgcolor=colors.ERROR,
                                            color=colors.ON_ERROR
                                        ),
                                        icon=icons.LOGOUT,
                                        icon_color=colors.ON_ERROR
                                    ),
                                    FilledButton(
                                        text="Simpan",
                                        on_click=self.save
                                    ) 
                                ],
                                spacing=10
                            )
                        ],
                        spacing=40
                    ),
                    padding=padding.symmetric(horizontal=50)
                )
            ],
            spacing=40
        )
        

    def generate_random_key(self, e):
        # generate random key based on all characters of ascii
        self.saved_key = "".join([chr(random.randint(0, 128)) for _ in range(32)])

        # show the key with base64 encoding
        self.key.value = base64.b64encode(self.saved_key.encode()).decode()
        self.page.update()

    def logout(self, e):
        self.page.client_storage.remove("user.email")
        self.page.client_storage.remove("user.validated")
        self.page.client_storage.remove("user.role")
        self.page.client_storage.remove("user.name")
        self.page.client_storage.remove("user.cred_id")


        self.page.database.decrypt(self.page.client_storage.get("user.key"))
        self.page.go("/auth")

    def save(self, e):
        self.page.client_storage.set("user.key", self.saved_key)
        self.page.go("/")

class SettingsView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/settings"
        self.page = page
        self.page.splash = None

        # Check for redirect
        if not page.client_storage.get("user.validated") or not page.client_storage.get("user.email"):
            page.go("/auth")
        elif not page.client_storage.get("user.role"):
            page.go("/auth/role")

        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.padding = 15
        self.bgcolor = colors.BACKGROUND

        self.controls = [
            SettingsContainer(page)
        ]
        