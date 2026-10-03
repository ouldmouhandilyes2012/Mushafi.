from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner


class RecitationScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=12)
        title = Label(text='التسميع', font_size='28sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)

        options = BoxLayout(spacing=10)
        self.surah_spinner = Spinner(text='1', values=[str(i) for i in range(1, 115)])
        self.start_spinner = Spinner(text='1', values=[str(i) for i in range(1, 115)])
        self.end_spinner = Spinner(text='10', values=[str(i) for i in range(1, 115)])
        options.add_widget(self.surah_spinner)
        options.add_widget(self.start_spinner)
        options.add_widget(self.end_spinner)
        root.add_widget(options)

        actions = BoxLayout(size_hint_y=None, height=60, spacing=10)
        record_btn = Button(text='تسجيل')
        record_btn.bind(on_release=self.record)
        actions.add_widget(record_btn)
        root.add_widget(actions)

        self.log = Label(text='جاهز للتسميع', halign='right', text_size=(self.width, None), color=(1, 1, 1, 1))
        root.add_widget(self.log)
        self.add_widget(root)

    def record(self, *_):
        surah = int(self.surah_spinner.text)
        start = int(self.start_spinner.text)
        end = int(self.end_spinner.text)
        record_id = self.app.recitation_engine.add_recitation(surah, start, end, 'تسجيل محلي')
        file_path = self.app.audio_service.record_local_audio(f"recitation_{record_id}.wav", duration_seconds=10)
        self.app.recitation_engine.add_recording(record_id, file_path, duration=10.0)
        self.log.text = f"تم تسجيل سورة {surah} من الآية {start} إلى {end} في ملف محلي."
