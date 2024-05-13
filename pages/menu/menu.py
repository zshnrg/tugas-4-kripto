from flet import *

class MenuContainer(Container):
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

        self.role = self.page.client_storage.get("user.role")

        self.database_card = Card(
            content=Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Basis Data", size=16, weight=FontWeight.BOLD),
                                Text("Lihat seluruh nilai mahasiswa dan tambahkan nilai mahasiswa", size=14, color=colors.ON_SURFACE_VARIANT, width=300),
                            ],
                            spacing=-4
                        ),
                        IconButton(
                            icon=icons.NAVIGATE_NEXT,
                            on_click=lambda e: self.page.go("/database"),
                        )
                    ]
                ),
                padding=padding.all(20),
                on_click=lambda e: self.page.go("/database")
            ),
            variant=CardVariant.OUTLINED,
        )

        self.transcript_card = Card(
            content=Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Transkrip Akademik", size=16, weight=FontWeight.BOLD),
                                Text("Buat transkrip akademik mahasiswa", size=14, color=colors.ON_SURFACE_VARIANT, width=300),
                            ],
                            spacing=-4
                        ),
                        IconButton(
                            icon=icons.NAVIGATE_NEXT,
                            on_click=lambda e: self.page.go("/transcript"),
                        )
                    ]
                ),
                padding=padding.all(20),
                on_click=lambda e: self.page.go("/transcript")
            ),
            variant=CardVariant.OUTLINED,
        )

        self.open_transcript_card = Card(
            content=Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Buka Transkrip Akademik", size=16, weight=FontWeight.BOLD),
                                Text("Buka file transkrip akademik yang terkunci", size=14, color=colors.ON_SURFACE_VARIANT, width=300),
                            ],
                            spacing=-4
                        ),
                        IconButton(
                            icon=icons.NAVIGATE_NEXT,
                            on_click=lambda e: self.page.go("/open"),
                        )
                    ]
                ),
                padding=padding.all(20),
                on_click=lambda e: self.page.go("/open")
            ),
            variant=CardVariant.OUTLINED,
        )

        self.validate_transcript_card = Card(
            content=Container(
                content=Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Validasi Transkrip Akademik", size=16, weight=FontWeight.BOLD),
                                Text("Validasi transkrip akademik mahasiswa", size=14, color=colors.ON_SURFACE_VARIANT, width=300),
                            ],
                            spacing=-4
                        ),
                        IconButton(
                            icon=icons.NAVIGATE_NEXT,
                            on_click=lambda e: self.page.go("/validate"),
                        )
                    ]
                ),
                padding=padding.all(20),
                on_click=lambda e: self.page.go("/validate")
            ),
            variant=CardVariant.OUTLINED,
        )

        if self.role == "mahasiswa":
            self.column = Column(
                controls=[
                    self.open_transcript_card,
                    self.validate_transcript_card,
                ],
            )
        elif self.role == "dosen":
            self.column = Column(
                controls=[
                    self.database_card,
                    self.open_transcript_card,
                    self.validate_transcript_card,
                ],
            )
        else:
            self.column = Column(
                controls=[
                    self.database_card,
                    self.transcript_card,
                    self.open_transcript_card,
                    self.validate_transcript_card,
                ],
            )

        self.content = Column(
            controls=[
                IconButton(
                    icon=icons.SETTINGS,
                    on_click=lambda e: self.page.go("/settings"),
                ),
                Container(
                    Column(
                        controls=[
                            Text("Menu", size=36, weight=FontWeight.BOLD),
                            Text("Pilih menu yang ingin Anda akses", size=15, color=colors.ON_SURFACE_VARIANT),
                            self.column
                        ],
                        spacing=40
                    ),
                    padding=padding.symmetric(horizontal=50),
                )
            ],
            spacing=40
        )

class MenuView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/"
        self.page = page
        self.page.splash = None

        # Check for redirect
        if not page.client_storage.get("user.email") or not page.client_storage.get("user.validated"):
            page.go("/auth")
        elif not page.client_storage.get("user.role"):
            page.go("/auth/role")

        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.padding = 15
        self.bgcolor = colors.BACKGROUND

        self.controls = [
            MenuContainer(page)
        ]