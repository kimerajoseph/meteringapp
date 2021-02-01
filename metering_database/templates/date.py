from datetime import date

years = []
for i in range(-2,5):
    year= date.today().year + i
    years.append(year)
print(years)
