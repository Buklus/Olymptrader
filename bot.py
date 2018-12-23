from pyvirtualdisplay import Display
from selenium import webdriver
import time, sys, pickle
from selenium.webdriver.common.keys import Keys

import telegram, requests, json, sys

telegram_token = "754942247:AAG8gXODpV5nG6LOUApghhgWlxABJK9fUIc"

kingsley_telegram_id = "553991636"
bukunmi_telegram_id = "652658806"

efosa_telegram_id = "465774397"

def send_telegram_message(user_id, message):
    api_url = "https://api.telegram.org/bot{}/".format("754942247:AAG8gXODpV5nG6LOUApghhgWlxABJK9fUIc")
    
    params = {'chat_id': user_id, 'text': message}
    method = 'sendMessage'
    
    resp = requests.post(api_url + method, params)
    
    return resp

def send_telegram_image(user_id,image_path):
    bot = telegram.Bot(token="754942247:AAG8gXODpV5nG6LOUApghhgWlxABJK9fUIc")
    bot.send_photo(chat_id = user_id, photo=open(image_path, 'rb'))
    return "sent"

def send_to_telegram_db(message):
    api_url = "https://api.telegram.org/bot{}/".format("787287032:AAH2uULgRGdB0QCAbxnUfcJnSyyuReDFxqU")
    
    params = {'chat_id': kingsley_telegram_id, 'text': message}
    method = 'sendMessage'
    
    resp = requests.post(api_url + method, params)
    
    return resp

display = Display(visible=0, size=(1928, 1060))
display.start()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)


url = 'http://christopher.su'
url = 'https://olymptrade.com/platform'


driver.get(url)

def login_function(driver, account_mail, account_password):
    email_input = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div/form/div[2]/input')
    password_input = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div/form/div[3]/input')

    email_input.send_keys(account_mail)
    password_input.send_keys(account_password)

    login_btn = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div/div/div/div[2]/div/form/div[5]/button')
    login_btn.click()

account_mail = "koning369@gmail.com"
account_password = "gabriel2009"

def get_balance_info(driver):
    balance_info = driver.find_element_by_xpath('//*[@id="header"]/div/div[3]/div[1]/button')
    
    #balance_info.text format: 'Demo account\n10 000.00 a\n '
    
    account_type = balance_info.text.split("\n")[0]
    
    account_balance = balance_info.text.split("\n")[1]
    account_balance = float( "".join(i for i in account_balance.split()[:2]) ) #Remove the last letter(possibly representing currency).
    
    return account_type, account_balance

def set_timeframe(driver, num_minutes='1'):
    num = driver.find_element_by_css_selector(".timeinput__input.timeinput__input_minutes")    

    #Setting num to 1:
    num.send_keys(Keys.CONTROL,'a')
    num.send_keys(Keys.DELETE)
    num.send_keys('1')
    
    #Set value for timeframe to min:
    #timeframe = driver.find_element_by_xpath('//*[@id="opcion"]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div[1]/span/span[2]/span/span')
    #driver.execute_script('arguments[0].innerHTML = "min";', timeframe)

def set_deal_amount(driver, value='1'):
    value = str(value)#Input control. Must be in string not int or float.
    if float(value) < 1:
        raise Exception("Deal amount cannot be less than 1")
    
    deal_amount = driver.find_element_by_class_name('input-currency__input')
    #Set deal amount:
    deal_amount.send_keys(Keys.CONTROL,'a')
    deal_amount.send_keys(Keys.DELETE)
    deal_amount.send_keys(value)

def click_green_or_red(to_click="green"):
    green_btn= driver.find_element_by_css_selector(".deal-buttons__button.deal-buttons__button_up")
    red_btn = driver.find_element_by_css_selector(".deal-buttons__button.deal-buttons__button_down")
    
    if to_click == "green":
        green_btn.click()
    elif to_click == "red":
        red_btn.click()
    else:
        raise Exception("Invalid argument entered for button colour to be clicked.")


