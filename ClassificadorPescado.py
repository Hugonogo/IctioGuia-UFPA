import flet as ft
from classification import carregar_dados, preparar_dados, treinar_arvore, prever
import json
import os

class ClassifierScreen:
    def __init__(self, page: ft.Page, app_bar):
        self.page = page
        self.app_bar = app_bar

    def obter_opcoes_dropdown(self, df):
        """Extrair opções únicas para os dropdowns e image/text options."""
        caracteristicas = [
            "cor_aspecto",
            "septo_horizontal",
            "perimisio",
            "miomeros_mioseptos",
            "musculatura"
        ]
        opcoes = {car: set() for car in caracteristicas}
        
        for car in caracteristicas:
            opcoes[car] = sorted(df[car].unique().tolist())
        
        return opcoes

    def show(self):
        """Exibe a tela de classificação."""
        self.page.controls.clear()
        
        # Carregar dados e treinar modelo (árvore de decisão)
        try:
            # Carregar dados do JSON
            df = carregar_dados("Pescados.json")
            # Preparar dados para árvore
            X, y, label_encoders, le_y, feature_names = preparar_dados(df)
            # Treinar a árvore
            modelo_arvore = treinar_arvore(X, y)
            # Obter opções para os dropdowns
            opcoes_dropdown = self.obter_opcoes_dropdown(df)
            if not opcoes_dropdown["miomeros_mioseptos"]:
                raise ValueError("Nenhuma opção encontrada para miomeros_mioseptos")
        except Exception as e:
            self.page.add(
                ft.Column(
                    [
                        self.app_bar,
                        ft.Container(height=15),
                        ft.Text(f"Erro ao carregar dados: {str(e)}", color="#EF4444", size=16)
                    ]
                )
            )
            self.page.update()
            return

        # Configuração das perguntas
        perguntas = [
            ("Cor e Aspecto", "cor_aspecto"),
            ("Septo Horizontal", "septo_horizontal"),
            ("Perimísio", "perimisio"),
            ("Miômeros/Mioseptos", "miomeros_mioseptos"),
            ("Musculatura", "musculatura")
        ]
        
        # Armazenar seleções do usuário
        selecoes = [opcoes_dropdown[key][0] for _, key in perguntas]
        current_step = ft.Ref[int]()
        current_step.current = 0
        selected_option = ft.Ref[str]()

        # Componentes da UI
        titulo = ft.Text(
            "Classificador de Pescados",
            size=22 if self.page.width < 400 else 26,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color="#1A202C"
        )
        pergunta_texto = ft.Text("", size=14 if self.page.width < 400 else 16, text_align=ft.TextAlign.CENTER)
        debug_texto = ft.Text("", size=12, color="#6B7280")
        dropdown = ft.Dropdown(
            width=0.9 * self.page.width if self.page.width < 400 else 320,
            text_size=13,
            options=[],
            content_padding=8,
            bgcolor="#FFFFFF",
            color="#2D3748",
            border_color="#D1D5DB"
        )
        resultado_texto = ft.Text(
            "",
            size=14 if self.page.width < 400 else 16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        def is_image_path(value):
            image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
            caminho = os.path.join("assets", os.path.basename(value)) if "assets" not in value.lower() else value
            caminho = caminho.replace("\\", "/")
            return any(caminho.lower().endswith(ext) for ext in image_extensions) and os.path.exists(caminho)

        def create_option_card(opt, is_selected):
            caminho = os.path.join("assets", os.path.basename(opt)) if "assets" not in opt.lower() else opt
            caminho = caminho.replace("\\", "/")  # Corrige para barras

            content = (
                ft.Image(
                    src=caminho,  # removido o "/" do começo
                    width=400,
                    height=400,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("Erro ao carregar imagem", size=12, color="#EF4444")
                )
                if is_image_path(caminho)
                else ft.Text(
                    opt,
                    size=12,
                    color="#2D3748",
                    weight=ft.FontWeight.NORMAL,
                    no_wrap=False,
                    width=100,
                    tooltip=opt
                )
            )
            return ft.Container(
                content=content,
                width=200,
                height=200,
                alignment=ft.alignment.center,
                bgcolor="#FFFFFF",
                border_radius=8,
                border=ft.border.all(3, "#184175" if is_selected else "#D1D5DB"),
                on_click=lambda e: select_option(opt),
                data=opt,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=3,
                    color="#D1D5DB",
                    offset=ft.Offset(0, 1)
                )
            )

        def select_option(opt):
            selected_option.current = opt
            selecoes[current_step.current] = opt
            atualizar_tela()

        def atualizar_tela():
            self.page.controls.clear()
            if current_step.current < 5:
                debug_texto.value = f"Passo {current_step.current + 1}/{len(perguntas)}"
            
            
            if current_step.current < len(perguntas):
                label, key = perguntas[current_step.current]
                pergunta_texto.value = label
                
                botoes = []
                if current_step.current > 0:
                    botoes.append(
                        ft.ElevatedButton(
                            "Voltar",
                            on_click=voltar,
                            width=0.45 * self.page.width if self.page.width < 400 else 140,
                            height=45,
                            bgcolor="#FFFFFF",
                            color="#184175",
                            elevation=2
                        )
                    )
                botoes.append(
                    ft.ElevatedButton(
                        "Próximo",
                        on_click=proximo,
                        width=0.45 * self.page.width if self.page.width < 400 else 140,
                        height=45,
                        bgcolor="#184175",
                        color="#FFFFFF",
                        elevation=2
                    )
                )
                
                if key == "miomeros_mioseptos":
                    option_cards = [
                        create_option_card(opt, opt == selected_option.current)
                        for opt in opcoes_dropdown[key]
                    ]
                    input_component = ft.Container(
                        content=ft.Column(
                            option_cards,
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        width=0.9 * self.page.width if self.page.width < 400 else 320,
                        height=300,
                        padding=15,
                        bgcolor="#E5E7EB",
                        border_radius=10,
                        border=ft.border.all(1, "#D1D5DB"),
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=5,
                            color="#D1D5DB",
                            offset=ft.Offset(0, 2)
                        )
                    )
                else:
                    dropdown.label = label
                    dropdown.options = [ft.dropdown.Option(opt) for opt in opcoes_dropdown[key]]
                    dropdown.value = selecoes[current_step.current]
                    input_component = dropdown
                
                self.page.add(
                    ft.Column(
                        [
                            self.app_bar,
                            ft.Container(height=8),
                            titulo,
                            ft.Container(height=8),
                            pergunta_texto,
                            ft.Container(height=8),
                            input_component,
                            ft.Container(height=8),
                            ft.Row(botoes, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                            ft.Container(height=8),
                            debug_texto
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=self.page.width,
                        spacing=8
                    )
                )
            else:
                # Prever usando a árvore
                especie_predita = prever(
                    modelo_arvore, 
                    label_encoders, 
                    le_y, 
                    feature_names, 
                    selecoes
                )
                if especie_predita:
                    resultado_texto.value = f"Espécie prevista: {especie_predita}"
                    resultado_texto.color = "#10B981"
                    print(selecoes)
                else:
                    resultado_texto.value = "Erro: Um ou mais valores selecionados não são válidos."
                    resultado_texto.color = "#EF4444"
                
                self.page.add(
                    ft.Column(
                        [
                            self.app_bar,
                            ft.Container(height=15),
                            titulo,
                            ft.Container(height=15),
                            resultado_texto,
                            ft.Container(height=15),
                            ft.ElevatedButton(
                                "Reiniciar",
                                on_click=reiniciar,
                                width=0.5 * self.page.width if self.page.width < 400 else 180,
                                height=45,
                                bgcolor="#184175",
                                color="#FFFFFF",
                                elevation=2
                            ),
                            ft.Container(height=8)
                            
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=self.page.width
                    )
                )
            self.page.update()

        def proximo(e):
            if perguntas[current_step.current][1] == "miomeros_mioseptos":
                selecoes[current_step.current] = selected_option.current
            else:
                selecoes[current_step.current] = dropdown.value
            current_step.current += 1
            atualizar_tela()

        def voltar(e):
            if perguntas[current_step.current][1] == "miomeros_mioseptos":
                selecoes[current_step.current] = selected_option.current
            else:
                selecoes[current_step.current] = dropdown.value
            current_step.current -= 1
            atualizar_tela()

        def reiniciar(e):
            current_step.current = 0
            selecoes[:] = [opcoes_dropdown[key][0] for _, key in perguntas]
            selected_option.current = selecoes[perguntas.index(("Miômeros/Mioseptos", "miomeros_mioseptos"))]
            resultado_texto.value = ""
            atualizar_tela()

        # Inicializar a primeira tela
        selected_option.current = selecoes[perguntas.index(("Miômeros/Mioseptos", "miomeros_mioseptos"))]
        atualizar_tela()