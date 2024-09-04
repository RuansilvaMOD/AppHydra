import tkinter as tk
import pyautogui
import threading
import keyboard
from utils.key_listener import KeyListener

class AutoClick:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.style = parent_app.style
        self.auto_click_active = False
        self.auto_click_interval = 100  # Intervalo em milissegundos
        self.auto_click_thread = None
        self.selected_key = 'left'  # Inicialmente botão esquerdo do mouse
        self.auto_click_button_key = 'f8'  # Tecla para acionar o AutoClick

        # Inicializa a captura de teclas
        self.key_listener = KeyListener(self.auto_click_button_key, self.toggle_auto_click_key)

    def show(self):
        """Exibe a interface de configuração do AutoClick."""
        self.frame = tk.Frame(self.parent_app.main_frame, bg=self.style.colors.primary)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Adiciona o título da seção
        title_label = tk.Label(self.frame, text="AutoClick Settings",
                               bg=self.style.colors.primary, fg=self.style.colors.light,
                               font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=10)

        # Adiciona o menu suspenso para selecionar a tecla ou botão
        key_frame = tk.Frame(self.frame, bg=self.style.colors.primary)
        key_frame.pack(pady=10, fill=tk.X)

        select_key_label = tk.Label(key_frame, text="Select key (EX: Left):",
                                    bg=self.style.colors.primary, fg=self.style.colors.light,
                                    font=('Helvetica', 14))
        select_key_label.pack(side=tk.LEFT, padx=10)

        key_options = [
            "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "left", "right", "middle",  # Botões do mouse
            "shift", "ctrl", "alt", "space", "enter", "esc", "tab", "backspace", "delete", "home", "end", "pageup", "pagedown", "up", "down", "left", "right"
        ]
        self.selected_key_var = tk.StringVar(value=self.selected_key)
        key_menu = tk.OptionMenu(key_frame, self.selected_key_var, *key_options,
                                 command=self.update_key_selection)
        key_menu.config(bg=self.style.colors.info, fg=self.style.colors.light, font=('Helvetica', 14))
        key_menu.pack(side=tk.LEFT)

        # Adiciona o campo para definir o intervalo entre cliques
        interval_frame = tk.Frame(self.frame, bg=self.style.colors.primary)
        interval_frame.pack(pady=10, fill=tk.X)

        interval_label = tk.Label(interval_frame, text="Interval between clicks (ms):",
                                  bg=self.style.colors.primary, fg=self.style.colors.light,
                                  font=('Helvetica', 14))
        interval_label.pack(side=tk.LEFT, padx=10)

        self.interval_var = tk.StringVar(value=str(self.auto_click_interval))
        interval_entry = tk.Entry(interval_frame, textvariable=self.interval_var, width=10,
                                  font=('Helvetica', 14))
        interval_entry.pack(side=tk.LEFT)
        interval_entry.bind("<FocusOut>", self.update_interval)  # Atualiza o intervalo ao sair do foco

        # Adiciona o campo para selecionar a tecla de ativação do AutoClick
        activate_key_frame = tk.Frame(self.frame, bg=self.style.colors.primary)
        activate_key_frame.pack(pady=10, fill=tk.X)

        activate_key_label = tk.Label(activate_key_frame, text="Key to active AutoClick:",
                                      bg=self.style.colors.primary, fg=self.style.colors.light,
                                      font=('Helvetica', 14))
        activate_key_label.pack(side=tk.LEFT, padx=10)

        activate_key_options = [
            "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "shift", "ctrl", "alt", "space", "enter", "esc", "tab", "backspace", "delete", "home", "end", "pageup", "pagedown", "up", "down", "left", "right"
        ]
        self.activate_key_var = tk.StringVar(value=self.auto_click_button_key)
        activate_key_menu = tk.OptionMenu(activate_key_frame, self.activate_key_var, *activate_key_options,
                                          command=self.update_activate_key_selection)
        activate_key_menu.config(bg=self.style.colors.info, fg=self.style.colors.light, font=('Helvetica', 14))
        activate_key_menu.pack(side=tk.LEFT)

    def update_key_selection(self, selection):
        """Atualiza a seleção da tecla ou botão."""
        self.selected_key = selection

    def update_activate_key_selection(self, selection):
        """Atualiza a tecla de ativação do AutoClick e reinicializa o ouvinte de teclas."""
        self.auto_click_button_key = selection
        self.key_listener.update_key(self.auto_click_button_key)

    def update_interval(self, event):
        """Atualiza o intervalo entre cliques com base na entrada do usuário."""
        try:
            new_interval = int(self.interval_var.get())
            if new_interval >= 100:
                self.auto_click_interval = new_interval
            else:
                self.auto_click_interval = 100  # Valor mínimo
                self.interval_var.set('100')
        except ValueError:
            self.auto_click_interval = 100
            self.interval_var.set('100')

    def toggle_auto_click_key(self):
        """Alterna o estado do AutoClick ao pressionar a tecla configurada."""
        if not self.auto_click_active:
            self.auto_click_active = True
            self.start_auto_click()
        else:
            self.auto_click_active = False
            self.stop_auto_click()

    def start_auto_click(self):
        """Inicia o auto click em uma thread separada."""
        if self.auto_click_thread is None or not self.auto_click_thread.is_alive():
            self.auto_click_thread = threading.Thread(target=self.auto_click)
            self.auto_click_thread.start()

    def auto_click(self):
        """Executa o auto click a cada intervalo definido."""
        while self.auto_click_active:
            if self.selected_key in ["left", "right", "middle"]:
                pyautogui.mouseDown(button=self.selected_key)  # Pressiona o botão do mouse selecionado
                pyautogui.mouseUp(button=self.selected_key)  # Libera o botão do mouse selecionado
            else:
                pyautogui.press(self.selected_key)  # Pressiona a tecla selecionada
            threading.Event().wait(self.auto_click_interval / 1000)

    def stop_auto_click(self):
        """Para o auto click."""
        self.auto_click_active = False
        if self.auto_click_thread:
            self.auto_click_thread.join()
