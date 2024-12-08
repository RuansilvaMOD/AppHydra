import tkinter as tk
import threading
from time import sleep

import time
import numpy as np
from PIL import ImageChops, Image
import mss
import pygetwindow as gw
import pyautogui
import easyocr
import requests
import ctypes
import os

from PIL import ImageEnhance, ImageChops


class LogBot:
    def __init__(self, parent_frame, style):
        self.parent_frame = parent_frame
        self.style = style
        self.frame = None
        self.is_active = False
        self.stop_event = threading.Event()  # Evento para sinalizar a interrupção
        self.search_path = self.get_image_path('Inv.png')

    def get_image_path(self, image_name):
        """Obtém o caminho da imagem relativo ao diretório do script."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, '..', 'images', image_name)

    def create_content(self):
        """Cria o conteúdo da categoria LogBot."""
        if self.frame:
            self.frame.destroy()  # Remove o conteúdo existente

        self.frame = tk.Frame(self.parent_frame, bg=self.style.colors.primary)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Adiciona o título da seção
        title_label = tk.Label(self.frame, text="LogBot Settings",
                               bg=self.style.colors.primary, fg=self.style.colors.light,
                               font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=10)

        # Frame para os controles de input
        control_frame = tk.Frame(self.frame, bg=self.style.colors.primary)
        control_frame.pack(pady=10, fill=tk.X)

        # Input para quantidade de TPS
        self.tps_var = tk.StringVar()
        tps_label = tk.Label(control_frame, text="Token:",
                             bg=self.style.colors.primary, fg=self.style.colors.light,
                             font=('Helvetica', 14))
        tps_label.pack(side=tk.LEFT, padx=10)

        tps_entry = tk.Entry(control_frame, textvariable=self.tps_var, width=5,
                             font=('Helvetica', 14))
        tps_entry.pack(side=tk.LEFT)

        # Botão Toggle para ligar/desligar o LogBot
        self.toggle_button = tk.Button(control_frame, text="Activate LogBot",
                                       bg="orange", fg=self.style.colors.light,
                                       font=('Helvetica', 14), command=self.toggle_active)
        self.toggle_button.pack(side=tk.LEFT, padx=10)

    def toggle_active(self):
        """Ativa ou desativa o LogBot."""
        if self.is_active:
            self.is_active = False
            self.stop_event.set()  # Sinaliza para interromper as ações
            self.toggle_button.config(text="Activate LogBot", bg="orange")
            print("LogBot desativado.")
        else:
            self.is_active = True
            self.stop_event.clear()  # Reseta o evento de parada
            self.toggle_button.config(text="Deactivate LogBot", bg=self.style.colors.danger)
            print("LogBot ativado.")
            self.start_logbot_process()

    def start_logbot_process(self):
        """Inicia o processo de captura e envio da requisição a cada 1 minuto."""
        def process():
            while not self.stop_event.is_set():
                if not self.is_window_minimized('ArkAscended'):
                    self.maximize_and_bring_to_front_ark_ascended()
                    self.capture_and_send_request()
                else:
                    print("Janela do ArkAscended minimizada ou alterada. Interrompendo o LogBot.")
                    break
                sleep(60)  # Aguarda 1 minuto antes de executar novamente

        # Inicia o processo em uma thread separada
        threading.Thread(target=process, daemon=True).start()

    monitor_area = {'top': 100, 'left': 100, 'width': 200, 'height': 200}

    def capture_screen(area):
        """Captura uma área específica da tela."""
        with mss.mss() as sct:
            screenshot = sct.grab(area)
            return Image.frombytes('RGB', screenshot.size, screenshot.rgb)

    def detect_changes(img1, img2):
        """Compara duas imagens e detecta mudanças."""
        diff = ImageChops.difference(img1, img2)
        # Converter a diferença em array numpy para análise
        diff_array = np.array(diff)
        return np.any(diff_array > 50)

    def maximize_and_bring_to_front_ark_ascended(self):
        """Maximiza a janela do ArkAscended e a coloca em primeiro plano."""
        try:
            windows = gw.getWindowsWithTitle('ArkAscended')
            if windows:
                ark_window = windows[0]
                self.bring_window_to_front(ark_window._hWnd)
                print("Janela do ArkAscended maximizada e trazida para frente.")
                sleep(2)
            else:
                print("Janela do ArkAscended não encontrada.")
        except Exception as e:
            print(f"Ocorreu um erro ao maximizar a janela: {e}")

    def capture_and_send_request(self):
        """Captura a tela, realiza OCR e envia a requisição HTTP."""
        try:
            sleep(2);
            # Capturar uma área da tela
            # Coordenadas do canto superior esquerdo (Top-Left)
            top_left_x, top_left_y = 554, 277  # Substitua pelos valores desejados

            # Coordenadas do canto inferior direito (Bottom-Right)
            bottom_right_x, bottom_right_y = 704, 316  # Substitua pelos valores desejados

            # Calculando a largura e a altura
            width = bottom_right_x - top_left_x
            height = bottom_right_y - top_left_y

            # Definir a região de captura
            region = (top_left_x, top_left_y, width, height)

            # Capturar a área da tela
            screenshot = pyautogui.screenshot(region=region)
            screenshot_path = r"C:\Users\ruans\Downloads\aa\captura_tela.png"
            screenshot = screenshot.convert("L")

            # Aumentar o contraste
            enhancer = ImageEnhance.Contrast(screenshot)
            screenshot = enhancer.enhance(2);



            screenshot.save("area_capturada.png")
            screenshot.save(screenshot_path, format="PNG")


            # Realizar OCR na imagem
            reader = easyocr.Reader(['en', 'pt'])
            results = reader.readtext("area_capturada.png")

            # Processar e exibir os resultados
            texto_capturado1 = " ".join([text for (_, text, _) in results])
            print("Tribe-Members:",  texto_capturado1)

            sleep(1);
            # Capturar uma área da tela
            # Coordenadas do canto superior esquerdo (Top-Left)
            top_left_x, top_left_y = 765, 200  # Substitua pelos valores desejados

            # Coordenadas do canto inferior direito (Bottom-Right)
            bottom_right_x, bottom_right_y = 1156, 815  # Substitua pelos valores desejados

            # Calculando a largura e a altura
            width = bottom_right_x - top_left_x
            height = bottom_right_y - top_left_y

            # Definir a região de captura
            region = (top_left_x, top_left_y, width, height)

            # Capturar a área da tela
            screenshot = pyautogui.screenshot(region=region)
            screenshot_path = r"C:\Users\ruans\Downloads\aa\captura_tela2.png"
            screenshot = screenshot.convert("L")

            # Aumentar o contraste
            enhancer = ImageEnhance.Contrast(screenshot)
            screenshot = enhancer.enhance(2);

            screenshot.save("area_capturada2.png")
            screenshot.save(screenshot_path, format="PNG")


            # Realizar OCR na imagem
            reader = easyocr.Reader(['en', 'pt'])
            results = reader.readtext("area_capturada2.png")

            # Processar e exibir os resultados
            texto_capturado = " ".join([text for (_, text, _) in results])
            partes = texto_capturado.split("Day")

            # Exibir os elementos da lista

            print("Tribe-Log:",  texto_capturado)

            url = "http://localhost:8080/api/tribeLog/log"

            # Criando o JSON com a variável
            payload = {
                "token": self.tps_var.get(),  # Adicionando a variável no JSON
                "tribeMembers": texto_capturado1,
                "log": texto_capturado
            }

            # Realizando a requisição HTTP POST
            url = "http://localhost:8080/api/tribeLog/log"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                print("Requisição bem-sucedida:", response.json())
            else:
                print("Erro na requisição:", response.status_code, response.text)
        except Exception as e:
            print(f"Ocorreu um erro durante a captura ou envio: {e}")

    def bring_window_to_front(self, hwnd):
        """Usa ctypes para colocar a janela com o identificador hwnd em primeiro plano."""
        try:
            ctypes.windll.user32.SetForegroundWindow(hwnd)
        except Exception as e:
            print(f"Ocorreu um erro ao trazer a janela para frente: {e}")

    def is_window_minimized(self, window_title):
        """Verifica se a janela com o título especificado está minimizada."""
        try:
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                window = windows[0]
                return window.isMinimized
            return False
        except Exception as e:
            print(f"Erro ao verificar o estado da janela: {e}")
            return False


# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    style = None  # Substitua pelo seu estilo de interface
    bot = LogBot(root, style)
    bot.create_content()
    root.mainloop()
