from urllib.request import Request, urlopen       
from bs4 import BeautifulSoup as soup

my_url = 'https://www.worldometers.info/coronavirus/'
req = Request(my_url, headers = {'User-Agent': 'XYZ/3.0'})
page_html = urlopen(req, timeout = 20).read()
page_soup = soup(page_html, "html.parser")

filename = "corona.csv"
f = open(filename, "w")
headers = "Total Cases, Total Deaths, Recovered, Active Cases, Closed Cases\n"
f.write(headers)

cases_container = page_soup.findAll("div", {"id":"maincounter-wrap"})
#print(cases_container[0])

total_cases_container = cases_container[0]
total_cases = total_cases_container.div.span.text
#print(total_cases)

deaths_container = cases_container[1]
deaths = deaths_container.div.span.text
#print(deaths)

recovered_container = cases_container[2]
recovered = recovered_container.div.span.text
#print(recovered)

cases_container1 = page_soup.findAll("div", {"class":"col-md-6"})

activecase_container = cases_container1[0]
accase = activecase_container.find("div", {"class":"number-table-main"})
active_cases = accase.text
#print(active_cases)

closedcase_container = cases_container1[1]
closcase = closedcase_container.find("div", {"class":"number-table-main"})
closed_cases = closcase.text
#print(closed_cases)

f.write(total_cases.replace(",","") + "," + deaths.replace(",","") + "," + recovered.replace(",","") + "," + active_cases.replace(",","") + "," + closed_cases.replace(",","") + "\n")        
f.close()

filename = "CoronaByCountry.csv"
g = open(filename, "w")
headers = "Number, Country, Total Cases, Total Deaths, Recovered, Active Cases\n"
g.write(headers)

for tr in page_soup.find_all('tr')[9:224]:
    tds = tr.find_all('td')
    g.write(tds[0].text.replace(",","") + "," + tds[1].text.replace(",","") + "," + tds[2].text.replace(",","") + "," + tds[4].text.replace(",","") + "," + tds[6].text.replace(",","") + "," + tds[7].text.replace(",","") + "\n")
    #print(tds[0].text, tds[1].text, tds[2].text, tds[4].text, tds[6].text, tds[7].text)
g.close()

print("Done! You can now check your computer for the files. ")