#Import Libraries
from bs4 import BeautifulSoup

#Open Local HTML File
with open('home.html', 'r') as html_file:
    content = html_file.read()

    #New Instance of BeatifulSoup
    soup = BeautifulSoup(content, 'lxml')
    
    #Search Request 
    course_cards  = soup.find_all('div', class_ = "card")
    
    #Format Scraped Data
    for course in course_cards:
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]

        print(f"{course_name} costs {course_price}.")
