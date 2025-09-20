import requests
from bs4 import BeautifulSoup
import os
import sys
from datetime import datetime
from decouple import config


def website_data():

    website_url = "https://www.tgju.org/"
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup


def clear():
    
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")

    return "\nScreen cleared."


def get_digit_input():

    while True:
        choice = input("Enter the option number to continue: ").strip()

        exit_chars = ['q','Q','exit','Exit']
        clear_chars = ['c','clear','cls','Clear']
        help_chars = ['?','h','help','Help']
        
        special_keys = {
            **{ch: 0 for ch in exit_chars},
            **{ch: -1 for ch in clear_chars},
            **{ch: -2 for ch in help_chars},
            "":"",
        }

        if choice.isdigit():
            choice = int(choice)
            break

        elif choice in special_keys:
            choice = special_keys[choice]
            break

        else:
            print("\nInvalid! Please enter the option number only.\n" \
            "> Enter '?'|'h'|'help' to see the manual.\n")

    return choice


def help():

    output = "\nHow to use this CLI Tool:\n\n" \
            "> Run the options with their numbers.\n" \
            "> Press 'Enter' to repeat your previous choice.\n" \
            "> Enter 'c'|'clear'|'cls' to Clear.\n" \
            "> Enter 'q'|'exit' to Exit."

    return output


def send_to_bot(msg):

    token = config('token')

    updates = requests.get(f"https://api.telegram.org/bot{token}/getUpdates").json()
    
    chat_ids = set()
    for update in updates['result']:
        try:
            chat_id = update['message']['from']['id']
            chat_ids.add(chat_id)
        except:
            continue
    
    for chat_id in chat_ids:
        post_url = (f"https://api.telegram.org/bot{token}/SendMessage?cha*t_id={chat_id}&text=" + str(msg))

        payload = {"UrlBox": post_url,
                    "AgentList":"Mozilla Firefox",
                    "VersionList":"HTTP/1.1",
                    "MethodList":"POST"
        }

        req = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx", data=payload)

        print(req)

    return "Successfully sent to bot."


def carat_convertor():

    current_gold_weight = float(input("Enter the gold weight in gr: "))
    current_gold_carat = float(input("Enter the current gold carat(0-24K or 0-1000 PerMille): "))
    target_gold_carat = float(input("Enter the target gold carat(0-24 or 0-1000): "))

    try:
        target_gold_weight = ((current_gold_carat / target_gold_carat) * current_gold_weight)
        return "\n"+f"The target will be {target_gold_weight:.3f}gr, {target_gold_carat} Gold."
    except:
        print("\nTarget gold carat cannot be zero!\nTry again!\n")
        return carat_convertor()


def hobab_seke():

    soup = website_data()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    sekee_tr = soup.find("tr", {"data-market-nameslug":"sekee"})
    sekee_price = sekee_tr.get("data-price")
    sekee_price = int(sekee_price.replace(",", ""))

    gold18_tr = soup.find("tr", {"data-market-nameslug":"geram18"})
    gold18_price = gold18_tr.get("data-price")
    gold18_price = int(gold18_price.replace(",", ""))

    hobab = (sekee_price / gold18_price)

    if hobab < 11.8:
        hobab_status = "*** Hobab kam. Seke bekhar! ***"
    elif 11.8 <= hobab <= 12.3:
        hobab_status = "*** Taadol. Sabr kon! ***"
    elif 12.3 < hobab:
        hobab_status = "*** Hobab ziad. AbShode bekhar! ***"

    shakhese_hobab = f"Shakhese Hobab  ~>  {hobab:.3f}"
    sekee_p = f"Seke Emami Price  ~>  {sekee_price:_} R"
    gold18_p = f"Gold18 Price  ~>  {gold18_price:_} R"

    output = str(today) + "\n\n" + hobab_status + "\n" + shakhese_hobab + "\n" + sekee_p + "\n" + gold18_p
    
    print(send_to_bot(output)+"\n")
    
    return output


