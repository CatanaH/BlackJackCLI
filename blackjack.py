import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    def __str__(self):
        deck_contents = ""
        for card in self.deck:
            deck_contents += '\n' + card.__str__()
        return "The deck contains: " + deck_contents
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1
    def adj_for_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total):
        self.total = total
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -=self.bet

def take_bet(chips):
    while True:
        try:
            bet = input("How much would you like to bet? ")
            chips.bet = int(bet)
        except:  # fix to cleaner error handling with types
            try:
                if bet[0].lower() == 'q':
                    pass  # code to quit whole program
            except:
                print('Sorry, Please provide a number')
        else:  # this runs if try reuns w/out exception
            if chips.bet > chips.total:
                print('Sorry, But you do not have enough chips! You currently have {} dollars'.format(chips.total))
            else:
                break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adj_for_aces()

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input('Hit or Stand, please enter H or S ')
        if x[0].lower() == 'h':
            hit(deck,hand)
            show_some(player_hand,dealer_hand)
        elif x[0].lower() == 's':
            print("Player Stands, Dealer's turn")
            playing = False
        elif x[0].lower() == 'q':
            pass  # code for quit program
        else:
            print('Invalid entry, please enter H for Hit or S for stand')
            continue
        break

def show_some(player,dealer):
    print("\n------------------\nDealer's Hand: ")
    print('**Card face down**')
    print(dealer.cards[1])
    print("\nPlayer's Hand:")
    for card in player.cards:
        print(card)
    print("Player's Total= ",player.value)


def show_all(player,dealer):
    print("\n-------------------\nDealer's Hand: ")
    for card in dealer.cards:
        print(card)
    print("Dealer's Total= ",dealer.value)
    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)
    print("Player's Total= ",player.value)

def player_wins(player, dealer, chips):
    #player starts with 21 or hits and dealer doesnt beat count, player gets chips
    print('player wins')
    chips.win_bet()

def player_busts(player, dealer, chips):
    #player hits and goes over 21, dealer gets chips
    print('Bust!')
    chips.lose_bet()

def dealer_wins(player, dealer, chips):
    print('Dealer wins!')
    chips.lose_bet()

def dealer_busts(player, dealer, chips):
    print('Dealer Busts! Player Wins!')
    chips.win_bet()

def push(player, dealer):
    print('Dealer and Player tie! Game is a PUSH')

"""
Start of game
"""
pot_total = 100
player_chips = Chips(pot_total)
while True:
    print(('\n' * 50) + 'Welcome to Black-Jack!')
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    print(f'Your total chips are: {player_chips.total}')
    take_bet(player_chips)

    show_some(player_hand,dealer_hand)

    if player_hand.value == 21:
        print("BLACKJACK!")
        playing = False

    while playing:
        hit_or_stand(deck,player_hand)
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        show_all(player_hand,dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)

    print('\nYour total chips are at: {}'.format(player_chips.total))
    new_game = input('Would you like to play another hand? y/n')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing, Good Bye!' + ('\n' * 25))
        break


# add automatic win if dealt blackjack  #done,need to test tho
# add quit anywhere in gameplay
# add timer to play cards slow
