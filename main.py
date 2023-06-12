import requests
import json
import datetime
from headermaker import genHeader 

# response = json.loads(requests.get("http://serwis.mobilotto.pl/mapi_v6/index.php?json=getGames").text)

HEADER = genHeader()


def handler():
    res = input("Czy chcesz wyjść z progamu?\ny/n\n> ")
    if res == 'y':
        exit(1)

def getGame(gra, data):
    url = f'https://www.lotto.pl/api/lotteries/draw-results/by-date-per-game?gameType={gra}&drawDate={data}&index=1&size=1&sort=DrawSystemId&order=DESC'
    try:
        response = json.loads(requests.get(url, headers=HEADER).text)
    except:
        raise ValueError("Musisz wygenerować nowy header!")

    try:
        with open("test.json", "w") as file:
            file.write(str(response))
    except: pass

    # print(response)
    # print(type(response))

    return response["items"][0]["results"]
    # return type(url), url

def setGames():

    gryTranslate = {
        1 : "Lotto",
        2 : "LottoPlus",
        3 : "Mini"
    }

    while True:
        print("Jakie gry chcesz sprawdzić?")
        try:
            gry = [gryTranslate[int(i)] for i in input("ROZDZIEL SPACJĄ\n\n1 - Lotto\n2 - Lotto Plus\n3 - Mini\n> ").split(" ")]
            if len(gry) > 0:
                return gry
            print("WYBIERZ PRZYNAJMIEJ JEDNĄ GRĘ!!!")
        except:
            print("WYBIERZ PRZYNAJMIEJ JEDNĄ GRĘ!!!")
            handler()

def setDate():    

    def checkIfDateExists(dateString):
        y, m, d = [int(i) for i in dateString.split("-")]
        if (y == 1957 and m == 1 and d < 27) or y < 1957:
            return False
        correctDate = None
        try:
            newDate = datetime.datetime(y, m, d)
            correctDate = True
        except ValueError:
            correctDate = False
        
        return correctDate

    while True:
        print("Jaką datę losowania chcesz sprawdzić?")
        try:
            date = "-".join((str(i) if len(str(i)) >= 2 else f'0{str(i)}') for i in input("WPISZ LICZBAMI I ROZDZIEL SPACJĄ\n\nRok Miesiąc Dzień\n> ").split(" "))
            if checkIfDateExists(date):
                return date
            print("NIEPOPRAWNA DATA!!!\n(pierwsze losowanie to 1957 01 27)\n")
        except:
            print("NIEPOPRAWNA DATA!!!\n(pierwsze losowanie to 1957 01 27)\n")
            handler()


def getUserNumbers():
    
    while True:
        try:
            numbers = [int(i) for i in input("WPROWADŹ SWOJE NUMERY\n(rozdziel spacją)\n\n> ").split(" ")]
            if len(set(numbers)) == 6:
                return numbers
            print("NIEPOPRAWNE NUMERKI!!!")
        except:
            print("NIEPOPRAWNE NUMERKI!!!")
            handler()
    
    return numbers

def getLotto(game, plus: bool):
    pass

# gry = setGames()
# data = setDate()
# numbers = getUserNumbers()

# print(numbers)
# print(getGame(gry[0], data))



# print(gry, data)