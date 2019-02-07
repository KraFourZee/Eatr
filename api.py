import myfitnesspal
import time
from datetime import datetime
from nightscout import postCarbsToNightscout 
from pushover import sendText
from configparser import ConfigParser

# reading config file
parser = ConfigParser()
parser.read('configs/config.ini')

def login(user, pw):
    client = myfitnesspal.Client(user, pw)
    return client

def getDiet(client, date):
    day = ''
    try: 
        day = client.get_date(int(date[0]), int(date[1]), int(date[2]))
    except:
        print("api error for get_date()")
    return day

# Every 10 minutes, make get request to see if any changes were made
# Make method for comparing day objects
# Check protein intake every x hours

def compareDays(oldDay, newDay):
    
    latestMealIndex = -1
    different = False
    snackAdd = False

    for i in range(len(newDay.meals)-1):
        if len(newDay.meals[i]) > 0:
            latestMealIndex = i

    #Find which meals to compare, and always pay attention to snacks
    for i in range(len(newDay.meals)-1):
        if i >= latestMealIndex:
            if len(newDay.meals[i]) > len(oldDay.meals[i]):
                different = True
    
    #Checks if new snack was added
    if len(newDay.meals[3]) > len(oldDay.meals[3]):
        snackAdd = True
        different = True

    return latestMealIndex, different, snackAdd

#Checks difference between 2 days meals at a certain meal index
def carbDiff(old_day, new_day, mealIndex):

    print('MealIndex: ' + str(mealIndex))

    oldMeal = old_day.meals[mealIndex].totals
    changedMeal = new_day.meals[mealIndex].totals
    if len(oldMeal) > 0:
        oldCarbs = oldMeal['carbohydrates']
    else:
        oldCarbs = 0
    newCarbs = changedMeal['carbohydrates']
    return newCarbs - oldCarbs

def main():

    # Myfitnesspal login
    user = parser.get('api', 'username')
    pw = parser.get('api', 'password')

    # NightScout Settings
    api_secret_hashed = parser.get('nightscout', 'api_secret_hashed')
    token = parser.get('nightscout', 'token')
    nightScoutUrl = parser.get('nightscout', 'url')

    client = login(user, pw)

    date = (str(datetime.now())).split(' ')[0].split('-')
    day = getDiet(client, date)

    old_day = day
    new_day = day

    carbsTotal = 0

    while True:

        if carbsTotal > 200:
            sendText('Eat less carbs yo')
            carbsTotal = 0

        carbsAdded = 0    
        #Wait x seconds
        time.sleep(5)

        new_day = getDiet(client, date)

        #Checks what the index of the latest meal is and if days are equivalent
        mealIndex, diff, snackAdded = compareDays(old_day, new_day)
        if diff:
            if mealIndex > -1:
                carbsAdded = carbDiff(old_day, new_day, mealIndex)

            #Add for snack
            if snackAdded:
                carbsAdded += carbDiff(old_day, new_day, 3)
        
        print('Carbs Added: ' + str(carbsAdded))
        if carbsAdded > 0:
            carbsTotal += carbsAdded
            postCarbsToNightscout(str(carbsAdded), nightScoutUrl, api_secret_hashed, token)
        old_day = new_day

main()