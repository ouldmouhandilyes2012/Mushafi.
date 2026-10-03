from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class SurahCard(BoxLayout):
    def __init__(self, surah_name, surah_number, status='unread', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (10, 10)
        self.spacing = 6
        self.size_hint_y = None
        self.height = 110
        self.border_color = self.get_status_color(status)
        self.canvas.before.clear()
        self.canvas.before.add(Color(1, 1, 1, 0.12))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))
        self.add_widget(Label(text=f"{surah_number}", halign='right', color=(0.98, 0.83, 0.37, 1), font_size='18sp', text_size=(self.width, None), valign='top'))
        self.add_widget(Label(text=surah_name, halign='right', color=(0.96, 0.96, 0.96, 1), font_size='18sp', text_size=(self.width, None), valign='middle'))
        self.add_widget(Label(text=self.status_label(status), halign='right', color=self.get_status_color(status), font_size='14sp'))

    def get_status_color(self, status):
        colors = {
            'memorized': (0.29, 0.69, 0.34, 1),
            'review': (0.89, 0.78, 0.42, 1),
            'unread': (0.86, 0.38, 0.35, 1),
            'default': (0.96, 0.96, 0.96, 1),
        }
        return colors.get(status, colors['default'])

    def status_label(self, status):
        return {'memorized': 'محفوظ', 'review': 'يحتاج مراجعة', 'unread': 'غير محفوظ'}.get(status, 'غير معروف')
