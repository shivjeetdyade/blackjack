from random import randint
import time

balance = 0
bet_amount = 0
ace = 11
reps = 0

deck = ['ace','2','3','4','5','6','7','8','9','10','k','q','j']
# deck = ['8','ace']

cards = {'ace':ace,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'k':10,'q':10,'j':10}
# cards = {'8':8,'ace':ace}

hands = {
    'dealer_hand':{
        'amount':bet_amount,
        'cards':[],
        'ace_value':ace
    },
    '1':{
        'amount':bet_amount,
        'cards':[],
        'ace_value':ace
    }
}

def bet(player_hand,x):
    hands[player_hand]['amount'] = bet_amount*x
def gets_a_card(player_hand):
    hands[player_hand]['cards'].append(deck[randint(0,len(deck)-1)])

def set_ace(ace_value):
    global ace
    ace = ace_value
    for hand in hands:
        hands[hand]['ace_value'] = ace_value
        cards['ace'] = ace_value

def cards_match(player_hand):
    return hands[player_hand]['cards'][0] == hands[player_hand]['cards'][1]

def split(player_hand):
    global balance
    new_hand = str(len(hands))
    hands[new_hand]={}
    hands[new_hand]['amount'] = bet_amount
    hands[new_hand]['cards'] = [111]
    hands[new_hand]['cards'][0] = hands[player_hand]['cards'][0]
    gets_a_card(new_hand)
    hands[new_hand]['ace_value'] = ace
    balance = balance - bet_amount
    hands[player_hand]['cards'][1] = deck[randint(0,len(deck)-1)]
def player_total(player_hand):
    total = 0
    for i in range(len(hands[player_hand]['cards'])):
        total = total + cards[hands[player_hand]['cards'][i]]

    return total

balance = int(input("enter number of coins to take:    "))

if input("want to deal?(y/n) ").lower() == 'y':
    bet_amount = int(input("enter bet amount:  "))
    bet('dealer_hand',1)
    bet('1',1)
    
    gets_a_card('dealer_hand')
    gets_a_card('dealer_hand')

    gets_a_card('1')
    gets_a_card('1')
    
    set_ace(11)

    user_total = player_total('1')
    print("dealer cards: ",hands['dealer_hand']['cards'][0],'and Hidden card',"dealer total: ",cards[hands['dealer_hand']['cards'][0]],'+ Hidden')
    print("user cards:  ",hands['1']['cards'],'user total:    ',user_total)

    if player_total('dealer_hand') == 21 and user_total == 21:

        print("You have a BlackJack. \n with cards", hands['dealer_hand']['cards'] ,"Dealer has a blackjack. \n You lose!!!")
    elif player_total('dealer_hand') == 21: 

        print("with cards", hands['dealer_hand']['cards'] ,"Dealer has a blackjack \n you lose!!!")
    elif user_total == 21: 

        print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'))
        print("You have blackjack. \n You win")
    else:
        reps = 0
        while reps<4:
            reps+=1
            for hand,hand_details in list(hands.items()):

                if not hand == 'dealer_hand' and cards_match(hand):
                    print("you've cards :",hand,":",hand_details['cards'])

                    if input("Do you want to split?(yes/no) ").lower() == 'yes':

                        split(hand)
                        print("split user cards:  ",hands[str(len(hands)-1)]['cards'],'user total:    ',player_total(str(len(hands)-1)))
                        print("split user cards:  ",hands[str(len(hands)-2)]['cards'],'user total:    ',player_total(str(len(hands)-2)))

                    else:
                        reps = 4

        for hand in hands:

            hits = 0
            if not hand == 'dealer_hand':

                if player_total(hand) == 21:

                    print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n You win')
                    balance = balance + 2*hands[hand]['amount']

                while not player_total(hand) >= 21:

                    print('player_total',player_total(hand))
                    if hits>0:
                        action = input("select one of the following option: \n \n hit \n stand \n \n ").strip().lower()
                    elif hits == 0:
                        action = input("select one of the following option: \n \n hit \n stand \n double \n \n ").strip().lower()
                    
                    if action == 'hit':

                        hits = hits + 1
                        gets_a_card(hand)
                        print('player_total',player_total(hand))
                        if player_total(hand) == 21: 

                            print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n You win')
                            balance = balance + 2*hands[hand]['amount']
                            break
                    elif action == 'double' and hits == 0:

                        bet(hand,2)
                        gets_a_card(hand)
                        print('player_total',player_total(hand))
                        set_ace(11)

                        print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'))
                        if player_total(hand) == 21:

                            print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n You win')
                            balance = balance + 2*hands[hand]['amount']
                            break
                        elif player_total(hand) > 21:

                            if 'ace' not in hands[hand]['cards'] or ('ace' in hands[hand]['cards'] and ace == 1):

                                print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n your cards:',hands[hand]['cards'],'and your total is',player_total(hand),' \n Bust \n You lose')
                                break
                            else:

                                set_ace(1)
                                if player_total(hand) == 21:

                                    print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n You win')
                                    balance = balance + 2*hands[hand]['amount']
                                    break
                                while player_total('dealer_hand') < 17:

                                    print("dealer_total",player_total('dealer_hand'))
                                    gets_a_card('dealer_hand')
                                    print("dealer_total",player_total('dealer_hand'))

                                if not player_total('dealer_hand') > 21 and not player_total(hand) > player_total('dealer_hand'): 

                                    print('You lose!!!')
                                    break
                                elif (not player_total('dealer_hand') > 21 and player_total(hand) > player_total('dealer_hand')) or (player_total('dealer_hand') > 21 and not 'ace' in hands['dealer_hand']['cards']) or (player_total('dealer_hand') > 21 and 'ace' in hands['dealer_hand']['cards'] and ace == 1):

                                    print('You won!!!')
                                    balance = balance + 2*hands[hand]['amount']
                                    break
                                elif player_total('dealer_hand') > 21 and 'ace' in hands['dealer_hand']['cards'] and ace != 1:

                                    set_ace(1)
                                    while player_total('dealer_hand') < 17:

                                        gets_a_card('dealer_hand')

                                        print("dealer_total",player_total('dealer_hand'))
                                    if not player_total('dealer_hand') > 21 and not player_total(hand) > player_total('dealer_hand'):

                                        print('player_total',player_total(hand))
                                        print('You lose!!!')
                                        break
                                    elif (not player_total('dealer_hand') > 21 and player_total(hand) > player_total('dealer_hand')) or (player_total('dealer_hand') > 21 ):

                                        print('player_total',player_total(hand))
                                        print('You won!!!')
                                        balance = balance + 2*hands[hand]['amount']
                                        break
                                    elif player_total('dealer_hand') == 21:

                                        print('You lose!!!')
                                        break
                    elif action == 'stand':
                        set_ace(11)

                        print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'))
                        while player_total('dealer_hand') < 17:

                            print("dealer_total",player_total('dealer_hand'))
                            gets_a_card('dealer_hand')
                            print("dealer_total",player_total('dealer_hand'))

                        if not player_total('dealer_hand') > 21 and not player_total(hand) > player_total('dealer_hand'): 

                            print('You lose!!!')
                            break
                        elif (not player_total('dealer_hand') > 21 and player_total(hand) > player_total('dealer_hand')) or (player_total('dealer_hand') > 21 and not 'ace' in hands['dealer_hand']['cards']) or (player_total('dealer_hand') > 21 and 'ace' in hands['dealer_hand']['cards'] and ace == 1):

                            print('You won!!!')
                            balance = balance + 2*hands[hand]['amount']
                            break
                        elif player_total('dealer_hand') > 21 and 'ace' in hands['dealer_hand']['cards'] and ace != 1:

                            set_ace(1)
                            while player_total('dealer_hand') < 17:

                                gets_a_card('dealer_hand')

                                print("dealer_total",player_total('dealer_hand'))
                            if not player_total('dealer_hand') > 21 and not player_total(hand) > player_total('dealer_hand'):
                                print('player_total',player_total(hand))
                                print('You lose!!!')
                                break
                            elif (not player_total('dealer_hand') > 21 and player_total(hand) > player_total('dealer_hand')) or (player_total('dealer_hand') > 21 ):
                                print('player_total',player_total(hand))
                                print('You won!!!')
                                balance = balance + 2*hands[hand]['amount']
                                break
                            elif player_total('dealer_hand') == 21:
                                print('You lose!!!')
                                break
