import tkinter as tk
import pygetwindow as gw
import ctypes
import os
import cv2
import numpy as np
import pyautogui as pag

class JoinSim:
    def __init__(self, parent, style):
        self.parent = parent
        self.style = style
        self.frame = None
        self.is_active = False
        # Caminho das imagens
        self.press_start_path = self.get_image_path('Press_Start.png')
        self.join_game_path = self.get_image_path('Join_Game.png')
        self.search_path = self.get_image_path('Search.png')
        self.found_path = self.get_image_path('Found.png')
        self.join_path = self.get_image_path('Join.png')

    def get_image_path(self, image_name):
        """Obtém o caminho da imagem relativo ao diretório do script."""
        # Obtém o diretório do script atual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Define o caminho da imagem (assumindo que a pasta 'images' está no mesmo diretório que o script)
        return os.path.join(script_dir, '..', 'images', image_name)

    def create_content(self):
        """Cria o conteúdo para a tela JoinSim."""
        # Limpa o conteúdo atual
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Cria um novo frame para o conteúdo JoinSim
        self.frame = tk.Frame(self.parent, bg=self.style.colors.primary, padx=20, pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Adiciona o título da seção
        title_label = tk.Label(self.frame, text="JoinSim Settings", bg=self.style.colors.primary, fg=self.style.colors.light,
                               font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=10)

        # Adiciona o rótulo e o campo de entrada para o número do servidor
        server_number_frame = tk.Frame(self.frame, bg=self.style.colors.primary)
        server_number_frame.pack(pady=10, fill=tk.X)

        server_number_label = tk.Label(server_number_frame, text="Server Number:",
                                       bg=self.style.colors.primary, fg=self.style.colors.light,
                                       font=('Helvetica', 14))
        server_number_label.pack(side=tk.LEFT, padx=10)

        self.server_number_var = tk.StringVar()
        server_number_entry = tk.Entry(server_number_frame, textvariable=self.server_number_var, width=20,
                                       font=('Helvetica', 14))
        server_number_entry.pack(side=tk.LEFT)

        # Adiciona o botão de ativação/desativação
        self.toggle_button = tk.Button(self.frame, text="Activate", bg="orange", fg=self.style.colors.light,
                                       font=('Helvetica', 14), command=self.toggle_active)
        self.toggle_button.pack(pady=20)

    def toggle_active(self):
        """Alterna o estado ativo/inativo da tela JoinSim e maximiza a janela do ArkAscended se ativado."""
        if self.is_active:
            self.is_active = False
            self.toggle_button.config(text="Activate", bg="orange")
            print("JoinSim is now inactive.")
        else:
            self.is_active = True
            self.toggle_button.config(text="Deactivate", bg=self.style.colors.danger)
            print("JoinSim is now active.")
            self.maximize_and_bring_to_front_ark_ascended()

    def maximize_and_bring_to_front_ark_ascended(self):
        """Maximiza a janela do ArkAscended se ela estiver aberta e a coloca em primeiro plano."""
        try:
            # Encontra a janela do ArkAscended
            windows = gw.getWindowsWithTitle('ArkAscended')
            if windows:
                ark_window = windows[0]  # Seleciona a primeira janela com o título correspondente
                self.bring_window_to_front(ark_window._hWnd)
                print("ArkAscended window maximized and brought to front.")
                # Aguarda um pouco para garantir que a janela está maximizada
                pag.sleep(2)
                # Clica no elemento Press_Start.png
                self.click_on_element(self.press_start_path)
                pag.sleep(1)  # Aguarda um segundo antes de clicar no próximo elemento
                # Clica no elemento Join_Game.png
                self.click_on_element(self.join_game_path)
                pag.sleep(1)  # Aguarda um segundo antes de clicar no próximo elemento
                # Clica no elemento Search.png e digita o número do servidor
                self.click_on_element(self.search_path)
                pag.sleep(1)  # Aguarda um segundo para garantir que o campo de pesquisa está ativo
                server_number = self.server_number_var.get()
                pag.sleep(1)
                pag.write(server_number)  # Digita o número do servidor
                print(f"Typed server number: {server_number}")
                pag.sleep(2)
                # Procura a imagem Found.png e clica abaixo dela
                self.click_below_element(self.found_path)
                pag.sleep(2)


                self.click_on_element(self.join_path)
            else:
                print("ArkAscended window not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def bring_window_to_front(self, hwnd):
        """Usa ctypes para colocar a janela com o identificador hwnd em primeiro plano."""
        try:
            ctypes.windll.user32.SetForegroundWindow(hwnd)
        except Exception as e:
            print(f"An error occurred while bringing the window to front: {e}")

    def click_on_element(self, image_path):
        """Procura o elemento na tela e clica nele."""
        try:
            # Carrega a imagem do elemento
            element_image = cv2.imread(image_path)
            if element_image is None:
                raise FileNotFoundError(f"Image file not found at {image_path}")

            # Converte a imagem para o formato que o OpenCV usa
            element_image = cv2.cvtColor(element_image, cv2.COLOR_BGR2RGB)
            element_image = np.array(element_image)

            # Tira uma captura de tela
            screenshot = pag.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

            # Encontra a posição do elemento na captura de tela
            result = cv2.matchTemplate(screenshot_np, element_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Define um limite de confiança
            threshold = 0.7
            if max_val >= threshold:
                # Calcula a posição do clique
                element_x, element_y = max_loc
                element_width, element_height = element_image.shape[1], element_image.shape[0]
                click_x = element_x + element_width // 2
                click_y = element_y + element_height // 2

                # Executa o clique na posição encontrada
                pag.click(click_x, click_y)
                print(f"Clicked on element at ({click_x}, {click_y})")
            else:
                print("Element not found in the screenshot.")
        except Exception as e:
            print(f"An error occurred while clicking on the element: {e}")

    def click_below_element(self, image_path):
        """Procura o elemento na tela e clica um pouco abaixo dele."""
        try:
            # Carrega a imagem do elemento
            element_image = cv2.imread(image_path)
            if element_image is None:
                raise FileNotFoundError(f"Image file not found at {image_path}")

            # Converte a imagem para o formato que o OpenCV usa
            element_image = cv2.cvtColor(element_image, cv2.COLOR_BGR2RGB)
            element_image = np.array(element_image)

            # Tira uma captura de tela
            screenshot = pag.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

            # Encontra a posição do elemento na captura de tela
            result = cv2.matchTemplate(screenshot_np, element_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Define um limite de confiança
            threshold = 0.8
            if max_val >= threshold:
                # Calcula a posição do clique
                element_x, element_y = max_loc
                element_width, element_height = element_image.shape[1], element_image.shape[0]
                click_x = element_x + element_width // 2
                click_y = element_y + element_height + 20  # Ajuste o valor conforme necessário para clicar abaixo

                # Executa o clique na posição encontrada
                pag.click(click_x, click_y)
                print(f"Clicked below element at ({click_x}, {click_y})")
            else:
                print("Element not found in the screenshot.")
        except Exception as e:
            print(f"An error occurred while clicking below the element: {e}")
