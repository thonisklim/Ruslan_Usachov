import
from kivy.app import App
from kivy.uix.widget import Widget


class DeckRules:
    deck = my_cards.Cards()
    # last card provides strong mast
    last_card = deck.pull_card()


class DurakGame(Widget):
    pass


class DurakApp(App):
    def build(self):
        f1 = Fl
        return DurakGame


if __name__ == '__main__':
    DurakApp.run()
