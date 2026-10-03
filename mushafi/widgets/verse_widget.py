from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class VerseWidget(BoxLayout):
    def __init__(self, surah_number, ayah_number, text, status='unread', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (12, 12)
        self.spacing = 8
        self.size_hint_y = None
        self.height = 130
        self.background_color = self.status_color(status)

        label = Label(text=f"{surah_number}:{ayah_number}", halign='right', font_size='15sp', color=(0.95, 0.82, 0.35, 1))
        text_label = Label(text=text, halign='right', font_size='18sp', text_size=(self.width, None), color=(1, 1, 1, 0.97))
        status_button = Button(text=self.status_text(status), background_color=self.status_color(status), color=(0.1, 0.1, 0.1, 1))
        self.add_widget(label)
        self.add_widget(text_label)
        self.add_widget(status_button)

    def status_color(self, status):
        return {
            'memorized': (0.23, 0.63, 0.34, 1),
            'review': (0.91, 0.76, 0.40, 1),
            'unread': (0.62, 0.49, 0.41, 1),
        }.get(status, (0.62, 0.49, 0.41, 1))

    def status_text(self, status):
        mapping = {'memorized': 'محفوظة', 'review': 'تحتاج مراجعة', 'unread': 'غير محفوظة'}
        return mapping.get(status, 'غير محفوظة')
