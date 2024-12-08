import tkinter as tk
import pygetwindow as gw
import ctypes
import os
import pyautogui
import pyautogui as pag
import threading
import keyboard

class PasteBot:
    def __init__(self, parent_frame, style):
        self.parent_frame = parent_frame
        self.style = style
        self.frame = None
        self.is_active = False
        self.stop_event = threading.Event()  # Evento para sinalizar a interrupção
        self.search_path = self.get_image_path('Inv.png')

    def get_image_path(self, image_name):
        """Obtém o caminho da imagem relativo ao diretório do script."""
        # Obtém o diretório do script atual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Define o caminho da imagem (assumindo que a pasta 'images' está no mesmo diretório que o script)
        return os.path.join(script_dir, '..', 'images', image_name)

    def create_content(self):
        """Cria o conteúdo da categoria PasteBot."""
        if self.frame:
            self.frame.destroy()  # Remove o conteúdo existente

        self.frame = tk.Frame(self.parent_frame, bg=self.style.colors.primary)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Adiciona o título da seção
        title_label = tk.Label(self.frame, text="PasteBot Settings",
                               bg=self.style.colors.primary, fg=self.style.colors.light,
                               font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=10)

        # Frame para os controles de input
        control_frame = tk.Frame(self.frame, bg=self.style.colors.primary)
        control_frame.pack(pady=10, fill=tk.X)

        # Input para quantidade de TPS
        self.tps_var = tk.IntVar(value=1)
        tps_label = tk.Label(control_frame, text="TPS Amount:",
                             bg=self.style.colors.primary, fg=self.style.colors.light,
                             font=('Helvetica', 14))
        tps_label.pack(side=tk.LEFT, padx=10)

        tps_entry = tk.Entry(control_frame, textvariable=self.tps_var, width=5,
                             font=('Helvetica', 14))
        tps_entry.pack(side=tk.LEFT)

        # Botão Toggle para ligar/desligar o PasteBot
        self.toggle_button = tk.Button(control_frame, text="Activate PasteBot",
                                       bg="orange", fg=self.style.colors.light,
                                       font=('Helvetica', 14), command=self.toggle_active)
        self.toggle_button.pack(side=tk.LEFT, padx=10)

    def toggle_active(self):
        """Ativa ou desativa o PasteBot."""
        if self.is_active:
            self.is_active = False
            self.stop_event.set()  # Sinaliza para interromper as ações
            self.toggle_button.config(text="Activate PasteBot", bg="orange")
            print("PasteBot desativado.")
        else:
            self.is_active = True
            self.stop_event.clear()  # Reseta o evento de parada
            self.toggle_button.config(text="Deactivate PasteBot", bg=self.style.colors.danger)
            print("PasteBot ativado.")
            self.maximize_and_bring_to_front_ark_ascended()

    def maximize_and_bring_to_front_ark_ascended(self):
        """Maximiza a janela do ArkAscended se ela estiver aberta e a coloca em primeiro plano."""
        try:
            windows = gw.getWindowsWithTitle('ArkAscended')
            if windows:
                ark_window = windows[0]  # Seleciona a primeira janela com o título correspondente
                self.bring_window_to_front(ark_window._hWnd)
                print("Janela do ArkAscended maximizada e trazida para frente.")

                while self.is_active:
                    tps_count = self.tps_var.get()
                    for _ in range(tps_count):
                        if self.stop_event.is_set():
                            return  # Interrompe imediatamente se o evento de parada for sinalizado

                        pag.keyDown('down')
                        pag.sleep(4)
                        pag.keyUp('down')

                        pag.press('r')
                        pag.sleep(5)
                        pag.keyDown('up')
                        pag.sleep(0.4)
                        pag.keyUp('up')

                        for _ in range(15):
                            if self.stop_event.is_set():
                                return  # Interrompe imediatamente se o evento de parada for sinalizado

                            pag.press('f')
                            pag.sleep(3)

                            try:
                                # Tenta localizar a imagem na tela
                                posicao = pyautogui.locateOnScreen(self.search_path, confidence=0.8)

                                if posicao:
                                    print("Imagem encontrada!")
                                    # Faça algo quando a imagem for encontrada

                                    pag.click(1272, 197)
                                    print("search clicado.")

                                    pag.sleep(3)
                                    pag.write('pa')
                                    print("Texto 'achat' escrito.")

                                    pag.sleep(3)
                                    pag.click(1372, 192)
                                    pag.sleep(0.2)
                                    pag.press('f')
                                    print("transfer clicado.")

                            except pyautogui.ImageNotFoundException:
                                print("Erro: Imagem não encontrada ou algo deu errado!")
                                # Faça algo se der erro ao procurar a imagem

                            pag.sleep(3)
                            pag.keyDown('left')
                            pag.sleep(0.32)
                            pag.keyUp('left')

                    if self.stop_event.is_set():
                        return  # Interrompe imediatamente se o evento de parada for sinalizado

                    pag.keyDown('down')
                    pag.sleep(3)
                    pag.keyUp('down')
                    pag.press('r')
                    pag.sleep(2)
                    pag.keyDown('up')
                    pag.sleep(0.4)
                    pag.keyUp('up')

                    for _ in range(10):
                        if self.stop_event.is_set():
                            return  # Interrompe imediatamente se o evento de parada for sinalizado

                        pag.sleep(1)
                        pag.press('e')
                        pag.sleep(2)
                        pag.keyDown('left')
                        pag.sleep(0.2)
                        pag.keyUp('left')

            else:
                print("Janela do ArkAscended não encontrada.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def bring_window_to_front(self, hwnd):
        """Usa ctypes para colocar a janela com o identificador hwnd em primeiro plano."""
        try:
            ctypes.windll.user32.SetForegroundWindow(hwnd)
        except Exception as e:
            print(f"Ocorreu um erro ao trazer a janela para frente: {e}")
