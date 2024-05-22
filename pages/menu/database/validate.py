import base64
from flet import *
from services.db import db
from lib.academic_db import AcademicData, Mahasiswa

from lib.cipher.rsa import RSA
from lib.cipher.sha import Keccak

class RowData(Container):
    def __init__(self, page: Page, mahasiswa: Mahasiswa):
        super().__init__()
        self.page = page
        self.mahasiswa = mahasiswa
        self.isVerified = False

        self.border = border.only(bottom=BorderSide(width=1, color=colors.OUTLINE))
        self.padding = padding.symmetric(vertical=5)

        self.verify_container = Container(
            content=FilledTonalButton(
                text="Verify",
                on_click=self.verify,                
                disabled=self.mahasiswa.signature is None,
            ),
            expand=1,
        )

        self.mata_kuliah = Column()

        for mk in self.mahasiswa.mata_kuliah:
            self.mata_kuliah.controls.append(
                Row(
                    controls=[
                        Container(Text(mk.course.kode, size=16, expand=True, text_align=TextAlign.CENTER), expand=1),
                        Container(Text(mk.course.nama, size=16, expand=True,), expand=2),
                        Container(Text(str(mk.course.sks), size=16, expand=True, text_align=TextAlign.CENTER), expand=1),
                        Container(Text(mk.indeks, size=16, expand=True, text_align=TextAlign.CENTER), expand=1),
                    ],
                )
            )

        self.content = Row(
            controls=[
                Container(
                    content=Text(self.mahasiswa.nim, size=16, text_align=TextAlign.CENTER),
                    expand=1,
                ),
                Container(
                    content=Text(self.mahasiswa.nama, size=16),
                    expand=1,
                ),
                Container(
                    content=self.mata_kuliah,
                    expand=5,
                ),
                Container(
                    content=Text(self.mahasiswa.ipk, size=16, text_align=TextAlign.CENTER),
                    expand=1,
                ),
                Container(
                    content=Text(self.mahasiswa.signature if self.mahasiswa.signature else "-", size=16, text_align=TextAlign.CENTER),
                    expand=3,
                ),
                self.verify_container
            ]
        )

    def verify(self, e):
        self.isVerified = not self.isVerified

        # Verify all mata kuliah
        one_line_data = self.mahasiswa.nim + self.mahasiswa.nama
        for mk in self.mahasiswa.mata_kuliah:
            one_line_data += mk.course.kode + mk.course.nama + str(mk.course.sks) + mk.indeks

        sha = Keccak()
        one_line_data_hash = sha.hash(one_line_data.encode())
        one_line_data_base64 = base64.b64encode(one_line_data_hash).decode()

        signature = self.mahasiswa.signature
        public_key = self.mahasiswa.public_key

        rsa = RSA()
        rsa.set_keys(private_key=public_key)

        # decoding signature
        decoded_signature = base64.b64decode(signature).decode()
        decoded_number = [int(num) for num in decoded_signature.split(",")]
        decrypted = rsa.decrypt(decoded_number)

        if decrypted == one_line_data_base64:
            self.verify_container.content = Container(
                content=Text("Valid", size=16, color=colors.GREEN_800, text_align=TextAlign.CENTER, weight=FontWeight.BOLD),
                bgcolor=colors.GREEN_200,
                padding=padding.all(10),
                border_radius=20,
            )
        else:
            self.verify_container.content = Container(
                content=Text("Invalid", size=16, color=colors.RED_800, text_align=TextAlign.CENTER, weight=FontWeight.BOLD),
                bgcolor=colors.RED_200,
                padding=padding.all(10),
                border_radius=20,
            )

        self.page.update()


class Table(Column):
    def __init__(self, page: Page, academic_data: AcademicData):
        super().__init__()
        self.page = page
        self.spacing = 0

        self.header = Container(
            content=Row(
                controls=[
                    Container(Text("NIM", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=1),
                    Container(Text("Nama", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=1),
                    Container(Text("Kode Mata Kuliah", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=1),
                    Container(Text("Nama Mata Kuliah", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=2),
                    Container(Text("SKS", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=1),
                    Container(Text("Indeks", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=1),
                    Container(Text("IPK", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=1),
                    Container(Text("Signature", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=3),
                    Container(Text("Validation", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER), expand=1),
                ]
            ),
            border=border.only(bottom=BorderSide(width=1, color=colors.OUTLINE)),
            padding=padding.symmetric(vertical=10),
        )

        self.controls = [
            self.header
        ]

        for mahasiswa in academic_data.mahasiswa:
            self.controls.append(
                RowData(page, mahasiswa)
            )
class DatabaseValidateListView(ListView):
    def __init__ (self, page: Page):
        super().__init__()
        self.page = page
        self.padding = padding.symmetric(horizontal=50)
        self.spacing = 40

        if not self.page.database:
            self.page.database = AcademicData(self.page, db)
            self.page.database.load_from_db()

        self.table = Table(page, self.page.database)

        self.controls = [
            Text("Validasi Database", size=36, weight=FontWeight.BOLD),
            Divider(),
            self.table
        ]
        
        
class DatabaseValidateView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/database/validate"
        self.page = page
        self.page.splash = None
        
        self.padding = padding.symmetric(vertical=80, horizontal=50)
        self.spacing = 40
        
        if not self.page.database:
            self.page.database = AcademicData(self.page, db)
            self.page.database.load_from_db()
        
        # Check for redirect
        if not page.client_storage.get("user.validated") or not page.client_storage.get("user.email"):
            page.go("/auth")
        role = page.client_storage.get("user.role")
        if not role:
            page.go("/auth/role")
        elif role == "mahasiswa":
            page.go("/")
        if not page.client_storage.get("user.key"):
            page.snack_bar = SnackBar(
                content=Text("Key not found, please generate a new key", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            page.snack_bar.open = True
            page.update()
            page.go("/settings")

        self.controls = [
            Row(
                controls=[
                    IconButton(
                        icon=icons.ARROW_BACK,
                        on_click=lambda e: page.go("/"),
                    ),
                    Row(
                        controls=[
                            FilledTonalButton(
                                text="Sync Database",
                                on_click=self.sync_database,
                            ),
                            FilledButton(
                                icon=icons.ADD,
                                text="Add Data",
                                on_click=lambda e: page.go("/database/add")
                            )
                        ],
                        spacing=10
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            Container(
                DatabaseValidateListView(page),
                expand=True
            )
        ]

    def sync_database(self, e):
        self.page.splash = ProgressBar()
        self.page.snack_bar = SnackBar(
            content=Text("Syncing database...", color=colors.ON_PRIMARY_CONTAINER),
            bgcolor=colors.PRIMARY_CONTAINER,
        )
        self.page.snack_bar.open = True
        self.page.update()

        try:
            self.page.database.save_to_db()
            self.page.database.load_from_db()

            self.page.snack_bar = SnackBar(
                content=Text("Database synced", color=colors.ON_PRIMARY_CONTAINER),
                bgcolor=colors.PRIMARY_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.update()

            if self.page.route == "/database":
                self.page.go("/database/d")
            else:
                self.page.go("/database")

        except Exception as e:
            self.page.snack_bar = SnackBar(
                content=Text(f"Error syncing database: {e}", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.splash = None
            self.page.update()