#ace loop on player hand
                if player_total(hand) > 21 and not action == 'double':

                    if 'ace' not in hands[hand]['cards'] or ('ace' in hands[hand]['cards'] and ace == 1):
                        print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n your cards:',hands[hand]['cards'],'and your total is',player_total(hand),' \n Bust \n You lose')
                    else:
                        set_ace(1)
                        while not player_total(hand) >= 21:

                            action = input("select one of the following option: \n \n hit \n stand \n \n ").strip().lower()
                            if action == 'hit':

                                hits = hits + 1
                                gets_a_card(hand)
                                if player_total(hand) == 21:

                                    print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n You win')
                                    balance = balance + 2*hands[hand]['amount']
                                elif player_total(hand) > 21:

                                    print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'),'\n your cards:',hands[hand]['cards'],'and your total is',player_total(hand),' \n Bust \n You lose')
                                    break
                            elif action == 'stand':

                                set_ace(11)
                                print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'))
                                while player_total('dealer_hand') < 17:

                                    gets_a_card('dealer_hand')
                                if not player_total('dealer_hand') > 21 and not player_total(hand) > player_total('dealer_hand'):

                                    print('You lose!!!')
                                    break
                                elif (not player_total('dealer_hand') > 21 and player_total(hand) > player_total('dealer_hand')) or (player_total('dealer_hand') > 21 and not 'ace' in hands['dealer_hand']['cards']) or (player_total('dealer_hand') > 21 and 'ace' in hands['dealer_hand']['cards'] and ace == 1):

                                    print('You won!!!')
                                    balance = balance + 2*hands[hand]['amount']
                                    break
                                elif player_total('dealer_hand') > 21 and 'ace' in hands['dealer_hand']['cards'] and ace != 1:

                                    set_ace(1)
                                while player_total('dealer_hand') < 17:

                                    gets_a_card('dealer_hand')
                                if not player_total('dealer_hand') > 21 and not player_total(hand) > player_total('dealer_hand'):

                                    print('You lose!!!')
                                    break
                                elif (not player_total('dealer_hand') > 21 and player_total(hand) > player_total('dealer_hand')) or (player_total('dealer_hand') > 21 ):

                                    print('You won!!!')
                                    balance = balance + 2*hands[hand]['amount']
                                    break
else:
    print("your deposit {coins} has been saved. Thank You")


time.sleep(10)
