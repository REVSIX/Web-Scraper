from bs4 import BeautifulSoup
import requests
import time

# Welcome user and ask for any unfamiliar skills 
print("Welcome to the Python Job Postings Calculator!")
print('Before we begin, are there any skills you are unfamilar with?')
unfamiliar_skill = input('> ').lower() # We use the .lower() method to filter out case sensitivity within the program.
print(f"Filtering out {unfamiliar_skill}...")

# Define the Command Used in the Program
def find_jobs():
    # Send an HTTP GET request and get the response
    response = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=')

    # Extract the HTML content from the response
    html_text = response.text

    # Create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(html_text, 'lxml')  # lxml is an external parser that reads the html file faster and more efficiently than python's standard html parser. 

    # Find job posts and format the findings per an indexed order
    job_posts = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for index, job in enumerate(job_posts):
        
        published_date = job.find('span', class_ = "sim-posted").span.text
        
        # Filter for recent postings
        if 'few' in published_date:
            company_role = job.h2.text
            company_name = job.h3.text
            company_location = job.span.text
            job_skills = job.find('span', class_ = "srp-skills").text.replace('  ',' ').lower() 
            job_link = job.find('a', href=True)['href']
            if unfamiliar_skill not in job_skills:
                
                # Create a new File for each job posting.
                with open (f'Jobs/{index}.txt', 'w') as f: 
                    f.write(f'''

    There is a job posting for a {company_role.strip()} at {company_name.strip()}. 

    The job is located in {company_location.strip()}. 

    Key skills include: {job_skills.strip()}.

    For more information, visit {job_link.strip()}.

        ''')
                    print(f'File Saved: {index}')

# Run the Web Scraper Every 10 Minutes
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10 
        print(f"Waiting for {time_wait} minutes...")
        time.sleep(time_wait*60)
