# This file handles the actual client, most of the functions here are implemented as basic GUI functionality
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from Kivy.window_analyze import WindowAnalyze
from Kivy.window_home import WindowHome
from Kivy.window_trade import WindowTrade

# imports the my.kv file we have for the configuration of the elements on each screen
kv = Builder.load_file("my.kv")
sm = ScreenManager()

# this is how we add all our screens to our GUI, In this case we only have one screen but its set up for multiple
screens = [WindowHome(name="home"), WindowAnalyze(name="analyze"), WindowTrade(name='trade')]
for screen in screens:
    sm.add_widget(screen)

sm.current = "home"


# this is how we build our GUI and run it.
class StockAndOptionsTool(App):
    def build(self):
        self.title = "Stock and Options Tool"
        return sm


if __name__ == "__main__":
    StockAndOptionsTool().run()
