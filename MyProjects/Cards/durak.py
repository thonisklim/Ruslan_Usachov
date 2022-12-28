import random


def get_mast(card_number):
    mast = ""
    temp_mast = card_number % 4
    match temp_mast:
        case 0:
            mast = " ♥"
        case 1:
            mast = " ♦"
        case 2:
            mast = " ♣"
        case 3:
            mast = " ♠"
    return mast


def get_val(card_num):
    name = ""
    value = card_num // 4
    match value:
        case 0:
            name = "6"
        case 1:
            name = "7"
        case 2:
            name = "8"
        case 3:
            name = "9"
        case 4:
            name = "10"
        case 5:
            name = "Valet"
        case 6:
            name = "Dama"
        case 7:
            name = "King"
        case 8:
            name = "A"
    return name


def what_card(i):
    # print(i, i // 4, i % 4)
    return get_val(i) + get_mast(i)


class Cards:
    def __init__(self):
        self.cards_arr = []
        # filling arr
        for i in range(36):
            self.cards_arr.append(i)

    def pull_card(self):
        a = random.choice(self.cards_arr)
        self.cards_arr.remove(a)
        return a

    # in num u write needed amount of cards, in durak it`s 6
    # overloading func give_cards
    def give_cards(self, num, player_deck=None):
        if player_deck is None:
            player_deck = []
        else:
            num = num - len(player_deck)
        for i in range(num):
            player_deck.append(self.pull_card())
        return player_deck

    def get_arr(self):
        return self.cards_arr


class Players(Cards):
    player_deck = []

    def __init__(self):
        super().__init__()
        self.deck = Cards()
        self.players_arr = []

    def players_init(self, num):
        for i in range(num):
            player = Players()
            player.player_deck = self.deck.give_cards(6)
            self.players_arr.append(player)

    def give_deck(self):
        return self.player_deck

    def my_deck(self):
        named_deck = []
        for i in self.player_deck:
            named_deck.append(what_card(i))
        return named_deck

    def show_decks(self):
        for player in self.players_arr:
            print(player.my_deck())


obj = Players()
obj.players_init(4)
obj.show_decks()
# print(obj.players_arr[0].my_deck())
