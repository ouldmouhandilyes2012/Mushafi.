from pathlib import Path
import json

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class TafsirScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=12)
        title = Label(text='التفسير', font_size='28sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)

        tafsir_path = Path(self.app.base_dir) / 'assets' / 'tafsir'
        files = list(tafsir_path.glob('*.json'))
        if files:
            try:
                data = json.loads(files[0].read_text(encoding='utf-8'))
                display = data[0].get('tafsir', 'التفسير موجود محلياً.') if data else 'لا توجد بيانات تفسير.'
            except Exception:
                display = 'يُرجى استيراد ملف tafsir.json في assets/tafsir.'
        else:
            display = 'لا توجد ملفات تفسير محلية. استخدم assets/tafsir/ لإضافة ملف JSON أو SQLite.'

        label = Label(text=display, halign='right', valign='top', text_size=(self.width, None), font_size='18sp', color=(1, 1, 1, 1))
        root.add_widget(label)
        self.add_widget(root)
