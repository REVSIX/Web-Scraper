from bs4 import BeautifulSoup
import requests

# Send an HTTP GET request and get the response
response = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=')

# Extract the HTML content from the response
html_text = response.text

# Create a BeautifulSoup object from the HTML content
soup = BeautifulSoup(html_text, 'lxml')

# Find job posts and format the findings
job_posts = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
for job in job_posts:
    company_role = job.h2.text
    company_name = job.h3.text
    company_location = job.span.text
    print(f"There is a job posting for:")
    print(f"{company_name} Looking for a: {company_role}")
    print()
    print(f"The job is based in {company_location}.")
    for i in range(2):
        print()
