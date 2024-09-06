import keyboard

def on_key_event(e):
    print(f'Tecla pressionada: {e.name}')

# Captura qualquer tecla pressionada
keyboard.on_press(on_key_event)
keyboard.on_press(keyboard.press('right'))
keyboard.press('right')



# Mantém o programa rodando
keyboard.wait('esc')  # O programa terminará aoaa aaadpressionar 'esc'aa