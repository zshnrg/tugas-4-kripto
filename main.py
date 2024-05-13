from flet import *
from router import router
from lib.academic_db import Mahasiswa, Course, AcademicData
from services.db import db

async def main(page: Page):
    page.title = "XIS"
    page.theme = Theme(
        color_scheme_seed=colors.BLUE_GREY
    )
    page.theme_mode = ThemeMode.LIGHT

    page.database = AcademicData(page, db)
    page.database.load_from_db()
    
    def route_change(route):
        page.views.clear()
        print(page.route)
        page.views.append(
            router(page, page.route)
        )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.goto(top_view.route)
 
    page.on_route_change = route_change
    page.on_view_pop = view_pop
 
    print("Main page")
    page.go("/")

if __name__ == "__main__":
    app(target=main, assets_dir="assets")