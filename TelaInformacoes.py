import flet as ft

class InfoScreen:
    def __init__(self, page: ft.Page, app_bar, navigate_to_classifier):
        self.page = page
        self.app_bar = app_bar
        self.navigate_to_classifier = navigate_to_classifier

        # Conteúdo dos cards: texto e caminho/imagem (substitua pelos seus arquivos)
        self.cards = [
            {
                "title": "Sobre o Aplicativo",
                "text": (
                    "Este aplicativo foi desenvolvido com o objetivo de auxiliar consumidores na identificação correta "
                    "de espécies de pescados comercializados em filé, contribuindo para a prevenção de fraudes e garantindo a transparência na comercialização."
                ),
                "image": "assets/sobre.png"
            },
            {
                "title": "Termos Importantes",
                "text": (
                    "• Miômeros: Segmentos musculares em formato de 'V' visíveis nos peixes.\n\n"
                    "• Mioseptos: Linhas brancas que separam os miômeros, visíveis no corte do filé.\n\n"
                    "• Septo horizontal: Estrutura divisória no músculo do peixe, importante na identificação.\n\n"
                    "• Perimísio: Tecido conjuntivo que envolve os miômeros.\n\n"
                    "• Cor e aspecto: Avaliação visual da carne do pescado (rosada, branca, presença de manchas, etc.)."
                ),
                "image": "assets/termos.png"
            }
        ]
        self.current_index = 0
        self.image_modal = None

    def build(self):
        max_width = 700

        card = self.cards[self.current_index]

        content = ft.Column(
            [
                self.app_bar,
                ft.Container(height=20),
                ft.Text(
                    card["title"],
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="#1A202C",
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Text(
                        card["text"],
                        size=15,
                        text_align=ft.TextAlign.LEFT,
                        color="#2D3748",
                    ),
                    width=max_width,
                    padding=ft.Padding(20, 10, 20, 10),
                ),
                ft.Container(height=20),

                # Imagem clicável dentro do GestureDetector
                ft.Container(
                    content=ft.GestureDetector(
                        content=ft.Image(
                            src=card["image"],
                            width=300,
                            height=200,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=10,
                        ),
                        on_tap=self.open_image_modal,
                    ),
                    alignment=ft.alignment.center,
                ),

                ft.Container(height=30),

                # Navegação entre cards
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Anterior",
                            on_click=self.previous_card,
                            disabled=self.current_index == 0,
                        ),
                        ft.Container(width=20),
                        ft.ElevatedButton(
                            "Próximo",
                            on_click=self.next_card,
                            disabled=self.current_index == len(self.cards) - 1,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Container(height=40),

                # Botão para seguir para o classificador
                ft.ElevatedButton(
                    "Ir para o Classificador",
                    width=250,
                    on_click=lambda e: self.navigate_to_classifier(),
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
            scroll=ft.ScrollMode.AUTO,
            width=self.page.width,
        )
        return content

    def show(self):
        self.page.controls.clear()
        self.page.add(self.build())
        self.page.update()

    def previous_card(self, e):
        if self.current_index > 0:
            self.current_index -= 1
            self.show()

    def next_card(self, e):
        if self.current_index < len(self.cards) - 1:
            self.current_index += 1
            self.show()

    def open_image_modal(self, e):
        card = self.cards[self.current_index]

        # Remove modal antigo se existir
        if self.image_modal:
            self.page.overlay.clear()
            self.image_modal = None

        zoomed_image = ft.GestureDetector(
            content=ft.Container(
                content=ft.Image(
                    src=card["image"],
                    fit=ft.ImageFit.CONTAIN,
                    width=600,
                    height=400,
                ),
                bgcolor="black",
                padding=10,
                border_radius=10,
            ),
            on_tap=self.close_image_modal,  # fecha ao clicar na imagem também
        )

        self.image_modal = ft.Stack(
            controls=[
                ft.Container(
                    bgcolor="rgba(0,0,0,0.7)",
                    expand=True,
                    on_click=self.close_image_modal,  # fecha ao clicar fora da imagem
                ),
                ft.Container(content=zoomed_image, alignment=ft.alignment.center),
            ]
        )

        self.page.overlay.append(self.image_modal)  # adiciona como modal acima da tela
        self.page.update()

    def close_image_modal(self, e):
        if self.image_modal:
            self.page.overlay.clear()  # remove modal da overlay
            self.image_modal = None
            self.page.update()