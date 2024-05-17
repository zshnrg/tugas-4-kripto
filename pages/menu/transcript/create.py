from flet import *

from services.db import db
from lib.academic_db import Mahasiswa, AcademicData

from lib.cipher.rsa import RSA
from lib.cipher.aes import AESCipher
from lib.pdf import create_transcript

from io import BytesIO
from datetime import datetime
import os
import datetime

class CreateTranscriptView(View):
    def __init__(self, page: Page, nim: str):
        super().__init__()
        self.page = page
        self.route = "/transcript/create"
        self.page.splash = None

        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.padding = 15
        self.bgcolor = colors.BACKGROUND

        # Check for redirect
        if not page.client_storage.get("user.validated") or not page.client_storage.get("user.email"):
            page.go("/auth")
        role = page.client_storage.get("user.role")
        if not role:
            page.go("/auth/role")
        elif role == "mahasiswa":
            page.go("/")

        if not self.page.database:
            self.page.database = AcademicData(self.page, db)
            self.page.database.load_from_db()

            
        self.page.database.decrypt(self.page.client_storage.get("user.key"))

        self.nim = nim
        self.mahasiswa : Mahasiswa = self.page.database.get_mahasiswa(self.nim)

        self.p_factor = TextField(
            label="P",
            border=border.all(1, colors.OUTLINE),
            border_radius=15,
            width=160,
        )

        self.q_factor = TextField(
            label="Q",
            border=border.all(1, colors.OUTLINE),
            border_radius=15,
            width=160,
        )

        pub_key = self.page.client_storage.get("user.public_key")
        priv_key = self.page.client_storage.get("user.private_key")

        self.public_key = TextField(
            label="Public Key",
            value=pub_key,
            border=border.all(1, colors.OUTLINE),
            border_radius=15,
        )

        self.private_key = TextField(
            label="Private Key",
            value=priv_key,
            password=True,
            can_reveal_password=True,
            border=border.all(1, colors.OUTLINE),
            border_radius=15
        )

        self.save_file = FilePicker(on_result=self.create_file)
        self.page.overlay.append(self.save_file)

        self.controls = [
            Container(
                content=Column(
                    controls=[
                        IconButton(
                            icon=icons.ARROW_BACK,
                            on_click=lambda e: self.page.go("/transcript"),
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Text(
                                        value="Atur Kunci", size=36, weight=FontWeight.BOLD
                                    ),
                                    Column(
                                        [
                                            Row(
                                                controls=[
                                                    self.p_factor,
                                                    self.q_factor,
                                                    IconButton(
                                                        icon=icons.REFRESH,
                                                        on_click=self.generate_key
                                                    )
                                                ]
                                            ),
                                            self.public_key,
                                            self.private_key,
                                        ],
                                        spacing=10
                                    ),
                                    FilledButton(
                                        text="Buat",
                                        on_click=self.save_file.get_directory_path
                                    )
                                ],
                                spacing=40
                            ),
                            padding=padding.symmetric(horizontal=50)
                        )
                    ],
                    spacing=40,
                ),
                width=600,
                bgcolor=colors.BACKGROUND,
                border_radius=25,
                border=border.all(1, colors.OUTLINE),
                padding=padding.symmetric(vertical=80, horizontal=50),
            )
        ]

    def generate_key(self, e):
        rsa = RSA()
        rsa.generate_keys()
        self.public_key.value = rsa.public_key
        self.private_key.value = rsa.private_key
        self.p_factor.value = str(rsa.p)
        self.q_factor.value = str(rsa.q)

        self.page.update()

    def create_file(self, e):
        print("Creating file...")

        self.page.snack_bar = SnackBar(
            content=Text("Membuat transkrip", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True

        self.page.splash = ProgressBar()
        self.page.update()


        if e.path == None:
            return
        self.page.client_storage.set("user.public_key", self.public_key.value)
        self.page.client_storage.set("user.private_key", self.private_key.value)

        pdf, signature = create_transcript(
            public_key=self.private_key.value,
            mahasiswa=self.mahasiswa,
        )

        # Save the file with AES
        print("Getting key...")
        key = self.page.client_storage.get("user.key")

        # transform key into byte buffer
        key = key.encode()

        print("Encrypting...")
        aes = AESCipher(key=key)
        pdf = aes.encrypt(pdf)

        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"[encrypted] {self.mahasiswa.nim}_transcript_{current_datetime}.pdf"
        
        print("Writing to file...")

        with open(os.path.join(e.path, file_name), 'wb') as f:
            f.write(pdf)

        print("File created successfully!")

        if not self.page.database:
            self.page.database = AcademicData(self.page, db)
            self.page.database.load_from_db()

        if db.getTranskrip(self.mahasiswa.nim):
            db.deleteTranskrip(self.mahasiswa.nim)

        db.insertTranskrip(
            nim=self.mahasiswa.nim,
            signature=signature,
            public_key=self.private_key.value
        )

        self.page.database.get_mahasiswa(self.mahasiswa.nim).signature = signature
        self.page.database.get_mahasiswa(self.mahasiswa.nim).public_key = self.private_key.value

        self.page.splash = None
        self.page.snack_bar = SnackBar(
            content=Text("Transkrip berhasil dibuat", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True
        self.page.update()
        self.page.go("/")
