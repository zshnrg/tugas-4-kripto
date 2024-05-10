from flet import *

class RoleContainer(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.width = 600
        self.bgcolor = colors.BACKGROUND
        self.border_radius = 25
        self.border = border.all(1, colors.OUTLINE)
        self.padding = padding.symmetric(vertical=80, horizontal=100)
        
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.email = self.page.client_storage.get("user.email")

        self.student_card = Card(
            content=Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Mahasiswa", size=16, weight=FontWeight.BOLD),
                                Text("Kamu dapat membuka transkrip akademik dan memvalidasi isinya", size=14, color=colors.ON_SURFACE_VARIANT, width=300),
                            ],
                            spacing=-4
                        ),
                        IconButton(
                            icon=icons.NAVIGATE_NEXT,
                            on_click=lambda e: self.page.go("/auth/role/mahasiswa"),
                        )
                    ]
                ),
                padding=padding.all(20),
                on_click=lambda e: self.page.go("/auth/role/mahasiswa")
            ),
            variant=CardVariant.OUTLINED,
        )

        self.lecturer_card = Card(
            content=Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Dosen", size=16, weight=FontWeight.BOLD),
                                Text("Kamu dapat menambahkan nilai pada data mahasiswa dan membuat transkrip akademik (khusus kaprodi)", size=14, color=colors.ON_SURFACE_VARIANT, width=300),
                            ],
                            spacing=-4
                        ),
                        IconButton(
                            icon=icons.NAVIGATE_NEXT,
                            on_click=lambda e: self.page.go("/auth/role/dosen"),
                        )
                    ]
                ),
                padding=padding.all(20),
                on_click=lambda e: self.page.go("/auth/role/dosen")
            ),
            variant=CardVariant.OUTLINED,
        )

        self.content = Column(
            controls=[
                Text("Identitasmu", size=36, weight=FontWeight.BOLD),
                Text("Sebelum menggunakan aplikasi ini, kami perlu mengetahui siapakah dirimu", size=15, color=colors.ON_SURFACE_VARIANT),
                Column(
                    controls=[
                        self.student_card,
                        self.lecturer_card,
                    ],
                    spacing=10
                )
            ],
            spacing=40
        )

class RoleView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/auth/role"
        self.page = page
        self.page.splash = None

        # Check for redirect
        if not page.client_storage.get("user.email"):
            page.go("/auth")
        if page.client_storage.get("user.role"):
            page.go("/")

        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.padding = 15
        self.bgcolor = colors.BACKGROUND

        self.controls = [
            RoleContainer(page)
        ]