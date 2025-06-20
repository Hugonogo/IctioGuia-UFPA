import flet as ft

class WelcomeScreen:
    def __init__(self, page: ft.Page, app_bar, navigate_to_infoscreen):
        self.page = page
        self.app_bar = app_bar
        self.navigate_to_info = navigate_to_infoscreen

    def build(self):
        max_width = 700  # Largura máxima para centralizar em telas grandes

        return ft.Column(
            [
                self.app_bar,
                ft.Container(height=30),

                # Título
                ft.Text(
                    "🎣 Bem-vindo ao Identifica Pescado",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="#1A202C",
                ),

                ft.Container(height=25),

                # Texto introdutório centralizado
                ft.Container(
                    content=ft.Text(
                        "Este aplicativo foi desenvolvido com o objetivo de ajudar você, consumidor, a identificar corretamente espécies de pescados comercializados em filé. "
                        "Ele é fruto de um projeto acadêmico da Universidade Federal do Pará (UFPA), desenvolvido no Instituto de Medicina Veterinária (IMV) do campus de Castanhal, "
                        "Pará, com foco na proteção do consumidor e na promoção da transparência no mercado de pescados.",
                        size=15,
                        text_align=ft.TextAlign.CENTER,
                        color="#2D3748"
                    ),
                    width=max_width,
                    padding=ft.Padding(20, 10, 20, 10),
                    border_radius=8,
                ),

                ft.Container(height=10),

                # Texto explicativo centralizado
                ft.Container(
                    content=ft.Text(
                        "Aqui, você pode analisar as características sensoriais e morfológicas do pescado — como cor, aspecto, mioseptos, miômeros e outras — "
                        "e verificar se o produto corresponde corretamente à espécie informada na etiqueta. Assim, contribuímos juntos para combater fraudes na comercialização de peixes "
                        "e garantimos uma escolha mais segura e consciente.",
                        size=15,
                        text_align=ft.TextAlign.CENTER,
                        color="#2D3748"
                    ),
                    width=max_width,
                    padding=ft.Padding(20, 10, 20, 10),
                    border_radius=8,
                ),

                ft.Container(height=30),

                # Botão iniciar
                ft.ElevatedButton(
                    "Iniciar",
                    width=220,
                    on_click=lambda e: self.navigate_to_info(),
                    bgcolor="#3182CE",
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=20,
                    ),
                ),

                ft.Container(height=40),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=self.page.width,
            scroll=ft.ScrollMode.AUTO  # Garante que funcione bem em qualquer tamanho de tela
        )

    def show(self):
        """Exibe a Tela de Boas-Vindas."""
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()
