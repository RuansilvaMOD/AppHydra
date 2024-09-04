# components/joinsim.py

import tkinter as tk

class LogBot:
    def __init__(self, parent_frame, style):
        self.parent_frame = parent_frame
        self.style = style
        self.frame = None

    def create_content(self):
        """Cria o conteúdo da categoria LogBot."""
        if self.frame:
            self.frame.destroy()  # Remove o conteúdo existente

        self.frame = tk.Frame(self.parent_frame, bg=self.style.colors.primary)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Adiciona o título da seção
        title_label = tk.Label(self.frame, text="LogBot - As coming in next update",
                               bg=self.style.colors.primary, fg=self.style.colors.light,
                               font=('Helvetica', 18, 'bold'), anchor='center')
        title_label.pack(expand=True)
