from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner


class QuranScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.current_surah = 1
        self.font_size = 22
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = Label(text='القرآن', font_size='28sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)

        controls = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.riwaya_spinner = Spinner(text='hafs', values=['hafs', 'warsh', 'qalun'])
        self.reader_spinner = Spinner(text='قارئ محلي', values=['قارئ محلي'])
        self.surah_spinner = Spinner(text='1', values=[str(i) for i in range(1, 115)])
        self.surah_spinner.bind(text=self.on_surah_change)
        controls.add_widget(self.riwaya_spinner)
        controls.add_widget(self.reader_spinner)
        controls.add_widget(self.surah_spinner)
        root.add_widget(controls)

        text_box = BoxLayout(orientation='vertical', padding=12, spacing=10)
        self.ayah_label = Label(text='اختر سورة', halign='right', valign='top', text_size=(self.width, None), font_size='22sp', color=(1, 1, 1, 1))
        text_box.add_widget(self.ayah_label)
        root.add_widget(text_box)

        nav = BoxLayout(size_hint_y=None, height=60, spacing=10)
        prev = Button(text='السابق')
        next_btn = Button(text='التالي')
        prev.bind(on_release=self.prev_surah)
        next_btn.bind(on_release=self.next_surah)
        nav.add_widget(prev)
        nav.add_widget(next_btn)
        root.add_widget(nav)

        actions = BoxLayout(size_hint_y=None, height=60, spacing=10)
        play = Button(text='تشغيل')
        tafsir = Button(text='التفسير')
        zoom_in = Button(text='+')
        zoom_out = Button(text='-')
        play.bind(on_release=lambda *_: None)
        tafsir.bind(on_release=lambda *_: self.manager.change_screen('tafsir'))
        zoom_in.bind(on_release=self.increase_font)
        zoom_out.bind(on_release=self.decrease_font)
        actions.add_widget(play)
        actions.add_widget(tafsir)
        actions.add_widget(zoom_out)
        actions.add_widget(zoom_in)
        root.add_widget(actions)

        self.add_widget(root)
        self.update_surah_text()

    def on_surah_change(self, instance, value):
        try:
            self.current_surah = int(value)
        except ValueError:
            self.current_surah = 1
        self.update_surah_text()

    def update_surah_text(self):
        name = self.app.quran_service.get_surah(self.current_surah)
        self.ayah_label.text = f"{name}\n\nالآية 1: {self.app.quran_service.get_surah(self.current_surah)}"
        self.ayah_label.font_size = str(self.font_size) + 'sp'

    def prev_surah(self, *_):
        self.current_surah = max(1, self.current_surah - 1)
        self.surah_spinner.text = str(self.current_surah)
        self.update_surah_text()

    def next_surah(self, *_):
        self.current_surah = min(114, self.current_surah + 1)
        self.surah_spinner.text = str(self.current_surah)
        self.update_surah_text()

    def increase_font(self, *_):
        self.font_size += 2
        self.update_surah_text()

    def decrease_font(self, *_):
        self.font_size = max(16, self.font_size - 2)
        self.update_surah_text()
