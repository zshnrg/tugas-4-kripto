import datetime
from flet import *

from lib.cipher.aes import AESCipher

import base64
import os

class OpenListView(ListView):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.padding = padding.symmetric(horizontal=50)
        self.spacing = 40

        self.key = self.page.client_storage.get("user.key")

        self.key_text_field = TextField(
            label="Kunci",
            value=base64.b64encode(self.key.encode()).decode(),
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

        self.open_button = FilledButton(
            text="Buka",
            on_click=lambda e: self.save_file.get_directory_path(),
            width=200,
            disabled=True,
        )

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
                                allowed_extensions=["pdf"]
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
            self.open_button,
        ]

    def handleOpen(self, e):
        self.selected_file.visible = True
        self.file_path = e.files[0].path
        self.selected_file.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.open_button.disabled = False
        self.page.update()

    def handleSave(self, e):
        
        self.page.snack_bar = SnackBar(
            content=Text("Membuka file", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True

        self.page.splash = ProgressBar()
        self.page.update()

        file_path = e.path

        if not file_path:
            self.page.snack_bar = SnackBar(
                content=Text("Folder yang dipilih tidak ditemukan", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.splash = None
            self.page.update()
            return
        
        
        # Decrypt the file
        self.page.snack_bar = SnackBar(
            content=Text("Mendekripsi file", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True
        self.page.update()

       

        with open(self.file_path, "rb") as f:
            data = f.read()

        aes = AESCipher(self.key.encode())
        data = aes.decrypt(data)

        data_split = data.split(b"http://www.reportlab.com")
        new_content = b'%PDF-1.4\n%\x93\x8c\x8b\x9e ReportLab Generated PDF document http://www.reportlab.com' + data_split[1] + b"http://www.reportlab.com" + data_split[2]

        # Save the file
        self.page.snack_bar = SnackBar(
            content=Text("Menyimpan file", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True
        self.page.update()
         
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"Transcript_{current_datetime}.pdf"

        with open(os.path.join(file_path, file_name), "wb") as f:
            f.write(new_content)

        self.page.splash = None
        self.page.snack_bar = SnackBar(
            content=Text("File berhasil dibuka", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True
        self.page.update()
        self.page.go("/")


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