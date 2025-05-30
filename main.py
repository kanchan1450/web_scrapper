import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def fetch_jobs(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://weworkremotely.com/",
        "Connection": "keep-alive",
    }

    time.sleep(2)  # polite delay

    response = requests.get(url, headers=headers)
    print("URL requested:", response.url)
    print("Response status code:", response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    
    job_sections = soup.find_all("li", class_="feature")  # Each job is inside this <li>

    job_list = []

    for job in job_sections:
        try:
            link_tag = job.find("a", href=True)
            title = job.find("span", class_="title").get_text(strip=True)
            company = job.find("span", class_="company").get_text(strip=True)
            link = "https://weworkremotely.com" + link_tag["href"]
            job_list.append({"Title": title, "Company": company, "Link": link})
        except AttributeError:
            continue

    return job_list

def save_to_csv(jobs, keyword):
    if not os.path.exists("output"):
        os.makedirs("output")
    df = pd.DataFrame(jobs)
    file_path = f"output/jobs_{keyword}.csv"
    df.to_csv(file_path, index=False)
    print(f" Saved {len(jobs)} jobs to {file_path}")

if __name__ == "__main__":
    keyword = input(" Enter job keyword to search: ")
    jobs = fetch_jobs(keyword)
    if jobs:
        save_to_csv(jobs, keyword)
    else:
        print("No jobs found.")
