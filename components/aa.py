import pyautogui
import time

print("Clique no canto superior esquerdo da área que deseja capturar. Aguarde 5 segundos...")
time.sleep(5)

# Captura as coordenadas do canto superior esquerdo
left, top = pyautogui.position()
print(f"Canto superior esquerdo capturado: Left={left}, Top={top}")

time.sleep(2)
print("Agora clique no canto inferior direito da área que deseja capturar. Aguarde 5 segundos...")
time.sleep(5)

# Captura as coordenadas do canto inferior direito
right, bottom = pyautogui.position()
print(f"Canto inferior direito capturado: Right={right}, Bottom={bottom}")

# Calcula largura e altura
width = right - left
height = bottom - top

print(f"Dimensões da área: Width={width}, Height={height}")
print(f"Coordenadas finais para captura: Left={left}, Top={top}, Width={width}, Height={height}")