#time.strftime('%X %x %Z') #https://docs.python.org/3/library/time.html
#Check if time is 06:00 or above.
#Note that strftime returns your current time - 1.
def time_reached( to_check="06:00" ):
    #strftime format: '05:04:53 12/14/18 UTC'
    struct_time = time.strftime('%X %x %Z')
    hour = struct_time.split()[0].split(":")[0]
    minute = struct_time.split()[0].split(":")[1]
    
    #If passed time(hour):
    if hour > to_check.split(":")[0]:
        return True
    
    #Check if passed/reached time(minute):
    elif hour == to_check.split(":")[0]:
        if minute >= to_check.split(":")[1]:
            return True
        else:
            return False
    
    else:
        return False

#Disadvantage of using xpath cos of screen size. [don't use it blindly.]
def get_rate():
    #btn = driver.find_element_by_xpath('//*[@id="pair-managing-add-btn"]/span[2]')
    btn = driver.find_element_by_xpath('//*[@id="pm-v1-XRPUSD"]/div[1]/span[2]')
    rate = float( btn.text.replace("%", "") )
    return rate


# URL to restdb.io database
dburl = 'https://olymptrader-f3e7.restdb.io/rest/trades'

# public api key
headers = {'x-apikey': 'affda68cd42728a147ab4fad19f4260ec3b94', 'Content-Type': 'application/json'}
params = {'sort': 'title'}

# [rate_of_return, float(amount_to_deal), "-", trade_time, get_colour]
def post_data(lst):
    payload = { "rate": lst[0], "stake": lst[1], "won_or_lost": lst[2], "trade_time": lst[3], "trade_direction": lst[4],
              "account_balance": lst[5], "current_day": lst[6] }

    # POST data
    r = requests.post(dburl, headers = headers, data = json.dumps(payload))
    print("Restdb post", r)


#This is the code for the second table at 82%
losses = []
shot_num = 0

opposite_dict = { "green":"red", "red":"green" }#To switch trade deals placed.
colour = "red"

session_profit = 0
streak = []
for_database = []

