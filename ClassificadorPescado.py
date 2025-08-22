import flet as ft
import joblib
import pandas as pd
import numpy as np
import os
import logging
import unicodedata
import re

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para padronizar texto (mesma do Código 1)
def padronizar_texto(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize('NFKD', text.lower()).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^\w\s/.\0-9]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class ClassifierScreen:
    def __init__(self, page: ft.Page, app_bar):
        self.page = page
        self.app_bar = app_bar

    def obter_opcoes_dropdown(self, df, label_encoders):
        """Extrair opções únicas para os dropdowns, respeitando o LabelEncoder."""
        caracteristicas = [
            "cor_aspecto",
            "septo_horizontal",
            "perimisio",
            "miomeros_mioseptos",
            "musculatura"
        ]
        opcoes = {}
        for car in caracteristicas:
            if car in df.columns and car in label_encoders:
                opcoes[car] = sorted(list(label_encoders[car].classes_))
        return opcoes

    def show(self):
        """Exibe a tela de classificação."""
        self.page.clean()
        try:
            # Carregar dados JSON para extrair opções
            df = pd.read_json("Dados.json")
            # Aplicar padronização ao DataFrame
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].apply(padronizar_texto)

            # Verificar se o arquivo .pkl existe
            model_file = "modelo_arvore.pkl"
            if not os.path.exists(model_file):
                raise FileNotFoundError(f"Arquivo {model_file} não encontrado.")

            # Carregar modelo usando joblib
            try:
                with open(model_file, "rb") as f:
                    modelo_data = joblib.load(f)
                logging.info(f"Modelo carregado com sucesso de {model_file}")
            except Exception as e:
                logging.error(f"Erro ao carregar o modelo: {e}")
                raise ValueError(f"Erro ao carregar o modelo: {str(e)}")

            # Desempacotar os dados salvos no pickle
            modelo_arvore = modelo_data["model"]
            label_encoders = modelo_data["label_encoders"]
            le_y = modelo_data["le_y"]
            feature_names = modelo_data["features"]

            # Obter opções para dropdowns com base no LabelEncoder
            opcoes_dropdown = self.obter_opcoes_dropdown(df, label_encoders)
            if not opcoes_dropdown.get("miomeros_mioseptos", []):
                raise ValueError("Nenhuma opção encontrada para miomeros_mioseptos")

        except Exception as e:
            logging.error(f"Erro ao carregar dados ou modelo: {e}")
            self.page.add(
                ft.Column(
                    [
                        self.app_bar,
                        ft.Container(height=15),
                        ft.Text(f"Erro ao carregar dados ou modelo: {str(e)}", color="#EF4444", size=16)
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

        # Seleções iniciais
        selecoes = [opcoes_dropdown[key][0] for _, key in perguntas]
        current_step = ft.Ref[int]()
        current_step.current = 0
        selected_option = ft.Ref[str]()

        # Componentes da UI
        titulo = ft.Text(
            "Classificador de Pescados",
            size=26,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color="#1A202C"
        )
        pergunta_texto = ft.Text("", size=16, text_align=ft.TextAlign.CENTER)
        resultado_texto = ft.Text("", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        debug_texto = ft.Text("", size=12, color="#6B7280")
        dropdown = ft.Dropdown(
            width=320,
            text_size=13,
            options=[],
            content_padding=8,
            bgcolor="#FFFFFF",
            color="#2D3748",
            border_color="#D1D5DB"
        )

        def is_image_path(value):
            image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
            caminho = os.path.join("assets", os.path.basename(value)) if "assets" not in value.lower() else value
            caminho = caminho.replace("\\", "/")
            return any(caminho.lower().endswith(ext) for ext in image_extensions) and os.path.exists(caminho)

        def create_option_card(opt, is_selected):
            caminho = os.path.join("assets", os.path.basename(opt)) if "assets" not in opt.lower() else opt
            caminho = caminho.replace("\\", "/")
            content = (
                ft.Image(
                    src=caminho,
                    width=400,
                    height=400,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("Erro ao carregar imagem", size=12, color="#EF4444")
                )
                if is_image_path(caminho)
                else ft.Text(opt, size=12, color="#2D3748", weight=ft.FontWeight.NORMAL, no_wrap=False, width=100, tooltip=opt)
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
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color="#D1D5DB", offset=ft.Offset(0, 1))
            )

        def select_option(opt):
            selected_option.current = opt
            selecoes[current_step.current] = opt
            atualizar_tela()

        def atualizar_tela():
            self.page.clean()
            if current_step.current < len(perguntas):
                label, key = perguntas[current_step.current]
                pergunta_texto.value = label
                debug_texto.value = f"Passo {current_step.current + 1}/{len(perguntas)}"
                botoes = []
                if current_step.current > 0:
                    botoes.append(ft.ElevatedButton("Voltar", on_click=voltar, width=140, height=45, bgcolor="#FFFFFF", color="#184175", elevation=2))
                botoes.append(ft.ElevatedButton("Próximo", on_click=proximo, width=140, height=45, bgcolor="#184175", color="#FFFFFF", elevation=2))
                
                if key == "miomeros_mioseptos":
                    option_cards = [create_option_card(opt, opt == selected_option.current) for opt in opcoes_dropdown[key]]
                    input_component = ft.Container(
                        content=ft.Column(
                            option_cards,
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        width=320,
                        height=300,
                        padding=15,
                        bgcolor="#E5E7EB",
                        border_radius=10,
                        border=ft.border.all(1, "#D1D5DB"),
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="#D1D5DB", offset=ft.Offset(0, 2))
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
                # Prever usando o modelo .pkl
                try:
                    dados_input = []
                    avisos = []
                    for idx, (_, key) in enumerate(perguntas):
                        valor = padronizar_texto(selecoes[idx])
                        le = label_encoders[key]
                        if valor in le.classes_:
                            dados_input.append(le.transform([valor])[0])
                        else:
                            # Usar o primeiro valor válido como padrão
                            valor_padrao = le.classes_[0]
                            dados_input.append(le.transform([valor_padrao])[0])
                            avisos.append(f"Valor inválido para '{key}': {valor}. Usando '{valor_padrao}' como padrão.")
                            logging.warning(f"Valor inválido para '{key}': {valor}. Usando '{valor_padrao}'.")
                    X_input = np.array([dados_input])
                    pred_index = modelo_arvore.predict(X_input)[0]
                    especie_predita = le_y.inverse_transform([pred_index])[0]
                    resultado_texto.value = f"Espécie prevista: {especie_predita}"
                    resultado_texto.color = "#10B981"
                    if avisos:
                        resultado_texto.value += "\n" + "\n".join(avisos)
                        resultado_texto.color = "#F59E0B"  # Amarelo para indicar aviso
                    logging.info(f"Previsão realizada: {especie_predita}")
                except Exception as e:
                    resultado_texto.value = f"Erro na previsão: {str(e)}"
                    resultado_texto.color = "#EF4444"
                    logging.error(f"Erro na previsão: {e}")
                
                self.page.add(
                    ft.Column(
                        [
                            self.app_bar,
                            titulo,
                            ft.Container(height=15),
                            resultado_texto,
                            ft.Container(height=15),
                            ft.ElevatedButton("Reiniciar", on_click=reiniciar, width=180, height=45, bgcolor="#184175", color="#FFFFFF", elevation=2)
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

        selected_option.current = selecoes[perguntas.index(("Miômeros/Mioseptos", "miomeros_mioseptos"))]
        atualizar_tela()

def main(page: ft.Page):
    page.title = "Classificador de Pescados"
    app_bar = ft.AppBar(title=ft.Text("Classificador"), bgcolor="#184175", color="#FFFFFF")
    classifier = ClassifierScreen(page, app_bar)
    classifier.show()

if __name__ == "__main__":
    ft.app(target=main)