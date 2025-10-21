#BusSchedule.py 
#Name: Blake Green
#Date: 10/15/25
#Assignment: Bus Schedule Homework

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def getHours(timeStr):
    timeStr = timeStr.replace("AM", " AM").replace("PM", " PM")  # <-- fix added
    parts = timeStr.split()
    hm = parts[0].split(":")
    hour = int(hm[0])
    ampm = parts[1]
    if ampm == "PM" and hour != 12:
        hour += 12
    if ampm == "AM" and hour == 12:
        hour = 0
    return hour

def getMinutes(timeStr):
    timeStr = timeStr.replace("AM", " AM").replace("PM", " PM")  # <-- fix added
    parts = timeStr.split()
    hm = parts[0].split(":")
    return int(hm[1])

def isLater(timeStr1, timeStr2):
    h1 = getHours(timeStr1)
    m1 = getMinutes(timeStr1)
    h2 = getHours(timeStr2)
    m2 = getMinutes(timeStr2)
    if h1 > h2:
        return True
    elif h1 == h2 and m1 > m2:
        return True
    else:
        return False

def getBusTimes(pageText):
    lines = pageText.split("\n")
    busTimes = []
    for line in lines:
        line = line.strip()
        if ":" in line and ("AM" in line or "PM" in line):
            busTimes.append(line)
    return busTimes

def minutesUntil(busTime, currentTime):
    busHour = getHours(busTime)
    busMin = getMinutes(busTime)
    curHour = currentTime.hour
    curMin = currentTime.minute
    totalBus = busHour * 60 + busMin
    totalCur = curHour * 60 + curMin
    return totalBus - totalCur

def main():
  url = "https://myride.ometro.com/Schedule?stopCode=2269&routeNumber=11&directionName=EAST"
  #c1 = loadURL(url) #loads the web page
  c1 = loadTestPage() #loads the test page

  busTimes = getBusTimes(c1)

  nowGMT = datetime.datetime.utcnow()
  nowCentral = nowGMT - datetime.timedelta(hours=5)
  currentTimeStr = nowCentral.strftime("%I:%M %p")
  print("Current Time", currentTimeStr)

  nextBuses = []
  for bus in busTimes:
      if isLater(bus, currentTimeStr):
          nextBuses.append(bus)

  # Fix: check the length of nextBuses before accessing elements
  if len(nextBuses) >= 2:
      firstBus = nextBuses[0]
      secondBus = nextBuses[1]
      print("The next bus will arrive in", minutesUntil(firstBus, nowCentral), "minutes.")
      print("The following bus will arrive in", minutesUntil(secondBus, nowCentral), "minutes.")
  elif len(nextBuses) == 1:
      firstBus = nextBuses[0]
      print("The next bus will arrive in", minutesUntil(firstBus, nowCentral), "minutes.")
      print("No more buses today.")
  else:
      print("No more buses today.")

main()
