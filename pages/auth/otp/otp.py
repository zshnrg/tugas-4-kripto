from flet import *
from services.db import db

class OTPContainer(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.width = 500
        self.bgcolor = colors.BACKGROUND
        self.border_radius = 25
        self.border = border.all(1, colors.OUTLINE)
        self.padding = padding.symmetric(vertical=80, horizontal=50)
        
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        self.email = self.page.client_storage.get("user.email")
        print(self.email)

        self.otp_1 = TextField(
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            autofocus=True,
            expand=True,
            text_align=TextAlign.CENTER,
            input_filter=NumbersOnlyInputFilter(),
            on_change=self.change_1
        )

        self.otp_2 = TextField(
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            expand=True,
            text_align=TextAlign.CENTER,
            input_filter=NumbersOnlyInputFilter(),
            on_change=self.change_2
        )

        self.otp_3 = TextField(
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            expand=True,
            text_align=TextAlign.CENTER,
            input_filter=NumbersOnlyInputFilter(),
            on_change=self.change_3
        )
        
        self.otp_4 = TextField(
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            expand=True,
            text_align=TextAlign.CENTER,
            input_filter=NumbersOnlyInputFilter(),
            on_change=self.change_4
        )

        self.otp_5 = TextField(
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            expand=True,
            text_align=TextAlign.CENTER,
            input_filter=NumbersOnlyInputFilter(),
            on_change=self.change_5
        )

        self.otp_6 = TextField(
            border_radius=10,
            border_color=colors.OUTLINE,
            bgcolor=colors.SURFACE,
            expand=True,
            text_align=TextAlign.CENTER,
            input_filter=NumbersOnlyInputFilter(),
            on_change=self.change_6
        )

        self.submit_button = FilledButton(
            text="Lanjut",
            on_click=self.submit
        )
        

        self.content = Column(
            controls=[
                IconButton(
                    icon=icons.ARROW_BACK,
                    on_click=lambda e: self.page.go("/auth"),
                ),
                Container(
                    Column(
                        controls=[
                            Text("Verifikasi", size=36, weight=FontWeight.BOLD),
                            Text(f"Kami telah mengirimkan kode verifikasi ke email {self.email.split('@')[0][:3]}****@{self.email.split('@')[1]}. Masukan kode verifikasi untuk melanjutkan", size=15, color=colors.ON_SURFACE_VARIANT),
                            Row(
                                controls=[
                                    self.otp_1,
                                    self.otp_2,
                                    self.otp_3,
                                    self.otp_4,
                                    self.otp_5,
                                    self.otp_6,
                                ],
                                spacing=4
                            ),
                            self.submit_button
                        ],
                        spacing=40
                    ),
                    padding=padding.symmetric(vertical=0, horizontal=50)
                ),
            ],
            spacing=40
        )

    def submit(self, e):
        if len(self.otp_1.value) != 1:
            self.otp_1.focus()
            return
        elif len(self.otp_2.value) != 1:
            self.otp_2.focus()
            return
        elif len(self.otp_3.value) != 1:
            self.otp_3.focus()
            return
        elif len(self.otp_4.value) != 1:
            self.otp_4.focus()
            return
        elif len(self.otp_5.value) != 1:
            self.otp_5.focus()
            return
        otp = self.otp_1.value + self.otp_2.value + self.otp_3.value + self.otp_4.value + self.otp_5.value + self.otp_6.value
        
        self.page.splash = ProgressBar()
        self.submit_button.disabled = True
        self.page.update()

        # Validate OTP
        try:
            user = db.verifyOTP(self.email, otp)

            db.insertUser(self.email)

            self.page.client_storage.set("user.validated", True)
            self.page.go("/auth/role")
        except Exception as e:
            self.page.splash = None
            self.submit_button.disabled = False
            self.page.snack_bar = SnackBar(
                content=Text("Kode verifikasi salah", color=colors.ON_ERROR_CONTAINER),
                bgcolor=colors.ERROR_CONTAINER,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

    def back(self, e):
        self.page.client_storage.remove("user.email")
        self.page.go("/auth")
    

    def change_1(self, e):
        if len(self.otp_1.value) == 1:
            self.otp_2.focus()

    def change_2(self, e):
        if len(self.otp_2.value) == 1:
            self.otp_3.focus()

    def change_3(self, e):
        if len(self.otp_3.value) == 1:
            self.otp_4.focus()

    def change_4(self, e):
        if len(self.otp_4.value) == 1:
            self.otp_5.focus()

    def change_5(self, e):
        if len(self.otp_5.value) == 1:
            self.otp_6.focus()

    def change_6(self, e):
        self.submit(e)
        
class OTPView(View):
    def __init__(self, page: Page):
        super().__init__()
        self.route = "/auth/otp"
        self.page = page
        self.page.splash = None

        # Check for redirect
        if not page.client_storage.get("user.email"):
            page.go("/auth")
        elif page.client_storage.get("user.validated"):
            page.go("/auth/role")
        elif page.client_storage.get("user.role"):
            page.go("/")
        
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.padding = 15
        self.bgcolor = colors.BACKGROUND
        
        self.controls = [
            OTPContainer(page)
        ]