def hobab_gold():

    soup = website_data()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    dollar_tr = soup.find("tr", {"data-market-nameslug":"price_dollar_rl"})
    dollar_price = dollar_tr.get("data-price")
    dollar_price = int(dollar_price.replace(",", ""))
    
    ounce_jahan_tr = soup.find("tr", {"data-market-nameslug":"ons"})
    ounce_jahan_price = ounce_jahan_tr.get("data-price")
    ounce_jahan_price = float(ounce_jahan_price.replace(",", ""))

    mesgal_iran_tr = soup.find("tr", {"data-market-nameslug":"mesghal"})
    mesgal_iran_price = mesgal_iran_tr.get("data-price")
    mesgal_iran_price = int(mesgal_iran_price.replace(",", ""))

    mesgal_jahan_price = ((ounce_jahan_price * dollar_price) / 9.5742)

    hobab = (mesgal_iran_price - mesgal_jahan_price)

    if hobab < 1_000_000:
        hobab_status = "*** Hobab kam. Tala bekhar! ***"
    elif 1_000_000 <= hobab <= 5_000_000:
        hobab_status = "*** Taadol. Sabr kon! ***"
    elif 5_000_000 < hobab:
        hobab_status = "*** Hobab ziad. Tala befroosh! ***"

    shakhese_hobab = f"Shakhese Hobab  ~>  {int(hobab):_}"
    mesgal_iran = f"Mesgal Iran Price  ~>  {mesgal_iran_price:_} R"
    mesgal_jahan = f"Mesgal Jahan Price  ~>  {int(mesgal_jahan_price):_} R"

    output = str(today) + "\n\n" + hobab_status + "\n" + shakhese_hobab + "\n" + mesgal_iran + "\n" + mesgal_jahan

    print(send_to_bot(output)+"\n")

    return output


def buy_calc():
    
    soup = website_data()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    mesgal_iran_tr = soup.find("tr", {"data-market-nameslug":"mesghal"})
    mesgal_iran_price = mesgal_iran_tr.get("data-price")
    mesgal_iran_price = int(mesgal_iran_price.replace(",", ""))

    geram18_price = ((mesgal_iran_price / 4.608) * (750/705))

    gold_weight = float(input("Enter the weight of gold you want to buy: "))
    ojrat = float(input("Enter the Ojrat persentage: "))
    sud = float(input("Enter the Sud persentage: "))

    total_price_per_gr = ((geram18_price * (1 + (ojrat/100))) * (1 + (sud/100)))
    tax = ((geram18_price * (ojrat/100)) + ((geram18_price * (1 + (ojrat/100))) * (sud/100))) * 0.1
    total_price = (total_price_per_gr * gold_weight) + tax

    total = f"The gold price is {int(total_price):_} R for buy."
    geram18 = f"Geram18 price is {int(geram18_price):_} R right now."
    total_price_per_gr_t = f"Geram18 per gr price is {int(total_price_per_gr):_} R for the gold."
    tax_t = f"Tax is {int(tax):_} R for the gold."

    output = "\n" + str(today) + "\n\n" + total + "\n" + geram18 + "\n" + total_price_per_gr_t + "\n" + tax_t

    return output


def sell_calc():
    
    soup = website_data()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    mesgal_iran_tr = soup.find("tr", {"data-market-nameslug":"mesghal"})
    mesgal_iran_price = mesgal_iran_tr.get("data-price")
    mesgal_iran_price = int(mesgal_iran_price.replace(",", ""))

    geram18_price = ((mesgal_iran_price / 4.608) * (750/705))

    gold_weight = float(input("Enter the weight of gold you want to sell: "))
    
    total_price = (gold_weight * (740/750)) * geram18_price

    total = f"Your gold price is {int(total_price):_} R for sell."
    geram18 = f"Geram18 price is {int(geram18_price):_} R right now."

    output = "\n" + str(today) + "\n\n" + total + "\n" + geram18

    return output


def main():

    last_choice = None

    while True:
        options = {
            "Hobabe Seke": hobab_seke,
            "Hobabe Iran/Jahan": hobab_gold,
            "Gold Buy calculator": buy_calc,
            "Gold Sell calculator": sell_calc,
            "Carat Convertor": carat_convertor,
            "Help": help,
            "Clear": clear,
            "Exit": lambda: sys.exit(0),
            }
        
        print("\n"+"="*25+"\n")
        for num, op in enumerate(options.keys()):
            print(num+1, op)
        print("\n"+"="*25+"\n")

        choice = get_digit_input()

        print()
        if choice == "":
            if last_choice is None:
                clear()
                print("\nNo previous choice yet.\n" \
                      "> Enter '?'|'h'|'help' to see the manual.")
                continue
            choice = last_choice
        else:
            last_choice = choice

        func = list(options.values())[choice-1]
        print(func())




if __name__ == "__main__":
    main()
