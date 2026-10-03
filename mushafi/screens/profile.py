from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class ProfileScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=12)
        title = Label(text='الملف الشخصي', font_size='28sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)

        name = self.app.db.get_setting('user_name', 'مستخدم')
        riwayah = self.app.db.get_setting('preferred_riwayah', 'hafs')
        goal_memorization = self.app.db.get_setting('goal_memorization', '30')
        goal_review = self.app.db.get_setting('goal_review', '10')
        summary = (
            f"الاسم: {name}\n"
            f"الرواية المفضلة: {riwayah}\n"
            f"هدف الحفظ: {goal_memorization}\n"
            f"هدف المراجعة: {goal_review}"
        )
        label = Label(text=summary, halign='right', valign='top', text_size=(self.width, None), font_size='18sp', color=(1, 1, 1, 1))
        root.add_widget(label)
        self.add_widget(root)
