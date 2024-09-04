import keyboard

class KeyListener:
    def __init__(self, key, callback):
        self.key = key
        self.callback = callback
        self.setup_key_listener()

    def setup_key_listener(self):
        """Configura o ouvinte de teclas para detectar o toggle de auto click mesmo com a janela minimizada."""
        keyboard.add_hotkey(self.key, self.callback)

    def update_key(self, new_key):
        """Atualiza a tecla do ouvinte e remove a configuração antiga."""
        keyboard.clear_all_hotkeys()
        self.key = new_key
        self.setup_key_listener()
