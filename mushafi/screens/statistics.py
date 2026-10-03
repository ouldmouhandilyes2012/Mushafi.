from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class StatisticsScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=12)
        title = Label(text='الإحصائيات', font_size='28sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)

        total_surah = self.app.db.fetch_one("SELECT COUNT(*) as total FROM surah_progress WHERE status = 'memorized'")["total"]
        review_count = self.app.db.fetch_one("SELECT COUNT(*) as total FROM surah_progress WHERE status = 'review'")["total"]
        memorized_ayahs = self.app.db.fetch_one("SELECT COUNT(*) as total FROM verse_progress WHERE status = 'memorized'")["total"]
        recitations = self.app.db.fetch_one("SELECT COUNT(*) as total FROM recitations")["total"]
        errors = self.app.db.fetch_one("SELECT SUM(mistakes) as total FROM reviews")["total"] or 0

        summary = (
            f"السور المحفوظة: {total_surah}\n"
            f"السور تحتاج مراجعة: {review_count}\n"
            f"الآيات المحفوظة: {memorized_ayahs}\n"
            f"جلسات التسميع: {recitations}\n"
            f"عدد الأخطاء: {errors}\n"
            f"أيام المراجعة: {self.app.db.fetch_one('SELECT COUNT(DISTINCT date(last_review)) as total FROM reviews')['total']}\n"
        )
        label = Label(text=summary, halign='right', valign='top', text_size=(self.width, None), font_size='18sp', color=(1, 1, 1, 1))
        root.add_widget(label)
        self.add_widget(root)
