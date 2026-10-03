from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class HeartGrid(GridLayout):
    def __init__(self, callbacks=None, **kwargs):
        super().__init__(**kwargs)
        self.cols = 6
        self.spacing = [8, 8]
        self.padding = [12, 12]
        self.callbacks = callbacks or {}
        self.cells = []
        self.build_grid()

    def build_grid(self):
        self.clear_widgets()
        self.cells = []
        for i in range(1, 115):
            button = Button(text=str(i), font_size='18sp', background_color=(0.65, 0.52, 0.31, 1))
            button.bind(on_release=lambda instance, value=i: self.callbacks.get('on_surah_click', lambda *_: None)(value))
            self.add_widget(button)
            self.cells.append(button)

    def update_status(self, statuses):
        for idx, button in enumerate(self.cells, start=1):
            status = statuses.get(idx, 'unread')
            if status == 'memorized':
                button.background_color = (0.28, 0.72, 0.36, 1)
            elif status == 'review':
                button.background_color = (0.93, 0.74, 0.34, 1)
            else:
                button.background_color = (0.88, 0.35, 0.31, 1)
