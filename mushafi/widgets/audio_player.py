from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class AudioPlayer(BoxLayout):
    def __init__(self, file_path='', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 12
        self.file_path = file_path
        self.sound = None
        self.status_label = Label(text='الصوت المحلي', halign='right', font_size='16sp')
        self.play_button = Button(text='تشغيل')
        self.play_button.bind(on_release=self.toggle_play)
        self.add_widget(self.status_label)
        self.add_widget(self.play_button)

    def toggle_play(self, *_):
        if not self.file_path:
            self.status_label.text = 'لا يوجد ملف صوتي'
            return
        if self.sound is None:
            self.sound = SoundLoader.load(self.file_path)
        if self.sound is not None:
            if self.sound.state == 'stop':
                self.sound.play()
                self.status_label.text = 'يُشغّل'
            else:
                self.sound.stop()
                self.status_label.text = 'متوقف'
