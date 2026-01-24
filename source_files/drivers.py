from urllib.request import urlopen
import json
import re

driver_number = {} 
team_name = {}
headshot = {}
colors = {}
driver_points = {}
for i in range(99):

    response = urlopen('https://api.openf1.org/v1/drivers?driver_number=' + str(i) + '&session_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    if data:
        datadic = data[0]
        driver_number[datadic["full_name"].title()] = datadic["driver_number"]
        team_name[datadic["full_name"].title()] = datadic["team_name"]
        headshot[datadic["full_name"].title()] = datadic["headshot_url"]
        colors[datadic["full_name"].title()] = datadic["team_colour"]

for name in driver_number:  
  response = urlopen('https://api.openf1.org/v1/championship_drivers?session_key=latest&driver_number=' + str(driver_number[name]))
  data = json.loads(response.read().decode('utf-8'))
  datadic = data[0]
  driver_points[name] = datadic["points_current"]

sortedbyPoints = {k: v for k, v in sorted(driver_points.items(), key=lambda item: item[1], reverse = True)}

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

for name in sortedbyPoints:
    number = driver_number[name]
    image = headshot[name]
    color = colors[name]
    points = driver_points[name]
    team = team_name[name]
    table_html += f"""
    <tr style="text-align:center; background-color:#{color};">
      <td style="border:1px solid #ffffff; padding:8px; width:1%;"><img src="{image}" alt="{name}" width="111" style="border-radius:8px;"></td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 32px;">{name}</td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 48px; font-weight: bold;">{number}</td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 32px;">{team}</td>
      <td style="border:1px solid #ffffff; padding:8px;font-size: 32px;">{points}</td>
    
    </tr>
    """

table_html += "</tbody></table>"

# Read your existing drivers.html
with open("../html/driver.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject table at the placeholder
html_content = re.sub(
    r'(<div id="drivers-table">).*?(</div>)',
    f"\\1{table_html}\\2",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML
with open("../html/driver.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("driver.html updated with new table!")
