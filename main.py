import flet as ft
from AppManager import AppManager

def main(page: ft.Page):
    app_manager = AppManager(page)
    app_manager.show_welcome_screen()

ft.app(target=main, view=ft.AppView.FLET_APP)