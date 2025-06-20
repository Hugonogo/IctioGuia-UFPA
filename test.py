import flet as ft


def main(page: ft.Page):
    page.title = "Teste Imagem"
    page.add(
        ft.Image(
            src="assets/mm02.png",
            width=300,
            height=300,
            error_content=ft.Text("Erro ao carregar imagem", color="red")
        )
    )


ft.app(target=main)
