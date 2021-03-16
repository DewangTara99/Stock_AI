import datetime
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r(s, first, last):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Outputs Insider Trading Statistics with input of SEC Form 4 ticker code
def InsiderTrading(url_code):
    Data = []
    Data2 = []
    for k in range(9):
        url = "https://www.secform4.com/insider-trading/" + str(url_code) + ("-" + str(k) if k != 0 else "") + ".htm"
        page_data = requests.get(url) # requests data object
        page_data = page_data.content # string

        soup = bs(page_data, "html.parser") # soup object
        # print(soup.prettify())

        ft = soup.find("table", { "id": "filing_table" })

        # params --> date, shares traded, shares owned, total amount
        ft_data = ft.find("tbody", {})
        ft_data = ft_data.findAll("tr")

        for data_point in ft_data:
            isSale = False
            date = None
            sale = data_point.findAll("td", {"class": "S"})
            exchange_volume = data_point.findAll("td")
            if not(sale == []):
                isSale = True
                temp_date = str(sale)[15:25]
                date = temp_date
            purchase = data_point.findAll("$0")
            if not(purchase == []):
                temp_date = str(purchase)[15:25]
                date = temp_date
            obj = [
                date,
                "Sale" if isSale else "Purchase",
            ]; Data.append(obj)

            Data2.append(exchange_volume)

    # Finds average price per share and total amount traded
    Data2 = str(Data2)

    string_money = []
    counter1 = 0
    counter2 = 0
    while counter1 < len(Data2):
        if Data2[counter1] == "$":
            counter2 = counter1
            while Data2[counter2] != '<':
                if Data2[counter2] != ',':
                    string_money.append(Data2[counter2])
                counter2 += 1
            string_money.append(',')
        counter1 += 1

    Money = ''
    for i in string_money[0:]:
        if i != '$':
            Money += i

    Money = Money[0:-1]
    money = list(map(float, Money.split(',')))

    avgPrice = []
    totalAmount = []
    counter3 = 0
    while counter3 < len(money):
        if (counter3 % 2 == 0):
            avgPrice.append(money[counter3])
        else:
            totalAmount.append(money[counter3])
        counter3 += 1

    owned = []
    for j in totalAmount:
        start = str(j)[-5:-2] + "</td>, <td>"
        end = "<br/><span class=\"ownership\">"
        s = Data2
        between = find_between(s, start, end)
        rev = ""
        for i in reversed(between):
            if i == ">":
                break
            if i != ",":
                rev += i
        out = ""
        for i in reversed(rev):
            out += i
        owned.append(out)

    Output = []
    counter4 = 0
    while counter4 < len(Data):
        Row = []
        Row.append(Data[counter4][0])

        # Represents the number of shares bought or sold divided by the number of initital shares before transaction multiplied by number of shares
        if Data[counter4][1] == "Sale":
            Row.append(-1 * (float(totalAmount[counter4]) / float(avgPrice[counter4])))
        else:
            Row.append(float(totalAmount[counter4]) / float(avgPrice[counter4]))

        Output.append(Row)
        counter4 += 1
    
    Output_df = pd.DataFrame(Output, columns = ['Date', 'Weighted Exchange'])

    return Output_df
