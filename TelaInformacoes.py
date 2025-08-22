import flet as ft

class InfoScreen:
    def __init__(self, page: ft.Page, app_bar, navigate_to_classifier):
        self.page = page
        self.app_bar = app_bar
        self.navigate_to_classifier = navigate_to_classifier
        self.image_modal = None
        # Conteúdo das seções
        self.sections = [
            {
                "title": "Sobre o Aplicativo",
                "text": (
                    "Este aplicativo foi desenvolvido com o objetivo de auxiliar consumidores na identificação correta "
                    "de espécies de pescados comercializados em filé, contribuindo para a prevenção de fraudes e garantindo a transparência na comercialização."
                ),
                "image": "none"
            },
            {
                "title": "Termos Importantes",
                "text": (
                    "• Miômeros: são blocos musculares segmentados, dispostos em forma de 'W' ou 'Z', que compõem a musculatura dos peixes e permitem o movimento ondulatório durante o nado.\n\n"
                    "• Mioseptos: são finas camadas de tecido conjuntivo que separam e conectam os miômeros ao esqueleto, contribuindo para a organização estrutural e a eficiência do movimento muscular.\n\n"
                    "• O septo horizontal: é uma faixa que divide os músculos de cima e de baixo no corpo do peixe. Em muitas espécies, ele é fácil de ver e costuma ter uma linha vermelha ao longo dele, o que pode ajudar a identificar qual é o tipo de peixe.\n\n"
                    "• Perimísio: é um tecido conjuntivo que envolve grupos de fibras musculares nos peixes, podendo variar em presença\n\n"
                    "• Cor e aspecto: Avaliação visual da carne do pescado (rosada, branca, amarelado, etc.).\n\n"
                    "• Musculatura: é formada por blocos de miômeros e mioseptos. Ela pode ser branca, vermelha ou tons intermediários entre branco e vermelho, como rosado, e sua aparência ajuda a identificar a espécie e evitar trocas nos filés ou postas."
                ),
                "image": "none"
            },
            {
                "title": "Formato dos Miômeros e Mioseptos",
                "text": (
                    "Circuitos dos Miômeros e Mioseptos"
                ),
                "image": "assets/MM.png"
            },
            {
                "title": "\nFICHA DE ESPÉCIES\n Tilápia (Oreochromis niloticus)",
                "text": (
                    "• Cor e Aspecto: Carne clara a rosada, com linhas rosadas ou avermelhadas. Após o cozimento, fica muito branca e tem sabor suave. Pode ter gosto ou cheiro de terra ou mofo por causa de MIB ou Geosmina. Filé arredondado, sem gordura acumulada por baixo da pele.\n\n"
                    "• Septo Horizontal: Visível e bem marcado.\n\n"
                    "• Perimísio: Geralmente ausente.\n\n"
                    "• Miômeros e Mioseptos: Ondulado com curva convexa antes do septo horizontal e trajeto final quebrado e angulo agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca, com faixa vermelha perto da espinha e no final do rabo, além de pontos vermelhos espalhados."
                ),
                "image": "assets/file_tilapia.png"
            },
            {
                "title": "Dourada (Brachyplatystoma flavicans)",
                "text": (
                    "• Cor e Aspecto: Carne branca ou levemente rosada. Com pele, parte de cima cinza e ventre branco.\n\n"
                    "• Septo Horizontal: Visível.\n\n"
                    "• Perimísio: Geralmente ausente.\n\n"
                    "• Miômeros e Mioseptos: Ondulado com curva convexa antes do septo horizontal e trajeto final quebrado e angulo agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca, com linha de sangue menos intensa que outros bagres."
                ),
                "image": "none"
            },
            {
                "title": "Mapará (Hypophthalmus spp.)",
                "text": (
                    "• Cor e Aspecto: Carne branca ou levemente amarelada. Com pele, parte de cima escura e barriga clara.\n\n"
                    "• Septo Horizontal: Visível.\n\n"
                    "• Perimísio: Geralmente ausente.\n\n"
                    "• Miômeros e Mioseptos: Ondulado com curva convexa antes do septo horizontal e trajeto final quebrado e angulo agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca, com linha de sangue bem delimitada."
                ),
                "image": "none"
            },
            {
                "title": "Piramutaba (Brachyplatystoma vaillantii)",
                "text": (
                    "• Cor e Aspecto: Carne branca ou levemente rosada. No congelado, pode ficar com aspecto “amanteigado” e cheiro de gordura velha.\n\n"
                    "• Septo Horizontal: Encoberto pela musculatura vermelha.\n\n"
                    "• Perimísio: Geralmente ausente.\n\n"
                    "• Miômeros e Mioseptos: Ondulado com curva convexa antes do septo horizontal e trajeto final quebrado e angulo agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Musculatura vermelha intensa ao castanho escuro, ao longo do septo, podendo se espalhar no subcutâneo e cobrir o desenho das fibras."
                ),
                "image": "assets/file_piramutaba.png"
            },
            {
                "title": "Filhote (Brachyplatystoma filamentosum)",
                "text": (
                    "• Cor e Aspecto: Carne clara levemente amarelada. Filés de Piraíba (adultos) são muito grandes.\n\n"
                    "• Septo Horizontal: Encoberto pela musculatura vermelha.\n\n"
                    "• Perimísio: Ausente.\n\n"
                    "• Miômeros e Mioseptos: Muito ondulado com curva convexa antes do septo horixontal com trajeto final ondulado e angulo muito agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Musculatura vermelha intensa e escura ao longo do septo, cobrindo o desenho das fibras nessa região."
                ),
                "image": "none"
            },
            {
                "title": "Surubim (Pseudoplatystoma spp.)",
                "text": (
                    "• Cor e Aspecto: Carne branca ou levemente rosada, podendo ser laranja quando fresca. Pode ter gordura que deixa gosto de ranço. Ao congelar, a cor laranja fica mais clara.\n\n"
                    "• Septo Horizontal: Visível, escuro e às vezes coberto por gordura.\n\n"
                    "• Perimísio: Geralmente ausente.\n\n"
                    "• Miômeros e Mioseptos: Ondulado com curva convexa antes do septo horizontal e trajeto final quebrado e angulo agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca, com musculatura vermelha/marrom ao longo do septo e gordura acumulada nessa região."
                ),
                "image": "assets/file_surubim.png"
            },
            {
                "title": "Pescada Amarela (Cynoscion acoupa)",
                "text": (
                    "• Cor e Aspecto: Carne rosada nos filés frescos e mais amarelada nos congelados.\n\n"
                    "• Septo Horizontal: Visível.\n\n"
                    "• Perimísio: Ausente.\n\n"
                    "• Miômeros e Mioseptos: Ondulado sem curva convexa antes do septo horizontal com trajeto final ondulado com angulo agudo na região posterior e menos agudo anterior.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca."
                ),
                "image": "none"
            },
            {
                "title": "Tambaqui (Colossoma macropomum)",
                "text": (
                    "• Cor e Aspecto: Carne rosada.\n\n"
                    "• Septo Horizontal: Visível.\n\n"
                    "• Perimísio: Pouco visível.\n\n"
                    "• Miômeros e Mioseptos: Muito ondulado com curva convexa antes do septo horixontal com trajeto final ondulado e angulo muito agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca."
                ),
                "image": "assets/file_tambaqui.png"
            },
            {
                "title": "Pescada Gó (Macrodon ancylodon)",
                "text": (
                    "• Cor e Aspecto: Carne ligeiramente rosada.\n\n"
                    "• Septo Horizontal: Visível.\n\n"
                    "• Perimísio: Visível.\n\n"
                    "• Miômeros e Mioseptos: Muito quebrado com trajeto final quebrado e angulo muito agudo.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca."
                ),
                "image": "none"
            },
            {
                "title": "Pirarucu (Arapaima gigas)",
                "text": (
                    "• Cor e Aspecto: Carne ligeiramente rosada.\n\n"
                    "• Septo Horizontal: Visível.\n\n"
                    "• Perimísio: Visível.\n\n"
                    "• Miômeros e Mioseptos: Ondulado com trajeto final ondulado sem curva convexa antes do septo horizontal e ângulo agudo na porção posterior e menos agudo na porção anterior.\n\n"
                    "• Musculatura Branca, Intermediária e Vermelha: Predominantemente branca."
                ),
                "image": "none"
            }
        ]

    def build(self):
        max_width = 700
        # Cria uma lista de widgets para todas as seções
        content_sections = []
        for section in self.sections:
            section_widgets = [
                ft.Text(
                    section["title"],
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="#00A676",  # Cor do título ajustada para verde teal
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Text(
                        section["text"],
                        size=15,
                        text_align=ft.TextAlign.JUSTIFY,
                        color="#2D3748",
                    ),
                    width=max_width,
                    padding=ft.Padding(20, 10, 20, 10),
                    bgcolor="#FFFFFF",  # Fundo branco como nos cards da imagem
                    border_radius=16,  # Bordas arredondadas como na imagem
                ),
                ft.Container(height=20),
            ]
            # Adiciona imagem apenas se não for "none"
            if section["image"] != "none":
                section_widgets.extend([
                    ft.Container(
                        content=ft.GestureDetector(
                            content=ft.Image(
                                src=section["image"],
                                width=500,
                                height=300,
                                fit=ft.ImageFit.CONTAIN,
                                border_radius=10,
                            ),
                            on_tap=lambda e, img=section["image"]: self.open_image_modal(e, img),
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=30),
                ])
            else:
                section_widgets.append(ft.Container(height=20))
            content_sections.extend(section_widgets)

        content = ft.Column(
            [
                self.app_bar,
                ft.Container(height=20),
                *content_sections,
                ft.Container(height=40),
                ft.ElevatedButton(
                    "Classificar",
                    width=220,
                    on_click=lambda e: self.navigate_to_classifier(),
                    bgcolor="#00A676",  # Cor do botão ajustada para verde teal
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=24),
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

    def open_image_modal(self, e, image_src):
        # Não abre modal para imagens "none"
        if image_src == "none":
            return
        # Remove modal antigo se existir
        if self.image_modal:
            self.page.overlay.clear()
            self.image_modal = None
        zoomed_image = ft.GestureDetector(
            content=ft.Container(
                content=ft.Image(
                    src=image_src,
                    fit=ft.ImageFit.CONTAIN,
                    width=600,
                    height=400,
                ),
                bgcolor="black",
                padding=10,
                border_radius=10,
            ),
            on_tap=self.close_image_modal,
        )
        self.image_modal = ft.Stack(
            controls=[
                ft.Container(
                    bgcolor="rgba(0,0,0,0.7)",
                    expand=True,
                    on_click=self.close_image_modal,
                ),
                ft.Container(content=zoomed_image, alignment=ft.alignment.center),
            ]
        )
        self.page.overlay.append(self.image_modal)
        self.page.update()

    def close_image_modal(self, e):
        if self.image_modal:
            self.page.overlay.clear()
            self.image_modal = None
            self.page.update()