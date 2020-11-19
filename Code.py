# Importing Libraries

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib as mpl

# Setting up the website for parsing

my_url = 'https://www.worldometers.info/coronavirus/'
req = Request(my_url, headers = {'User-Agent': 'XYZ/3.0'})
page_html = urlopen(req, timeout = 20).read()
page_soup = soup(page_html, "html.parser")

# Opening and Editing the CSV File 

filename = "CoronaWorldwide.csv"
f = open(filename, "w")
headers = "Total Cases, Total Deaths, Recovered, Active Cases, Closed Cases\n"
f.write(headers)

# Defining Elements for Scraping 

cases_container = page_soup.findAll("div", {"id":"maincounter-wrap"})

total_cases_container = cases_container[0]
total_cases = total_cases_container.div.span.text

deaths_container = cases_container[1]
deaths = deaths_container.div.span.text

recovered_container = cases_container[2]
recovered = recovered_container.div.span.text

cases_containerAC = page_soup.findAll("div", {"class":"col-md-6"})

activecase_container = cases_containerAC[0]
accase = activecase_container.find("div", {"class":"number-table-main"})
active_cases = accase.text

closedcase_container = cases_containerAC[1]
closcase = closedcase_container.find("div", {"class":"number-table-main"})
closed_cases = closcase.text

f.write(total_cases.replace(",","") + "," + deaths.replace(",","") + "," + recovered.replace(",","") + "," + active_cases.replace(",","") + "," + closed_cases.replace(",","") + "\n")        
f.close()

# Opening and Editing the CSV File 

filename = "CoronaByCountry.csv"
g = open(filename, "w")
headers = "Number, Country, Total Cases, Total Deaths, Recovered, Active Cases\n"
g.write(headers)

for tr in page_soup.find_all('tr')[9:224]:
    tds = tr.find_all('td')
    g.write(tds[0].text.replace(",","") + "," + tds[1].text.replace(",","") + "," + tds[2].text.replace(",","") + "," + tds[4].text.replace(",","") + "," + tds[6].text.replace(",","") + "," + tds[7].text.replace(",","") + "\n")
g.close()

# Reading and Plotting the Data

plt.style.use("fivethirtyeight")
data = pd.read_csv("coronabycountry.csv", sep = r'\s*,\s*', engine='python', encoding = 'ISO-8859-1')

# Modifying Data

piedataa = data['Country']
piedatab = data['Total Cases']
total_cases = int(total_cases.replace(",",""))
data_1 = data[0:16]
piedataa = piedataa[0:8]
piedatab = piedatab[0:8]
deaths = data_1["Total Deaths"]
total = data_1["Total Cases"]
countries = data_1["Country"]
pd.options.mode.chained_assignment = None  # default='warn'
mortality = (data_1['Total Deaths']/data_1['Total Cases']*100)
data_1 ['Mortality Rate'] = mortality
print(data_1)
sum = 0
for i in piedatab:
    sum = sum + i

piedataa[8] = "Others (~230 countries)"
piedatab[8] = (total_cases - sum)

'''for item in range(0,16):
    mortality.append((deaths[item]/total[item])*100)  '''
    
m = (countries.tolist())
m.reverse()
listm = list(map(list,zip(m, mortality)))
sortlist  = (sorted(listm, key = lambda x: (x[1],x[0]), reverse = True))

# Plot for Total Cases

plots = data_1.sort_values(by = 'Total Cases').plot(kind = 'barh', y = 'Total Cases', x = 'Country', legend = None)
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.title("Total Cases")
plt.tight_layout()
plt.savefig('Total Cases.png')
plt.show()

# Plot for Total Deaths

plots = data_1.sort_values(by = 'Total Deaths').plot(kind = 'barh', y = 'Total Deaths', x = 'Country', legend = None)
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.title("Total Deaths")
plt.tight_layout()
plt.savefig("Total Deaths.png")
plt.show()

# Plot for Mortality Rate

plots = data_1.sort_values(by = 'Mortality Rate').plot(kind = 'barh', y = 'Mortality Rate', x = 'Country', legend = None)
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.title("Mortality Rate")
plt.tight_layout()
plt.savefig("Mortality Rate.png")
plt.show()

# Plot for Pie Chart

mpl.rcParams['font.size'] = 11.5
plt.pie(piedatab, labels = piedataa, autopct = "%1.1f%%", )
plt.title("Cases and Countries")
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.savefig("Countries And Cases Pie Chart.png")
plt.show()