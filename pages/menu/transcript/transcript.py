from flet import *
from lib.academic_db import Mahasiswa, AcademicData
from services.db import db

class Table(Column):
    def __init__(self, page: Page, mahasiswa: Mahasiswa):
        super().__init__()
        self.page = page
        self.spacing = 0

        self.header = Container(
            content=Row(
                controls=[
                    Text("NIM", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER),
                    Text("Nama", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER),
                    Text("Kode Mata Kuliah", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER),
                    Text("Nama Mata Kuliah", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER),
                    Text("SKS", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER),
                    Text("Indeks", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER),
                    Text("IPK", size=16, weight=FontWeight.BOLD, expand=True, text_align=TextAlign.CENTER),
                ]
            ),
            border=border.only(bottom=BorderSide(width=1, color=colors.OUTLINE)),
            padding=padding.symmetric(vertical=10),
        )

        self.controls = [
            self.header,
        ]

        first = True
        for mk in mahasiswa.mata_kuliah:
            if first:
                self.controls.append(
                    Container(
                        content=Row(
                            controls=[
                                Text(mahasiswa.nim, size=16, expand=True, text_align=TextAlign.CENTER),
                                Text(mahasiswa.nama, size=16, expand=True,),
                                Text(mk.course.kode, size=16, expand=True, text_align=TextAlign.CENTER),
                                Text(mk.course.nama, size=16, expand=True, ),
                                Text(str(mk.course.sks), size=16, expand=True, text_align=TextAlign.CENTER),
                                Text(mk.indeks, size=16, expand=True, text_align=TextAlign.CENTER),
                                Text(mahasiswa.ipk, size=16, expand=True, text_align=TextAlign.CENTER),
                            ]
                        ),
                        border=border.only(top=BorderSide(width=1, color=colors.OUTLINE_VARIANT)),
                        padding=padding.symmetric(vertical=5),
                    )
                )
            else:
                self.controls.append(
                    Container(
                        content=Row(
                            controls=[
                                Text("", size=16, expand=True, text_align=TextAlign.CENTER),
                                Text("", size=16, expand=True,),
                                Text(mk.course.kode, size=16, expand=True, text_align=TextAlign.CENTER),
                                Text(mk.course.nama, size=16, expand=True, ),
                                Text(str(mk.course.sks), size=16, expand=True, text_align=TextAlign.CENTER),
                                Text(mk.indeks, size=16, expand=True, text_align=TextAlign.CENTER),
                                Text("", size=16, expand=True, text_align=TextAlign.CENTER),
                            ]
                        ),
                        border=border.only(top=BorderSide(width=1, color=colors.OUTLINE_VARIANT)),
                        padding=padding.symmetric(vertical=5),
                    )
                )
            first = False


class TranscriptListView(ListView):
    def __init__(self, page: Page, db: AcademicData):
        super().__init__()
        self.page = page
        self.padding = padding.symmetric(horizontal=50)
        self.spacing = 40

        self.nim_nama_dict = {}
        for mahasiswa in db.mahasiswa:
            self.nim_nama_dict[mahasiswa.nim] = mahasiswa.nama

        self.nim_text_field = TextField(
            label="NIM",
            on_change=self.on_nim_change,
            border_color=colors.OUTLINE,
            border_radius=15,
            input_filter=NumbersOnlyInputFilter(),
            
        )

        self.name_text_field = TextField(
            label="Nama",
            border_color=colors.OUTLINE,
            border_radius=15,
            read_only=True,
            expand=True,
        )

        self.nim_search_result = Column(
            expand=True
        )

        self.search_result_container = Container(
            content=self.nim_search_result,
            bgcolor=colors.SURFACE,
        )

        self.create_button = FilledButton(
            text="Buat Transkrip",
            on_click=self.on_create,
            disabled=True,
        )

        self.stack = Stack(
            controls=[
                self.create_button,
            ]
        )

        self.controls = [
            Text("Transkrip Akademik", size=36, weight=FontWeight.BOLD),
            Divider(),
            Row(
                controls=[
                    self.nim_text_field,
                    self.name_text_field
                ]
            ),
            self.stack,
            Divider(),
        ]

    def on_nim_change(self, e):
        if len(self.stack.controls) == 1:
            self.stack.controls.append(self.search_result_container)
            
        if len(self.controls) > 5:
            self.controls.pop()

        self.nim_search_result.controls = []
        self.create_button.disabled = True
        
        for nim, nama in self.nim_nama_dict.items():
            if self.nim_text_field.value in nim:
                self.nim_search_result.controls.append(
                    ListTile(
                        title=Text(nim + " - " + nama),
                        data=nim,
                        on_click=self.on_nim_search_result_click
                    )
                )
        
        if len(self.nim_search_result.controls) == 1 and len(self.nim_text_field.value) == 8:
            self.name_text_field.value = self.nim_nama_dict[self.nim_search_result.controls[0].data]
            self.controls.append(
                Table(self.page, self.page.database.get_mahasiswa(self.nim_search_result.controls[0].data))
            )
        elif len(self.nim_search_result.controls) == 0 or len(self.nim_text_field.value) == 0:
            self.nim_search_result.controls = []
            self.name_text_field.value = ""
        else:
            self.name_text_field.value = ""
        self.page.update()

    def on_nim_search_result_click(self, e):
        self.stack.controls.pop()

        if len(self.controls) > 5:
            self.controls.pop()

        self.nim_text_field.value = e.control.data
        self.name_text_field.value = self.nim_nama_dict[e.control.data]
        self.controls.append(
            Table(self.page, self.page.database.get_mahasiswa(e.control.data))
        )

        self.nim_search_result.controls = []
        self.create_button.disabled = False

        self.page.update()

    def on_create(self, e):
        self.page.go("/transcript/create/" + self.nim_text_field.value)

class TranscriptView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.route = "/transcript"
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
            IconButton(
                icon=icons.ARROW_BACK,
                on_click=lambda e: page.go("/"),
            ),
            Container(
                content=TranscriptListView(page, self.page.database),
            )
        ]