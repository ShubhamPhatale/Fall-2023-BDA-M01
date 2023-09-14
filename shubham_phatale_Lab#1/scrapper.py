from selenium import webdriver
from bs4 import BeautifulSoup

url = "https://cs.uic.edu/faculty-staff/faculty/"

viewer = webdriver.Chrome()

viewer.get(url)
response = viewer.page_source
parser = BeautifulSoup(response, "html.parser")
professors_container = parser.find("div", class_="_section")
professor_names = professors_container.find_all("span", class_="_name")

with open("allScrappedData.txt", "w", encoding="utf-8") as file:
    for professor in professor_names:
        subjects = []
        bioLink = professor.a["href"]
        viewer.get(bioLink)
        urlResponse = viewer.page_source
        parser = BeautifulSoup(urlResponse, "html.parser")
        facultyName = parser.find("div", class_="profile-header").find("div", class_="_colB").find("h1").text
        facultyBio = parser.find("div", class_="profile-body").find("div", class_="_colB").find_all("section")
        for section in facultyBio:
            about_heading = section.find('h2', string="About")
            subjects = []
            teaching_tag = section.find('strong', string="Teaching:")
            if teaching_tag:
                hash3 = teaching_tag.parent
                hasul = hash3.find_next('ul')
                if hasul:
                    listtags = hasul.find_all('li')
                    for li in listtags:
                        subjects.append(li.get_text(strip=True))
            if about_heading:
                about_text = section.find("p")
                if about_text:
                    isHeading = about_text.find("strong")
                    if isHeading:
                        bio = ""
                    else:
                        bio = about_text.text
                    break
        file.write(f"{facultyName}   {bio}    {subjects}\n")
        file.write("\n")

viewer.quit()
