from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner


class SettingsScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=12)
        title = Label(text='الإعدادات', font_size='28sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)

        self.riwayah_spinner = Spinner(text='hafs', values=['hafs', 'warsh', 'qalun'])
        self.font_spinner = Spinner(text='20', values=['18', '20', '24', '28'])
        self.night_spinner = Spinner(text='إيقاف', values=['إيقاف', 'تفعيل'])

        root.add_widget(self.riwayah_spinner)
        root.add_widget(self.font_spinner)
        root.add_widget(self.night_spinner)

        save = Button(text='حفظ الإعدادات')
        save.bind(on_release=self.save_settings)
        root.add_widget(save)

        delete_recordings = Button(text='حذف التسجيلات')
        delete_recordings.bind(on_release=self.delete_recordings)
        root.add_widget(delete_recordings)

        delete_data = Button(text='حذف بيانات التطبيق')
        delete_data.bind(on_release=self.delete_all_data)
        root.add_widget(delete_data)

        self.add_widget(root)

    def save_settings(self, *_):
        self.app.db.set_setting('preferred_riwayah', self.riwayah_spinner.text)
        self.app.db.set_setting('font_size', self.font_spinner.text)
        self.app.db.set_setting('night_mode', '1' if self.night_spinner.text == 'تفعيل' else '0')

    def delete_recordings(self, *_):
        for row in self.app.db.fetch_all("SELECT file_path FROM recordings"):
            path = row['file_path']
            import os
            if os.path.exists(path):
                os.remove(path)
        self.app.db.execute("DELETE FROM recordings")

    def delete_all_data(self, *_):
        self.app.db.execute("DELETE FROM reviews")
        self.app.db.execute("DELETE FROM notes")
        self.app.db.execute("DELETE FROM bookmarks")
        self.app.db.execute("DELETE FROM recitations")
        self.app.db.execute("DELETE FROM recordings")
        self.app.db.execute("DELETE FROM surah_progress")
        self.app.db.execute("DELETE FROM verse_progress")
