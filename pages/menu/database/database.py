from flet import *
from services.db import db
from lib.academic_db import AcademicData

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
                ]
            ),
            border=border.only(bottom=BorderSide(width=1, color=colors.OUTLINE)),
            padding=padding.symmetric(vertical=10),
        )

        self.controls = [
            self.header
        ]

        for mahasiswa in academic_data.mahasiswa:
            column = Column()

            for mk in mahasiswa.mata_kuliah:
                column.controls.append(
                    Row(
                        controls=[
                            Container(Text(mk.course.kode, size=16, expand=True, text_align=TextAlign.CENTER), expand=1),
                            Container(Text(mk.course.nama, size=16, expand=True,), expand=2),
                            Container(Text(str(mk.course.sks), size=16, expand=True, text_align=TextAlign.CENTER), expand=1),
                            Container(Text(mk.indeks, size=16, expand=True, text_align=TextAlign.CENTER), expand=1),
                        ],
                    )
                )

            self.controls.append(
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=Text(mahasiswa.nim, size=16, text_align=TextAlign.CENTER),
                                expand=1,
                            ),
                            Container(
                                content=Text(mahasiswa.nama, size=16),
                                expand=1,
                            ),
                            Container(
                                content=column,
                                expand=5,
                            ),
                            Container(
                                content=Text(mahasiswa.ipk, size=16, text_align=TextAlign.CENTER),
                                expand=1,
                            ),
                            Container(
                                content=Text(mahasiswa.signature if mahasiswa.signature else "-", size=16, text_align=TextAlign.CENTER),
                                expand=3,
                            ),
                        ]
                    ),
                    border=border.only(top=BorderSide(width=1, color=colors.OUTLINE_VARIANT)),
                    padding=padding.symmetric(vertical=5),
                )
                
            )
                
class DatabaseListView(ListView):
    def __init__ (self, page: Page):
        super().__init__()
        self.page = page
        self.padding = padding.symmetric(horizontal=50)
        self.spacing = 40

        if not self.page.database:
            self.page.database = AcademicData(self.page, db)
            self.page.database.load_from_db()

        self.is_encrypted = self.page.database.is_encrypted
        if self.is_encrypted:
            self.segment = {"encrypted"}
        else:
            self.segment = {"raw"}

        self.table = Table(page, self.page.database)

        self.controls = [
            Text("Database", size=36, weight=FontWeight.BOLD),
            Divider(),
            SegmentedButton(
                on_change=self.handleChange,
                show_selected_icon=False,
                selected=self.segment,
                segments=[
                    Segment(
                        value="raw",
                        label=Text("Raw"),
                    ),
                    Segment(
                        value="encrypted",
                        label=Text("Encrypted"),
                    ),
                ]
            ),
            self.table
        ]

    def handleChange(self, e: ControlEvent):
        if e.data[2:-2] == "encrypted":
            self.page.database.encrypt(self.page.client_storage.get("user.key"))
            self.page.go("/database/e")
        else:
            self.page.database.decrypt(self.page.client_storage.get("user.key"))
            self.page.go("/database/d")
        
        
class DatabaseView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/database"
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
                DatabaseListView(page),
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