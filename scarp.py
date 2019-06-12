'''
We'll be scraping weather forecasts from the National Weather Service,
and then analyzing them using the Pandas library.
The components of a web page

When we visit a web page, our web browser makes a request to a web
server. This request is called a GET request, since we're getting files
from the server. The server then sends back files that tell our browser
how to render the page for us. The files fall into a few main types:

HTML — contain the main content of the page.
CSS — add styling to make the page look nicer.
JS — Javascript files add interactivity to web pages.
Images — image formats, such as JPG and PNG allow web pages to show pictures.
After our browser receives all the files, it renders the page and displays it
to us. There's a lot that happens behind the scenes to render a page nicely,
but we don't need to worry about most of it when we're web scraping.
When we perform web scraping, we're interested in the main content of the web
page, so we look at the HTML.
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
print(forecast_items)
tonight = forecast_items[0]
print(tonight)
print(tonight.prettify())

'''

inside the forecast item tonight is all the information we want.
There are 4 pieces of information we can extract:

The name of the forecast item — in this case, Tonight.
The description of the conditions — this is stored in the title property of img.
A short description of the conditions — in this case, Mostly Clear.
The temperature low — in this case, 49 degrees.

We'll extract the name of the forecast item, the short description, and the temperature first,
since they're all similar:'''


period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

print(period)
print(short_desc)
print(temp)
'''
extract the title attribute from the img tag. To do this, we just treat the
BeautifulSoup object like a dictionary, and pass in the attribute we want as a
key:'''

img = tonight.find("img")
desc = img['title']

print(desc)

'''
we know how to extract each individual piece of information,
we can combine our
knowledge with css selectors and list comprehensions to extract everything
at
once.

# 1. Select all items with the class period-name inside an item with the
#class tombstone-container in seven_day.

# 2. Use a list comprehension to call the get_text method on each
# BeautifulSoup object.

'''
period_tags = seven_day.select(".tombstone-container .period-name")
print(period_tags)
periods = [pt.get_text() for pt in period_tags]
print(periods)

'''
our technique gets us each of the period names, in order. We can apply
the same technique to get the other 3 fields:
'''

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
print('\n##### Short Description starts Here #####' )
print(short_descs)
print('\n##### Short Description Ends Here #####' )
print(temps)
print('\n##### Temprature Ends Here #####' )
print(descs)
print('\n##### Description Ends Here #####' )
'''
combine the data into a Pandas DataFrame and analyze it. A DataFrame is an
object that can store tabular data, making data analysis easy. 
'''
weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs, 
        "temp": temps, 
        "desc":descs
    })
print('\n\n##### wheather report #####' )
print(weather)

writer = pd.ExcelWriter('whetherreport.xlsx', engine='xlsxwriter')
weather.to_excel(writer, sheet_name='whether')

writer.save()
# do some analysis on the data
# use a regular expression and the Series.str.extract method
# to pull out the numeric temperature values:

temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')

print('\n\n##### Temperature Numbers Only #####' )
print(temp_nums)
print('\n\n##### Mean Temperature #####' )
print(weather["temp_num"].mean()) # find mean of temprature

#select the rows that happen at night:
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
print('\n\n##### Night Temperature only #####' )
print(is_night)

print(weather[is_night])
'''
writer = pd.ExcelWriter('whetherreport.xlsx', engine='xlsxwriter')
weather.to_excel(writer, sheet_name='whether')

writer.save()
'''