current_day = time.strftime('%Y-%m-%d')
def run_bot( deadline="06:00" ):
    global losses, shot_num, account_type, account_balance, opposite_dict, colour, session_profit, total_loss, streak, for_database, driver
    #Check balance and account type:
    account_type, account_balance = get_balance_info(driver)
    print("Account type:", account_type, account_balance)
    
    session_starting_balance = account_balance #To track profit at begining and end of trade.

    def place_trade():
        global losses, shot_num, account_type, account_balance, opposite_dict, colour, total_loss, session_profit, streak, for_database
        if len(losses) == 0: amount_to_deal = '1'
        elif len(losses) == 1: amount_to_deal = '2.5'
        elif len(losses) == 2: amount_to_deal = '5.65'
        elif len(losses) == 3: amount_to_deal = '12.69'
        elif len(losses) == 4: amount_to_deal = '28.55'
        elif len(losses) == 5: amount_to_deal = '65.5'
        elif len(losses) == 6: amount_to_deal = '160'
        elif len(losses) == 7: amount_to_deal = '365'
        elif len(losses) == 8: amount_to_deal = '850'
        elif len(losses) == 9: amount_to_deal = '2000'
        #elif len(losses) == 10: amount_to_deal = '2945'
        #elif len(losses) == 11: amount_to_deal = '5000'
        
        
        #Making sure deal_amount is correct.
        set_timeframe( driver, num_minutes='1' )
        set_deal_amount( driver, value=amount_to_deal )
        
        get_colour = opposite_dict[colour]
        rate_of_return = get_rate()#Get current rate to click.
        click_green_or_red( to_click=get_colour )
        colour = get_colour #To switch colour.
                
        trade_time = time.strftime('%X')
        nigerian_time = str( int(trade_time.split(":")[0]) +1) + ":" + ":".join(i for i in trade_time.split(":")[1:])
        trade_time = nigerian_time #Converting to Nigerian current time. [1 hour +]
        print("Current time:", trade_time)
        
        bot_text = "Amount Staked *{}*:".format(get_colour) + " " + amount_to_deal
        print(bot_text)
        
        #Take Snapshot:
        driver.save_screenshot("shot{}.png".format(shot_num))
        shot_num += 1

        #Wait for 62 to check if trade is successful:
        time.sleep(62)
        
        last_time = time.time()
        
        #Save screenshot after 90 seconds to send later below:
        #driver.save_screenshot("shot{}.png".format(shot_num))
        
        #Check balance:
        old_balance = account_balance

        account_type, account_balance = get_balance_info(driver)
        print("\nNew Balance:", account_balance)
                
        up_arrow, down_arrow = u'\u2191', u'\u2193'
        good_check, x_check = u'\u2714', u'\u2718'
        
        if get_colour == "green": arrow = up_arrow
        elif get_colour == "red": arrow = down_arrow
        
        '{} For trade of ${} at {} {}'.format(x_check, amount_to_deal, trade_time, down_arrow)
        if account_balance > old_balance:
            print("Won Trade!")
            losses = []
            session_profit += account_balance - old_balance
            
            bot_message = '{} For trade of ${} at {} {}'.format(good_check, amount_to_deal, trade_time, arrow)
            send_telegram_message(kingsley_telegram_id, bot_message)
            # send_telegram_message(efosa_telegram_id, bot_message)
            # send_telegram_message( bukunmi_telegram_id, bot_message )
            streak.append("w")
    
            lst = [rate_of_return, float(amount_to_deal), "w", trade_time, get_colour, account_balance, current_day]
            for_database.append(lst)
            #Post data to restdb:
            # post_data(lst)
            
        elif account_balance < old_balance:
            print("Loss Trade")
            losses.append(rate_of_return)#Append rates.
            
            bot_message = '{} For trade of ${} at {} {}'.format(x_check, amount_to_deal, trade_time, arrow)
            send_telegram_message(kingsley_telegram_id, bot_message)
            # send_telegram_message(efosa_telegram_id, bot_message)
            # send_telegram_message( bukunmi_telegram_id, bot_message )
            streak.append("l")
    
            lst = [rate_of_return, float(amount_to_deal), "l", trade_time, get_colour, account_balance, current_day]
            for_database.append(lst)
            #Post data to restdb:
            # post_data(lst)
            
        elif account_balance == old_balance:
            #ignore and continue if account balance is still same for whatever reason after trade.
            print("Account balance remained same after thread. Situation Ignored!")
            
            bot_message = '{} For trade of ${} at {} {}'.format('--', amount_to_deal, trade_time, arrow)
            send_telegram_message(kingsley_telegram_id, bot_message)
            # send_telegram_message(efosa_telegram_id, bot_message)
            # send_telegram_message( bukunmi_telegram_id, bot_message )
            streak.append("-")
    
            lst = [rate_of_return, float(amount_to_deal), "-", trade_time, get_colour, account_balance, current_day]
            for_database.append(lst)
            #Post data to restdb:
            # post_data(lst)
            
        
        #Check if losses is up to 5:
        if len(losses) >= 5:
            print( "Number of losses at a stretch so far is:", len(losses) )
        
        if len(losses) > 10:
            bot_message = "There has been losses made for over 10 trades.\nBot has been stopped.\nAccount balance: ${}".format(account_balance)
            send_telegram_message( kingsley_telegram_id, bot_message )
            # send_telegram_message(efosa_telegram_id, bot_message)
            # send_telegram_message( bukunmi_telegram_id, bot_message )
            driver.quit()
            
        print("Number of losses so far:", len(losses))
        #Wait for another 56 seconds before next trade: In hopes that it sums up to exactly 10 seconds.
        time.sleep( 59- (time.time() - last_time) )
    
    #Convert deadline to true value for Nigerian time (1 hour +).
    nigerian_deadline = str( int(deadline.split(":")[0]) + 1 ) + ":" + deadline.split(":")[1]
    
    bot_start_time = time.strftime('%X')
    to_nigerian_time = str( int(bot_start_time.split(":")[0]) +1) + ":" + bot_start_time.split(":")[1]
    bot_start_time = to_nigerian_time #Converting to Nigerian current time. [1 hour +]
    
    bot_message = "Ripple currency Trade session has started with Google Compute Engine.\n From {} till {}".format(bot_start_time, nigerian_deadline)
    send_telegram_message( kingsley_telegram_id, bot_message )
    # send_telegram_message(efosa_telegram_id, bot_message)
    # send_telegram_message( bukunmi_telegram_id, bot_message )
    
    bot_message = "Account balance at start of session: ${}".format(session_starting_balance)
    send_telegram_message( kingsley_telegram_id, bot_message)
    # send_telegram_message(efosa_telegram_id, bot_message)
    # send_telegram_message( bukunmi_telegram_id, bot_message )
    
    #While time has not been reached or passed:
    try:
        while not time_reached( to_check=deadline ):
            place_trade()
            print()
        else:
            print("Trade deadline exceeded!")
            bot_message = "Trade deadline of {} exceeded!".format(nigerian_deadline)
            send_telegram_message( kingsley_telegram_id, bot_message)
            # send_telegram_message(efosa_telegram_id, bot_message)
            # send_telegram_message( bukunmi_telegram_id, bot_message )

            #Keep placing trades until all losses are cleared:
            if len(losses) != 0:
                while len(losses) != 0:
                    place_trade()
                    print()
            
            if len(losses) == 0:
                print("Trading session has ended.")
                session_ending_balance = account_balance
                
                bot_message = "Trading session has ended."
                send_telegram_message( kingsley_telegram_id, bot_message)
                # send_telegram_message(efosa_telegram_id, bot_message)
                # send_telegram_message( bukunmi_telegram_id, bot_message )
                
                send_telegram_message(kingsley_telegram_id, "Account balance at end of session: ${}".format(session_ending_balance) )
                # send_telegram_message(efosa_telegram_id, "Account balance at end of session: ${}".format(session_ending_balance) )
                # send_telegram_message(bukunmi_telegram_id, "Account balance at end of session: ${}".format(session_ending_balance) )
                
                bot_message = "Total profit made at end of session is: ${}".format(round(session_ending_balance - session_starting_balance,2))
                print(bot_message)
                send_telegram_message( kingsley_telegram_id, bot_message )
                # send_telegram_message(efosa_telegram_id, bot_message)
                # send_telegram_message( bukunmi_telegram_id, bot_text )

                print("Streaks:", streak)
    except Exception as e:
        #Save the driver.
        driver = driver
        print(e)
        print("Program stoppped.")
        send_telegram_message( kingsley_telegram_id, str(e) )
        # send_telegram_message( bukunmi_telegram_id, "Program stoppped by admin." )
    
    return for_database


login_function(driver, account_mail, account_password)

try:
    driver.save_screenshot("out.png")
except Exception as e:
    send_telegram_message( kingsley_telegram_id, str(e) )
    send_telegram_message( kingsley_telegram_id, "Refreshing the page to try again." )
    
    driver.refresh()
    try:
        driver.save_screenshot("out.png")
    except Exception as e:
        send_telegram_message( kingsley_telegram_id, str(e) )
        send_telegram_message( kingsley_telegram_id, "Can't go further." )
        driver.quit()
        sys.exit()

#time.strftime('%X %x %Z')
#Start when time is 6:19am meaning 5:19am

while True:
    #Remember time(hour -1). 06:00:00 instead of 07:00:00
    if time.strftime("%X") > '04:35:00':
        #Remember time(hour -1). 18:00 instead of 19:00
        database = run_bot( deadline="04:51" )
        break

driver.quit()
display.stop()
sys.exit()

# import pandas as pd
# df = pd.DataFrame(b)
# writer = pd.ExcelWriter("output.xlsx")
# df.to_excel(writer, "Sheet1")
# writer.save()
# print(" Done. ")

