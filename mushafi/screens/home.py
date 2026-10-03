from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=18)
        header = BoxLayout(size_hint_y=None, height=60)
        header.add_widget(Label(text='مصحفي', font_size='30sp', halign='right', color=(0.95, 0.82, 0.38, 1), text_size=(self.width, None)))
        root.add_widget(header)

        grid = GridLayout(cols=2, spacing=12)
        menu_items = [
            ('القرآن', 'quran'),
            ('الحفظ', 'heart'),
            ('قلب القرآن', 'heart'),
            ('المراجعة', 'review'),
            ('التسميع', 'recitation'),
            ('التفسير', 'tafsir'),
            ('العلامات', 'quran'),
            ('الملاحظات', 'profile'),
            ('الإحصائيات', 'statistics'),
            ('الملف الشخصي', 'profile'),
            ('الإعدادات', 'settings'),
        ]
        for label, screen_name in menu_items:
            btn = Button(text=label, background_color=(0.77, 0.62, 0.31, 1), color=(0.12, 0.12, 0.12, 1), font_size='18sp')
            btn.bind(on_release=lambda instance, target=screen_name: self.manager.change_screen(target))
            grid.add_widget(btn)
        root.add_widget(grid)
        self.add_widget(root)
