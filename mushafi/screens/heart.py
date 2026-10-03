from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

try:
    from ..widgets.heart_grid import HeartGrid
except ImportError:
    from widgets.heart_grid import HeartGrid


class HeartScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        title = Label(text='قلب القرآن', font_size='30sp', halign='right', color=(0.95, 0.82, 0.38, 1))
        root.add_widget(title)
        self.heart_grid = HeartGrid(callbacks={'on_surah_click': self.handle_surah_click})
        root.add_widget(self.heart_grid)
        self.add_widget(root)
        self.load_statuses()

    def handle_surah_click(self, surah_number):
        statuses = self.app.db.fetch_all("SELECT surah_id, status FROM surah_progress")
        mapping = {row['surah_id']: row['status'] for row in statuses}
        current = mapping.get(surah_number, 'unread')
        next_status = {'unread': 'review', 'review': 'memorized', 'memorized': 'unread'}[current]
        self.app.db.execute(
            "INSERT INTO surah_progress (surah_id, status, memorized, reviewed) VALUES (?, ?, 1, 1) ON CONFLICT(surah_id) DO UPDATE SET status = excluded.status, memorized = 1, reviewed = 1",
            (surah_number, next_status),
        )
        self.load_statuses()

    def load_statuses(self):
        rows = self.app.db.fetch_all("SELECT surah_id, status FROM surah_progress")
        mapping = {row['surah_id']: row['status'] for row in rows}
        for i in range(1, 115):
            mapping.setdefault(i, 'unread')
        self.heart_grid.update_status(mapping)
