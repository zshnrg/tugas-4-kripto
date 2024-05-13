from flet import *
import base64

class OpenListView(ListView):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.padding = padding.symmetric(horizontal=50)
        self.spacing = 40

        self.key = self.page.client_storage.get("user.key")
        self.key = base64.b64encode(self.key.encode()).decode()

        self.key_text_field = TextField(
            label="Kunci",
            value=self.key,
            border_color=colors.OUTLINE,
            border_radius=15,
            expand=True,
        )

        self.selected_file = Text()
        self.selected_file.visible = False
        self.file_path = None

        self.pick_file = FilePicker(on_result=self.handleOpen)
        self.save_file = FilePicker(on_result=self.handleSave)
        self.page.overlay.append(self.pick_file)
        self.page.overlay.append(self.save_file)

        self.controls = [
            Text("Buka Transkrip", size=36, weight=FontWeight.BOLD),
            Divider(),
            Container(
                content=Column(
                    [
                        FilledTonalButton(
                            text="Pilih File",
                            on_click=lambda e: self.pick_file.pick_files(
                                allow_multiple=False,
                                allowed_extensions=["pdf", "xis"]
                            ),
                        ),
                        self.selected_file,
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                padding=padding.all(80),
                border=border.all(1, colors.OUTLINE_VARIANT),
                border_radius=15,
                alignment=alignment.center,
                on_click=lambda e: self.pick_file.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["pdf", "xis"]
                ),
            ),
            self.key_text_field,
            FilledButton(
                text="Buka",
                on_click=lambda e: self.save_file.get_directory_path(),
                width=200,
            )
        ]

    def handleOpen(self, e):
        self.selected_file.visible = True
        self.file_path = e.files[0].path
        self.selected_file.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.page.update()

    def handleSave(self, e):
        ...

class OpenView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.route = "/open"
        self.page.splash = None

        self.padding = padding.symmetric(vertical=80, horizontal=50)
        self.spacing = 40
        
        if not page.client_storage.get("user.validated") or not page.client_storage.get("user.email"):
            page.go("/auth")
            
        role = page.client_storage.get("user.role")
        if not role:
            page.go("/auth/role")

        self.controls = [
            IconButton(
                icon=icons.ARROW_BACK,
                on_click=lambda e: page.go("/"),
            ),
            Container(
                OpenListView(page),
                expand=True,
            )
        ]