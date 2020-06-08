from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

my_url = 'https://www.worldometers.info/coronavirus/'
req = Request(my_url, headers = {'User-Agent': 'XYZ/3.0'})
page_html = urlopen(req, timeout = 20).read()
page_soup = soup(page_html, "html.parser")

filename = "CoronaWorldwide.csv"
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

plt.style.use("fivethirtyeight")

data = pd.read_csv("coronabycountry.csv", sep = r'\s*,\s*', engine='python', encoding = 'ISO-8859-1')

countries = data['Country']
total = data['Total Cases']
deaths = data['Total Deaths']
recoverd = data['Recovered']
active = data['Active Cases']
piedataa = data['Country']
piedatab = data['Total Cases']
total_cases = int(total_cases.replace(",",""))

data1 = data[0:16]


#Modifying Data

countries = countries[0:16]
total = total[0:16]
total = total[::-1]
countries = countries[::-1]
deaths = deaths[0:16]
deaths = deaths[::-1]
piedataa = piedataa[0:8]
piedatab = piedatab[0:8]

sum = 0
for i in piedatab:
    sum = sum + i

piedataa[8] = "Others (~230 countries)"
piedatab[8] = (total_cases - sum)

mortality = []
for item in range(0,16):
    mortality.append((deaths[item]/total[item])*100)  
    
m = (countries.tolist())
n = (deaths.tolist())
m.reverse()
n.reverse()

listm = list(map(list,zip(m, mortality)))
listn = list(map(list,zip(m, n)))

sortlist1 = (sorted(listn, key = lambda x: (x[1],x[0]), reverse = True))
sortlist  = (sorted(listm, key = lambda x: (x[1],x[0]), reverse = True))



#Plot for Total Cases

plt.barh(countries, total, height = 0.5, log = True)
plt.title("Total Cases")
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.savefig("TotalCases.png")
plt.show()





#Plot for Total Deaths

a = np.array(sortlist1)
plt.barh((a[:,0])[::-1], sorted(deaths), height = 0.5, log = 1)
plt.title("Total Deaths")
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.savefig("TotalDeaths.png")
plt.show()




#Plot for Mortality Rate

b = np.array(sortlist)

plt.barh((b[:,0])[::-1], sorted(mortality), height = 0.5)

plt.title("Mortality Rate (%)")

plt.tight_layout()

import matplotlib as mpl
mpl.rcParams['font.size'] = 10
    
fig = plt.gcf()

fig.set_size_inches(10,10)

plt.savefig("MortalityRate.png")

plt.show()

# Font Formatting

import matplotlib as mpl
mpl.rcParams['font.size'] = 11.5

#Plot for Pie Chart

plt.pie(piedatab, labels = piedataa, autopct = "%1.1f%%", )

plt.title("Cases and Countries")

plt.tight_layout()

fig = plt.gcf()

fig.set_size_inches(10,10)

plt.savefig("CountriesAndCasesPie.png")

plt.show()