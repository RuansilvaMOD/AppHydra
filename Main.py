import tkinter as tk
from ttkbootstrap import Style
from components.navbar import Navbar
from components.auto_click import AutoClick
from components.join_sim import JoinSim
from components.log_bot import LogBot
from components.paste_bot import PasteBot

class HydraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydra JoinSim")
        self.root.geometry("1000x500")
        self.root.minsize(1000, 500)


        # Centraliza a janela
        self.center_window()

        # Cria um estilo com ttkbootstrap
        self.style = Style(theme='solar')

        # Configura a interface
        self.navbar = Navbar(self.root, self.style, self.load_content)
        self.main_frame = self.create_main_frame()

        # Inicializa a categoria padrão
        self.current_category = None

        # Inicializa o AutoClick e JoinSim
        self.auto_click = AutoClick(self)
        self.join_sim = None  # Inicializa join_sim como None
        self.log_bot = None
        self.paste_bot = None

    def center_window(self):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_main_frame(self):
        """Cria o frame principal à direita."""
        main_frame = tk.Frame(self.root, bg=self.style.colors.primary,
                              relief='flat', bd=4, padx=20, pady=20)  # Fundo com cor primária e padding
        main_frame.grid(row=0, column=1, sticky='nsew')

        # Configura a proporção da coluna principal e a linha para ocupar toda a altura da tela
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Adiciona conteúdo inicial ao frame principal
        self.default_label = tk.Label(main_frame, text="Hydra App by: Ruan",
                                      bg=self.style.colors.primary, fg=self.style.colors.light,
                                      font=('Helvetica', 16, 'italic'), anchor='center', wraplength=500)
        self.default_label.pack(expand=True)

        return main_frame

    def load_content(self, category):
        """Carrega o conteúdo correspondente à categoria selecionada."""
        # Limpa o frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_category = category  # Atualiza a categoria atual

        if category == "AutoClick":
            self.auto_click.show()

        elif category == "JoinSim":
            # Cria e mostra o conteúdo da categoria JoinSim
            if self.join_sim is None:
                self.join_sim = JoinSim(self.main_frame, self.style)
            self.join_sim.create_content()

        elif category == "LogBot":
            # Cria e mostra o conteúdo da categoria LogBot
            if self.log_bot is None:
                self.log_bot = LogBot(self.main_frame, self.style)
            self.log_bot.create_content()

        elif category == "PasteBot":
            # Cria e mostra o conteúdo da categoria PasteBot
            if self.paste_bot is None:
                self.paste_bot = PasteBot(self.main_frame, self.style)
            self.paste_bot.create_content()



if __name__ == "__main__":
    root = tk.Tk()
    app = HydraApp(root)
    root.mainloop()
