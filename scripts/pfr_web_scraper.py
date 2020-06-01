import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

base_url = "https://www.pro-football-reference.com/years/"

years_list = list(range(1966, 2021))
weeks_list = list(range(1,22))

containers = []

filename = "nfl_records.csv"
f = open(filename, "w")

headers = "date, winner, winning_score, loser, losing_score, draw\n"
f.write(headers)

for year in years_list:
    for week in weeks_list:
        new_url = base_url+str(year)+"/"+"week_"+str(week)+".htm"
        try:
            uClient = uReq(new_url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")
            containers.append(page_soup.findAll("div", {"class":"game_summary expanded nohover"}))
        except:
            pass

for i in range(0, len(containers)):
    for j in range(0, len(containers[i])):
        date = containers[i][j].td.text
        winner = containers[i][j].find("tr", {"class":"winner"})
        loser = containers[i][j].find("tr", {"class":"loser"})
        if(winner == None):
            teams = containers[i][j].findAll("tr", {"class":"draw"})
            winning_team = teams[0].td.text
            losing_team = teams[1].td.text
            winning_score = teams[0].find("td", {"class":"right"}).text
            losing_score = winning_score
            draw = "Yes"
        else:
            winning_team = winner.a.text
            losing_team = loser.a.text
            winning_score = winner.find("td", {"class":"right"}).text
            losing_score = loser.find("td", {"class":"right"}).text
            draw = "No"
        f.write(" " + date.replace(",", "|") + "," + winning_team + "," + winning_score + "," + losing_team + "," + losing_score + "," + draw + "\n")
f.close()
