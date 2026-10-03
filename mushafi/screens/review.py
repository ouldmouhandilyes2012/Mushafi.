from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class ReviewScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=12)
        title = Label(text='جدول المراجعة', font_size='28sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)

        rows = self.app.review_engine.build_review_queue()
        summary = self.app.review_engine.stats()
        text = (
            f"المراجعات اليوم: {summary['due_today']}\n"
            f"المراجعات القادمة: {summary['total'] - summary['due_today']}\n"
            f"المتأخرات: {summary['delayed']}\n"
        )
        if rows:
            text += '\n'.join(
                f"سورة {row['surah']} | من {row['ayah_start']} إلى {row['ayah_end']} | موعد: {row['due_date']}"
                for row in rows[:8]
            )
        else:
            text += 'لا توجد مراجعات حالياً.'

        label = Label(text=text, halign='right', valign='top', text_size=(self.width, None), font_size='18sp', color=(1, 1, 1, 1))
        root.add_widget(label)
        self.add_widget(root)
