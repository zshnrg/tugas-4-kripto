import base64
from typing import Literal, Union
from flet import *

from services.db import db

from lib.academic_db import AcademicData
from lib.pdf import read_transcript

from lib.cipher.rsa import RSA
from lib.cipher.sha import Keccak

class ValidateListView(ListView):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.padding = padding.symmetric(horizontal=50)
        self.spacing = 40

        self.selected_file = Text()
        self.selected_file.visible = False
        self.file_path = None

        self.pick_file = FilePicker(on_result=self.handleOpen)
        self.page.overlay.append(self.pick_file)

        self.validate_button = FilledButton(
            text="Validasi",
            on_click=self.validate_transcript,
            disabled=True,
        )

        self.controls = [
            Text("Validasi Transkrip", size=36, weight=FontWeight.BOLD),
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
                    allowed_extensions=["pdf"]
                ),
            ),
            self.validate_button,
        ]

    def handleOpen(self, e):
        self.selected_file.visible = True
        self.file_path = e.files[0].path
        self.selected_file.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )

        if len(self.controls) > 4:
            # remove the validation result at forth index
            self.controls.pop()
            self.controls.pop()
            self.controls.append(
                self.validate_button
            )

        self.validate_button.disabled = False
        self.page.update()

    def validate_transcript(self, e):
        
        self.page.snack_bar = SnackBar(
            content=Text("Memvalidasi transkrip", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True

        self.page.splash = ProgressBar()
        self.page.update()

        if not self.file_path:
            self.page.snack_bar = SnackBar(
                content=Text("File tidak ditemukan", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.splash = None
            self.page.update()
            return
        
        try:
            result: Union[tuple[str, str, str], tuple[None, None, None], Literal['Edit detected']] = read_transcript(self.file_path)

            if result == "Edit detected":
                self.controls.pop()
                self.controls.append(
                    Container(
                        Column(
                            [
                                Text("Transkrip tidak valid", size=24, weight=FontWeight.BOLD),
                                Text("Transkrip yang Anda unggah tidak valid karena telah diubah", size=16),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        padding=padding.symmetric(vertical=40, horizontal=50),
                        alignment=alignment.center,
                        bgcolor=colors.ERROR_CONTAINER,
                        border=border.all(1, colors.ON_ERROR_CONTAINER),
                        border_radius=15,
                    )
                )
                self.controls.append(
                    self.validate_button
                )
                self.validate_button.disabled = True
                self.page.splash = None
                self.page.snack_bar.open = False
                self.page.update()
                return
            
            nim, data, signature = result

            # if all none then the file is invalid or corrupted
            if not nim or not data or not signature:
                self.page.snack_bar = SnackBar(
                    content=Text("Transkrip tidak valid", color=colors.ON_ERROR_CONTAINER),
                    bgcolor=colors.ERROR_CONTAINER,
                )
                self.page.snack_bar.open = True
                self.page.splash = None
                self.page.update()
                return
            
            if not self.page.database:
                self.page.database = AcademicData(self.page, db)
                self.page.database.load_from_db()

            self.public_key = self.page.database.get_mahasiswa(nim=nim).public_key

            rsa = RSA()
            rsa.set_keys(private_key=self.public_key)

            # decoding signature
            decoded_signature = base64.b64decode(signature).decode()
            decoded_number = [int(num) for num in decoded_signature.split(",")]
            decrypted = rsa.decrypt(decoded_number)

            self.page.snack_bar = SnackBar(
                content=Text("Transkrip terbaca", color=colors.ON_PRIMARY_CONTAINER),
                bgcolor=colors.PRIMARY_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.update()

            self.page.splash = None

            if decrypted == data:
                self.controls.pop()
                self.controls.append(
                    Container(
                        Column(
                            [
                                Text("Transkrip terverifikasi", size=24, weight=FontWeight.BOLD),
                                Text("Transkrip yang Anda unggah telah terverifikasi dan benar", size=16),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        padding=padding.symmetric(vertical=40, horizontal=50),
                        alignment=alignment.center,
                        bgcolor=colors.SECONDARY_CONTAINER,
                        border=border.all(1, colors.ON_SECONDARY_CONTAINER),
                        border_radius=15,
                    )
                )
                self.controls.append(
                    self.validate_button
                )
                self.validate_button.disabled = True
                self.page.update()
            else:
                self.controls.pop()
                self.controls.append(
                    Container(
                        Column(
                            [
                                Text("Transkrip tidak valid", size=24, weight=FontWeight.BOLD),
                                Text("Transkrip yang Anda unggah tidak valid karena telah diubah", size=16),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        padding=padding.symmetric(vertical=40, horizontal=50),
                        alignment=alignment.center,
                        bgcolor=colors.ERROR_CONTAINER,
                        border=border.all(1, colors.ON_ERROR_CONTAINER),
                        border_radius=15,
                    )
                )
                self.controls.append(
                    self.validate_button
                )
                self.validate_button.disabled = True
                self.page.update()

        except Exception as e:
            self.page.snack_bar = SnackBar(
                content=Text("Gagal membaca transkrip", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.splash = None
            self.page.update()




class ValidateView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.route = "/validate"
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
                ValidateListView(page),
                expand=True,
            )
        ]