from random import randint
import time
import sqlite3

blackjack_db_file = "deposits.db"

def initialize_database():
    conn = sqlite3.connect(blackjack_db_file)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_deposits (
        username TEXT PRIMARY KEY,
        deposit INTEGER
    )
    """)
    conn.commit()
    conn.close()

def get_user_deposit(username):
    conn = sqlite3.connect(blackjack_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT deposit FROM user_deposits WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def update_user_deposit(username, deposit):
    conn = sqlite3.connect(blackjack_db_file)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO user_deposits (username, deposit)
    VALUES (?, ?)
    ON CONFLICT(username) DO UPDATE SET deposit=excluded.deposit
    """, (username, deposit))
    conn.commit()
    conn.close()

def blackjack_game():
    print(""" \n\n\n       ♠   ♥   ♣   ♦   BLACKJACK   ♦   ♣   ♥   ♠ """)
    print(r"""  
      ____  _            _     _            _    
     | __ )| | __ _  ___| | __(_) __ _  ___| | __
     |  _ \| |/ _` |/ __| |/ /| |/ _` |/ __| |/ /
     | |_) | | (_| | (__|   < | | (_| | (__|   < 
     |____/|_|\__,_|\___|_|\_\|_|\__,_|\___|_|\_\

    """)

    print()
    print()
    print()

    initialize_database()
    username = input("enter your name:  ")

    deposit = get_user_deposit(username)

    one_more_round = 'yes'

    while one_more_round == 'yes':
        bet_amount = 0
        reps = 0

        deck = ['ace','2','3','4','5','6','7','8','9','10','k','q','j']
        # deck = ['ace']

        card = {'ace':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'k':10,'q':10,'j':10}
        # card = {'ace':11}

        hands = {
            'dealer_hand':{
                'cards':[],
                'double':False
            },
            '1':{
                'cards':[],
                'double':False
            }
        }

        def gets_a_card(player_hand):
            hands[player_hand]['cards'].append(deck[randint(0,len(deck)-1)])

        def set_ace(ace_value):
            card['ace'] = ace_value

        def cards_match():
            for hand in hands:
                if not hand == 'dealer_hand' and hands[hand]['cards'][0] == hands[hand]['cards'][1]:
                    return True
            return False

        def split(player_hand):
            new_hand = str(len(hands))
            hands[new_hand]={}
            hands[new_hand]['cards'] = [111]
            hands[new_hand]['cards'][0] = hands[player_hand]['cards'][0]
            hands[new_hand]['double'] = False
            gets_a_card(new_hand)
            hands[player_hand]['cards'][1] = deck[randint(0,len(deck)-1)]
            return deposit - bet_amount

        def player_total(player_hand):
            total = 0
            set_ace(11)
            for i in range(len(hands[player_hand]['cards'])):
                total = total + card[hands[player_hand]['cards'][i]]
            if total > 21:
                set_ace(1)
                total = 0
                for j in range(len(hands[player_hand]['cards'])):
                    total = total + card[hands[player_hand]['cards'][j]]
            return total

        print('Your deposit is', deposit, 'Rupees')
        deposit = deposit + float(input("enter number of coins to take: (1 coin equals 1 rupee) "))
        print('Your deposit is', deposit, 'Rupees')

        if not deposit > 0:
            one_more_round = 'no'
            break

        if input("want to deal?(y/n) ").lower() == 'y':
            bet_done = False
            while not bet_done:
                bet_amount = float(input("enter bet amount:  "))
                if bet_amount <= deposit:
                    bet_done = True
                else:
                    print("enter a valid bet_amount.")

            deposit = deposit - bet_amount
            print('Your deposit is', deposit, 'Rupees and you are playing with', bet_amount, 'coins.')

            gets_a_card('dealer_hand')
            gets_a_card('dealer_hand')

            gets_a_card('1')
            gets_a_card('1')

            user_total = player_total('1')
            print("dealer cards: ",hands['dealer_hand']['cards'][0],'and Hidden card'," , dealer total: ",card[hands['dealer_hand']['cards'][0]],'+ Hidden')
            print("your cards:  ",hands['1']['cards'],', your total:    ',user_total)

            if player_total('dealer_hand') == 21 and user_total == 21:
                print("You have a BlackJack. \n with cards", hands['dealer_hand']['cards'] ,"Dealer has a blackjack. \n You lose!!!")

            elif player_total('dealer_hand') == 21: 
                print("with cards", hands['dealer_hand']['cards'] ,"Dealer has a blackjack \n you lose!!!")

            elif user_total == 21: 
                print("dealer cards: ",hands['dealer_hand']['cards'],'dealer total: ',player_total('dealer_hand'))
                print("You have blackjack. \n You win")
                deposit = deposit + 7/3 * bet_amount

            else:
                no_of_hands = len(hands)

                while no_of_hands < 4:

                    if cards_match() and deposit - bet_amount >=0:

                        if input("Do you want to split?(yes/no) ").lower() == 'yes':
                            deposit = split(str(len(hands)-1))
                            print("you've got a new hand: ",list(hands.keys())[-1],":",hands[str(len(hands)-1)])
                            no_of_hands = len(hands)

                        else:
                            no_of_hands = 5
                            break

                    else:
                        break

                for hand in hands:
                    hits = 0

                    if not hand == 'dealer_hand':
                        print('you are playing hand no.',hand)
                        if player_total(hand) == 21:
                            continue

                        while not player_total(hand) >= 21:
                            print('your_total',player_total(hand))

                            if hits == 0 and (deposit - bet_amount) >= 0:
                                action = input("select one of the following option: \n \n hit \n stand \n double \n \n ").strip().lower()

                            else:
                                action = input("select one of the following option: \n \n hit \n stand \n \n ").strip().lower()

                            if action == 'hit':
                                hits = hits + 1
                                gets_a_card(hand)
                                print('your cards',hands[hand]['cards'] ,'Your total',player_total(hand))

                                if player_total(hand) == 21: 
                                    break

                            elif action == 'double' and hits == 0 and (deposit - bet_amount) >= 0:
                                hands[hand]['double'] = True
                                hits += 1
                                deposit = deposit - bet_amount
                                print("your deposit is",deposit)
                                gets_a_card(hand)
                                print('your cards',hands[hand]['cards'] ,'Your total',player_total(hand))

                                if player_total(hand) == 21:
                                    break

                                elif player_total(hand) > 21:
                                    break
                                break

                            elif action == 'stand':
                                break

                        if player_total(hand) > 21 and not action == 'double':
                            continue

                while player_total('dealer_hand') < 17:
                    print("dealer cards: ",hands['dealer_hand']['cards'],"dealer_total",player_total('dealer_hand'))
                    gets_a_card('dealer_hand')
                    print("dealer cards: ",hands['dealer_hand']['cards'],"dealer_total",player_total('dealer_hand'))

                for hand in hands:
                    if not hand == 'dealer_hand' and hands[hand]['double'] == True:
                        print("comparing hand",hand,":",hands[hand]['cards'],"against dealer_hand",hands['dealer_hand']['cards'])

                        if player_total(hand) == 21:
                            deposit = deposit + 4 * bet_amount
                            print("You have blackjack. \n You win")
                            continue

                        elif player_total(hand) > 21:
                            print("Bust. \n You lose!!!")
                        
                        elif player_total(hand) < 21:

                            if player_total('dealer_hand') > 21:
                                print("Dealer Bust. \n You win!!!")
                                deposit = deposit + 4 * bet_amount

                            elif player_total('dealer_hand') == 21:
                                print("dealer has a BlackJack. \n You lose!!!")

                            elif player_total('dealer_hand') > player_total(hand):
                                print("You lose!!!")

                            elif player_total('dealer_hand') < player_total(hand):
                                print("You Win!!!")
                                deposit = deposit + 4 * bet_amount

                            elif player_total('dealer_hand') == player_total(hand):
                                print("Push!!!")
                                deposit = deposit + 2 * bet_amount

                    elif not hand == 'dealer_hand' and not hands[hand]['double'] == True:
                        print("comparing hand",hand,":",hands[hand]['cards'],"against dealer_hand",hands['dealer_hand']['cards'])

                        if player_total(hand) == 21:
                            deposit = deposit + 2 * bet_amount
                            print("You have blackjack. \n You win")
                            continue

                        elif player_total(hand) > 21:
                            print("Bust. \n You lose!!!")
                        
                        elif player_total(hand) < 21:

                            if player_total('dealer_hand') > 21:
                                print("Dealer Bust. \n You win!!!")
                                deposit = deposit + 2 * bet_amount

                            elif player_total('dealer_hand') == 21:
                                print("dealer has a BlackJack. \n You lose!!!")

                            elif player_total('dealer_hand') > player_total(hand):
                                print("You lose!!!")

                            elif player_total('dealer_hand') < player_total(hand):
                                print("You Win!!!")
                                deposit = deposit + 2 * bet_amount

                            elif player_total('dealer_hand') == player_total(hand):
                                print("Push!!!")
                                deposit = deposit + bet_amount

            print('Your deposit is', deposit, 'Rupees')
            update_user_deposit(username, deposit)
            one_more_round = input("Take more coins or play_next_round?(yes/no)    ")

        else:
            print("your deposit", deposit, "has been saved. Thank You")
            one_more_round = 'no'

    time.sleep(5)

if __name__ == '__main__':
    blackjack_game()
