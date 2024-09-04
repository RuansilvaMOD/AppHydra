import tkinter as tk

class Navbar:
    def __init__(self, root, style, load_content_callback):
        self.root = root
        self.style = style
        self.load_content_callback = load_content_callback
        self.create_navbar()

    def create_navbar(self):
        """Cria a navbar com as categorias à esquerda."""
        self.navbar_frame = tk.Frame(self.root, bg=self.style.colors.dark, width=220,
                                     relief='raised', bd=3)  # Fundo escuro com borda sutil
        self.navbar_frame.grid(row=0, column=0, sticky='ns')

        categories = ["AutoClick", "JoinSim", "LogBot", "PasteBot"]

        # Configura o número de linhas baseado na quantidade de categorias
        total_categories = len(categories)
        for i, category in enumerate(categories):
            btn = tk.Button(self.navbar_frame, text=category, bg=self.style.colors.info,
                            fg=self.style.colors.light, relief=tk.FLAT, anchor='center',
                            font=('Helvetica', 16),  # Aumenta o tamanho da fonte
                            cursor="hand2", width=20, height=2,  # Aumenta o tamanho do botão
                            command=lambda c=category: self.load_content_callback(c))
            btn.grid(row=i, column=0, sticky='ew', padx=10, pady=10)

            # Configura a borda arredondada (com uma abordagem alternativa, pois tkinter não suporta bordas arredondadas diretamente)
            btn.config(
                highlightbackground=self.style.colors.dark,  # Borda ao redor do botão
                highlightcolor=self.style.colors.dark,
                borderwidth=2
            )
            # Remove o efeito de passar o mouse por cima
            btn.bind("<Enter>", lambda e, b=btn: None)
            btn.bind("<Leave>", lambda e, b=btn: None)

        # Configura a proporção das linhas da navbar para dividir igualmente o espaço vertical
        for i in range(total_categories):
            self.navbar_frame.grid_rowconfigure(i, weight=1)

        # Configura a proporção da coluna da navbar para centralizar o texto
        self.navbar_frame.grid_columnconfigure(0, weight=1)
