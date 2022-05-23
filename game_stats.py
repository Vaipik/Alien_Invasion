class GameStats():
    # Відстежння статистики

    def __init__(self, ai_settings):
        # Ініцілізація статистики
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        # Ініціалізує статистику, що змінюється в ході гри
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1