import flet as ft
from TelaBoasVindas import WelcomeScreen
from ClassificadorPescado import ClassifierScreen
from TelaInformacoes import InfoScreen  # ✅ Importa a nova tela

class AppManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_screen = None
        self.setup_page()
        self.navigation_drawer = self.create_navigation_drawer()
        self.app_bar = self.create_app_bar()

    def setup_page(self):
        """Configura as propriedades da página."""
        self.page.title = "Classificador de Pescados"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.padding = ft.padding.symmetric(horizontal=10, vertical=15)
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#184175",
                on_primary="#D1D5DB",
                background="#F5F7FA",
                on_background="#2D3748",
                surface="#D1D5DB",
                on_surface="#2D3748",
                secondary="#4B5EAA",
                on_secondary="#D1D5DB",
            ),
            text_theme=ft.TextTheme(
                body_medium=ft.TextStyle(color="#2D3748", size=14),
                headline_medium=ft.TextStyle(color="#1A202C", weight=ft.FontWeight.BOLD, size=22),
            )
        )
        self.page.bgcolor = "#F5F7FA"
        self.page.window_maximized = False
        self.page.window_width = 360
        self.page.window_height = 640
        self.page.update()

    def create_app_bar(self):
        """Cria a barra superior com o menu hamburguer."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.MENU,
                        icon_color="#FFFFFF",
                        on_click=self.toggle_navigation_drawer,
                        tooltip="Menu"
                    ),
                    ft.Text("Classificador", color="#FFFFFF", size=18, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True
            ),
            bgcolor="#184175",
            padding=10,
            height=60,
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color="#000000",
                offset=ft.Offset(0, 2)
            )
        )

    def create_navigation_drawer(self):
        """Cria o menu hamburguer."""
        return ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.HOME,
                    label="Boas-Vindas",
                    selected_icon=ft.Icons.HOME_FILLED,
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.INFO,
                    label="Informações",
                    selected_icon=ft.Icons.INFO_OUTLINE,
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.FACT_CHECK,
                    label="Classificador",
                    selected_icon=ft.Icons.FACT_CHECK_OUTLINED,
                ),
            ],
            on_change=self.on_navigation_change,
            bgcolor="#F5F7FA",
        )

    def toggle_navigation_drawer(self, e):
        """Abre ou fecha o menu hamburguer."""
        self.page.drawer = self.navigation_drawer
        self.page.drawer.open = not self.page.drawer.open
        self.page.update()

    def on_navigation_change(self, e):
        """Lida com a mudança de tela no menu hamburguer."""
        index = e.control.selected_index
        if index == 0:
            self.show_welcome_screen()
        elif index == 1:
            self.show_info_screen()
        elif index == 2:
            self.show_classifier_screen()
        self.page.drawer.open = False
        self.page.update()

    def show_welcome_screen(self):
        """Exibe a Tela de Boas-Vindas."""
        welcome_screen = WelcomeScreen(self.page, self.app_bar, self.show_info_screen)  # ✅ Vai para InfoScreen
        welcome_screen.show()
        self.current_screen = "welcome"
        self.navigation_drawer.selected_index = 0
        self.page.update()

    def show_info_screen(self):
        """Exibe a Tela de Informações."""
        info_screen = InfoScreen(self.page, self.app_bar, self.show_classifier_screen)  # ✅ Vai para classificador
        info_screen.show()
        self.current_screen = "info"
        self.navigation_drawer.selected_index = 1
        self.page.update()

    def show_classifier_screen(self):
        """Exibe a Tela de Classificação."""
        classifier_screen = ClassifierScreen(self.page, self.app_bar)
        classifier_screen.show()
        self.current_screen = "classifier"
        self.navigation_drawer.selected_index = 2
        self.page.update()
