from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

try:
    from .database.database import DatabaseManager
    from .screens.heart import HeartScreen
    from .screens.home import HomeScreen
    from .screens.profile import ProfileScreen
    from .screens.quran import QuranScreen
    from .screens.recitation import RecitationScreen
    from .screens.review import ReviewScreen
    from .screens.settings import SettingsScreen
    from .screens.statistics import StatisticsScreen
    from .screens.tafsir import TafsirScreen
    from .services.audio_service import AudioService
    from .services.offline_manager import OfflineManager
    from .services.quran_service import QuranService
    from .services.recitation_engine import RecitationEngine
    from .services.review_engine import ReviewEngine
except ImportError:
    from database.database import DatabaseManager
    from screens.heart import HeartScreen
    from screens.home import HomeScreen
    from screens.profile import ProfileScreen
    from screens.quran import QuranScreen
    from screens.recitation import RecitationScreen
    from screens.review import ReviewScreen
    from screens.settings import SettingsScreen
    from screens.statistics import StatisticsScreen
    from screens.tafsir import TafsirScreen
    from services.audio_service import AudioService
    from services.offline_manager import OfflineManager
    from services.quran_service import QuranService
    from services.recitation_engine import RecitationEngine
    from services.review_engine import ReviewEngine

Window.clearcolor = (0.18, 0.12, 0.08, 1)


class ScreenManagerEx(ScreenManager):
    def change_screen(self, name):
        self.current = name


class MushafiApp(App):
    def build(self):
        self.base_dir = Path(__file__).resolve().parent
        self.db = DatabaseManager(self.base_dir / 'mushafi.db')
        self.quran_service = QuranService(self.base_dir)
        self.audio_service = AudioService(self.base_dir)
        self.review_engine = ReviewEngine(self.db)
        self.recitation_engine = RecitationEngine(self.db)
        self.offline_manager = OfflineManager(self.base_dir)

        self.manager = ScreenManagerEx()
        self.home_screen = HomeScreen(app=self)
        self.quran_screen = QuranScreen(app=self)
        self.heart_screen = HeartScreen(app=self)
        self.review_screen = ReviewScreen(app=self)
        self.recitation_screen = RecitationScreen(app=self)
        self.tafsir_screen = TafsirScreen(app=self)
        self.statistics_screen = StatisticsScreen(app=self)
        self.profile_screen = ProfileScreen(app=self)
        self.settings_screen = SettingsScreen(app=self)

        self.manager.add_widget(self.home_screen)
        self.manager.add_widget(self.quran_screen)
        self.manager.add_widget(self.heart_screen)
        self.manager.add_widget(self.review_screen)
        self.manager.add_widget(self.recitation_screen)
        self.manager.add_widget(self.tafsir_screen)
        self.manager.add_widget(self.statistics_screen)
        self.manager.add_widget(self.profile_screen)
        self.manager.add_widget(self.settings_screen)

        self.home_screen.name = 'home'
        self.quran_screen.name = 'quran'
        self.heart_screen.name = 'heart'
        self.review_screen.name = 'review'
        self.recitation_screen.name = 'recitation'
        self.tafsir_screen.name = 'tafsir'
        self.statistics_screen.name = 'statistics'
        self.profile_screen.name = 'profile'
        self.settings_screen.name = 'settings'
        self.manager.current = 'home'
        return self.manager


if __name__ == '__main__':
    MushafiApp().run()
