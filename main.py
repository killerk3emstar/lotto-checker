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

def getGame(typGry, data):
    url = f'https://www.lotto.pl/api/lotteries/draw-results/by-date-per-game?gameType={typGry}&drawDate={data}&index=1&size=1&sort=DrawSystemId&order=DESC'
    try:
        response = json.loads(requests.get(url, headers=HEADER).text)
    except:
        raise ValueError("Musisz wygenerować nowy header!")

    # print(response["items"][0]["results"][0])

    return response["items"][0]["results"][0]

def setGameType():

    gryTranslate = {
        1 : "Lotto",
        2 : "LottoPlus",
        3 : "Mini"
    }

    while True:
        print("Jaką gry chcesz sprawdzić?")
        try:
            gra = gryTranslate[int(input("1 - Lotto\n2 - Lotto Plus\n3 - Mini\n> "))]
            return gra
        except:
            print("WYBIERZ JEDNĄ GRĘ!!!")
            handler()

def setDrawDate():    

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

def getUserNumbers(NumberOfGames):
    userNumbers = []
    def getOneSet():
        while True:
            try:
                numbers = [int(i) for i in input("> ").split(" ")]
                if len(set(numbers)) == 6 and len(numbers) == 6:
                    return set(numbers)
                print("NIEPOPRAWNE NUMERKI!!!")
            except:
                print("NIEPOPRAWNE NUMERKI!!!")
                handler()

    print("WPROWADŹ SWOJE NUMERY\n(rozdziel spacją, po wprowadzeniu jednego zakładu wciśnij enter)\n")

    for _ in range(NumberOfGames):
        userNumbers.append(getOneSet())

    return userNumbers

def displayLottoAndPlusResult(userNumbers, game):
    def displayLine(userNumber, drawnNumbers):  
            hit = userNumber & set(drawnNumbers)
            for number in sorted(userNumber):
                if number in hit:
                    print('\x1b[6;30;42m' + str(number).zfill(2) + '\x1b[0m', end="  ")
                else:
                    print(str(number).zfill(2), end="  ")
            print(f'Trafienia: {len(hit)}')

    drawSystemId = game["drawSystemId"]
    drawDate = game["drawDate"][:10]
    gameType = game["gameType"]
    winningNumbers = sorted(set(game["resultsJson"]))

    print(f'Losowanie gry {gameType}, numer {str(drawSystemId)}, dnia {drawDate}')
    print("  ".join(str(i).zfill(2) for i in winningNumbers))
    print("".join("-" for _ in range(22)))

    for userNumber in userNumbers:
        displayLine(userNumber, winningNumbers)


def getNumberOfGamesToCheck():
    while True:
        try:
            howManyGames = int(input("Ile zakładów chcesz sprawdzić?\n> "))
            if howManyGames > 0:
                return howManyGames
            print("WYBIERZ CONAJMNIEJ JEDEN ZAKŁAD DO SPRAWDZENIA!\n")
        except:
            print("WYBIERZ CONAJMNIEJ JEDEN ZAKŁAD DO SPRAWDZENIA!\n")
            handler()
    
    return howManyGames


typGry = setGameType()
data = setDrawDate()
howManyGames = getNumberOfGamesToCheck()
numbers = getUserNumbers(howManyGames)
gra = getGame(typGry, data)

displayLottoAndPlusResult(numbers, gra)


