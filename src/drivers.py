from urllib.request import urlopen
import json
import re

#dictionary init
driver_name = {} 
team_name = {}
headshot = {}
colors = {}
driver_points = {}
response = urlopen('https://api.openf1.org/v1/drivers?&session_key=latest')
data = json.loads(response.read().decode('utf-8'))
for datadic in data: #for each list in the API call dictionary, extract Driver Name, Team Name, Image, and Color
  driver_name[datadic["driver_number"]] = datadic["full_name"].title()
  team_name[datadic["driver_number"]] = datadic["team_name"]
  headshot[datadic["driver_number"]] = datadic["headshot_url"]
  colors[datadic["driver_number"]] = datadic["team_colour"]

response = urlopen('https://api.openf1.org/v1/championship_drivers?session_key=latest') #get points for each driver
cdata = json.loads(response.read().decode('utf-8'))
if cdata:
  for datadic in cdata:
    driver_points[datadic["driver_number"]] = datadic["points_current"]
else:
  for datadic in data:
     driver_points[datadic["driver_number"]] = 0
sortedbyPoints = {k: v for k, v in sorted(driver_points.items(), key=lambda item: item[1], reverse = True)} #sort by points descending


#Initial Table
table_html = """
<table style="width:100%; border-collapse: collapse; margin-top: 20px;">
  <thead>
    <tr style="background-color:#1c1c1c;">
      <th style="border:1px solid #ffffff; padding:8px; font-size: 24px;">Image</th>
      <th style="border:1px solid #ffffff; padding:8px; font-size: 24px;">Driver</th>
      <th style="border:1px solid #ffffff; padding:8px; font-size: 24px;">Number</th>
      <th style="border:1px solid #ffffff; padding:8px; font-size: 24px;">Team</th>
      <th style="border:1px solid #ffffff; padding:8px; font-size: 24px;">Points</th>
    </tr>
  </thead>
<tbody>
"""

for number in sortedbyPoints:
  if number in driver_name:
    name = driver_name[number]
    image = headshot[number]
    color = colors[number]
    points = driver_points[number]
    team = team_name[number]
    #this adds each driver to the end of the table
    table_html += f"""
    <tr style="text-align:center; background-color:#{color};">
      <td style="border:1px solid #ffffff; padding:8px; width:1%;"><img src="{image}" alt="{name}" width="111" style="border-radius:8px;"></td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 32px;">{name}</td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 48px; font-weight: bold;">{number}</td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 32px;">{team}</td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 32px;">{points}</td>
    
    </tr>
    """
#close table
table_html += "</tbody></table>"

# Read drivers.html
with open("docs/driver.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject table at the placeholder
html_content = re.sub(
    r'(<div id="drivers-table">).*?(</div>)',
    f"\\1{table_html}\\2",
    html_content,
    flags=re.DOTALL
)

# Save drivers.html
with open("docs/driver.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("driver.html updated with new table!")
