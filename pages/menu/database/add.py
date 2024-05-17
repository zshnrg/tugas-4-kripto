from flet import *
from services.db import db
from lib.academic_db import AcademicData, Mahasiswa, Course, EnrolledCourse

class MataKuliahSearch(Column):
    def __init__ (self, page: Page, data: dict[str, dict]):
        super().__init__()
        self.page = page
        self.spacing = 10

        self.data = data
        self.kode = []
        for kode in data:
            self.kode.append(kode)
        
        self.kode_text_field = TextField(
            label="Kode Mata Kuliah",
            on_change=self.on_change,
            border_color=colors.OUTLINE,
            border_radius=15,
            max_length=6,
            input_filter=InputFilter(regex_string="[A-Z0-9]"),
        )

        self.nama_text_field = TextField(
            label="Nama Mata Kuliah",
            border_color=colors.OUTLINE,
            border_radius=15,
            read_only=True
        )

        self.sks_text_field = TextField(
            label="SKS",
            border_color=colors.OUTLINE,
            border_radius=15,
            read_only=True,
            input_filter=NumbersOnlyInputFilter(),
            max_length=1,
            expand=True
        )

        self.nilai_text_field = TextField(
            label="Indeks",
            border_color=colors.OUTLINE,
            border_radius=15,
            input_filter=InputFilter(regex_string="[A-E]"),
            max_length=2,
            expand=True
        )

        self.kode_search_result = ListView(
            padding=padding.symmetric(vertical=10)
        )
        self.kode_search_result.visible = False

        self.controls = [
            self.kode_text_field,
            self.kode_search_result,
            self.nama_text_field,
            Row(
                controls=[
                    self.sks_text_field,
                    self.nilai_text_field
                ]
            )
        ]

    def on_change(self, e):
        self.kode_search_result.visible = True
        self.kode_search_result.controls = []

        for kode in self.kode:
            if self.kode_text_field.value in kode:
                self.kode_search_result.controls.append(
                    ListTile(
                        title=Text(kode),
                        data=kode,
                        on_click=self.on_click
                    )
                )
        if len(self.kode_search_result.controls) == 1:
            self.nama_text_field.value = self.data[self.kode_search_result.controls[0].data]["nama"]
            self.sks_text_field.value = self.data[self.kode_search_result.controls[0].data]["sks"]
            self.kode_search_result.visible = False
        elif self.kode_search_result.controls == []:
            self.nama_text_field.read_only = False
            self.sks_text_field.read_only = False
            self.kode_search_result.visible = False
            self.nama_text_field.value = ""
            self.sks_text_field.value = ""
        else:
            self.nama_text_field.read_only = True
            self.sks_text_field.read_only = True
        self.page.update()

    def on_click(self, e: ControlEvent):
        self.kode_text_field.value = e.control.data
        self.kode_search_result.controls = []
        self.kode_search_result.visible = False

        self.nama_text_field.value = self.data[e.control.data]["nama"]
        self.sks_text_field.value = self.data[e.control.data]["sks"]
        self.page.update()

    def get_data(self):
        if self.nilai_text_field.value not in ["A", "AB", "B", "BC", "C", "D", "E"]:
            self.nilai_text_field.value = "E"
        return (self.kode_text_field.value, self.nama_text_field.value, self.sks_text_field.value, self.nilai_text_field.value)

class NIMSearch(Column):
    def __init__ (self, page: Page, data : dict[str, str]):
        super().__init__()
        self.page = page
        self.spacing = 10

        self.data = data
        self.nim = []
        for nim in data:
            self.nim.append(nim)
        
        self.nim_text_field = TextField(
            label="NIM",
            on_change=self.on_change,
            border_color=colors.OUTLINE,
            border_radius=15,
            input_filter=NumbersOnlyInputFilter(),
            max_length=8
        )

        self.name_text_field = TextField(
            label="Nama",
            border_color=colors.OUTLINE,
            border_radius=15,
            read_only=True
        )

        self.nim_search_result = ListView(
            padding=padding.symmetric(vertical=10)
        )
        self.nim_search_result.visible = False

        self.controls = [
            self.nim_text_field,
            self.nim_search_result,
            self.name_text_field
        ]

    def on_change(self, e):
        self.nim_search_result.visible = True
        self.nim_search_result.controls = []
        print(self.nim_text_field.value)
        print(self.nim)

        for nim in self.nim:
            if self.nim_text_field.value in nim:
                self.nim_search_result.controls.append(
                    ListTile(
                        title=Text(nim),
                        data=nim,
                        on_click=self.on_click
                    )
                )
        if len(self.nim_search_result.controls) == 1:
            self.name_text_field.value = self.data[self.nim_search_result.controls[0].data]
            self.nim_search_result.visible = False
        elif self.nim_search_result.controls == []:
            self.name_text_field.read_only = False
            self.nim_search_result.visible = False
            self.name_text_field.value = ""
        else:
            self.name_text_field.read_only = True
        self.page.update()

    def on_click(self, e: ControlEvent):
        self.nim_text_field.value = e.control.data
        self.nim_search_result.controls = []
        self.nim_search_result.visible = False

        self.name_text_field.value = self.data[e.control.data]
        self.page.update()

    def get_data(self):
        return (self.nim_text_field.value, self.name_text_field.value)

class AddListView(ListView):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.padding = padding.symmetric(horizontal=50)
        self.spacing = 40

        if not self.page.database:
            self.page.database = AcademicData(self.page, db)
            self.page.database.load_from_db()

        self.nim_nama_dict = {}
        for mahasiswa in self.page.database.mahasiswa:
            self.nim_nama_dict[mahasiswa.nim] = mahasiswa.nama

        self.mata_kuliah_dict = {}
        for course in self.page.database.available_mata_kuliah:
            self.mata_kuliah_dict[course.kode] = {
                "nama": course.nama,
                "sks": course.sks
            }

        self.nim = NIMSearch(self.page, self.nim_nama_dict)
        self.mata_kuliah = MataKuliahSearch(self.page, self.mata_kuliah_dict)

        self.submit_button = FilledButton(
            text="Submit",
            on_click=self.on_submit,
        )

        self.controls = [
            Text("Tambah Data", size=36, weight=FontWeight.BOLD),
            Divider(),
            self.nim,
            self.mata_kuliah,
            self.submit_button
        ]

    def on_submit(self, e):
        nim, nama = self.nim.get_data()
        kode, nama_mk, sks, nilai = self.mata_kuliah.get_data()

        if nim == "" or nama == "" or kode == "" or nama_mk == "" or sks == "" or nilai == "":
            self.page.snack_bar = SnackBar(
                content=Text("Data tidak boleh kosong", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        try:
            mahasiswa = self.page.database.get_mahasiswa(nim)
            course = self.page.database.get_course(kode)

            if not mahasiswa:
                mahasiswa = Mahasiswa(nim, nama)
                self.page.database.add_mahasiswa(mahasiswa)
            if not course:
                course = Course(kode, nama_mk, sks)
                self.page.database.add_course(course)
            
            mahasiswa.add_course(EnrolledCourse(course, nilai))
            self.page.database.save()

            self.page.snack_bar = SnackBar(
                content=Text("Data berhasil ditambahkan", color=colors.ON_PRIMARY_CONTAINER),
                bgcolor=colors.PRIMARY_CONTAINER
            )
            self.page.snack_bar.open = True
            self.page.update()

            self.page.go("/database")
        except Exception as e:
            self.page.snack_bar = SnackBar(
                content=Text(f"Error: {e}", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER
            )
            self.page.snack_bar.open = True
            self.page.update()

            
        


class AddView(View):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.page.route = "/database/add"
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
        
        self.controls = [
            IconButton(
                icon=icons.ARROW_BACK,
                on_click=lambda e: page.go("/database"),
            ),
            Container(
                content=AddListView(page),
                expand=True
            )
        ]
        