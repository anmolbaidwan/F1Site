from urllib.request import urlopen
import json
import re

index = 0
name_list = []
driver_number = []
team_name = []
headshot = []
colors = []
drive_points = []

for i in range(99):

    response = urlopen('https://api.openf1.org/v1/drivers?driver_number=' + str(i) + '&session_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    if data:
        dic = data[0]
        name_list.append(dic["full_name"].title())
        driver_number.append(dic["driver_number"])
        team_name.append(dic["team_name"])
        headshot.append(dic["headshot_url"])
        colors.append(dic["team_colour"])

for number in driver_number:  
  response = urlopen('https://api.openf1.org/v1/championship_drivers?session_key=latest&driver_number=' + str(number))
  data = json.loads(response.read().decode('utf-8'))
  datadic = data[0]
  drive_points.append(datadic["points_current"])
table_html = """
<table style="width:100%; border-collapse: collapse; margin-top: 20px;">
  <thead>
    <tr style="background-color:#1c1c1c;">
      <th style="border:1px solid #ffffff; padding:8px;">Image</th>
      <th style="border:1px solid #ffffff; padding:8px;">Driver</th>
      <th style="border:1px solid #ffffff; padding:8px;">Number</th>
      <th style="border:1px solid #ffffff; padding:8px;">Team</th>
      <th style="border:1px solid #ffffff; padding:8px;">Points</th>
    </tr>
  </thead>
<tbody>
"""

for name, number, team, image, color, points in zip(name_list, driver_number, team_name, headshot, colors, drive_points):
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
with open("driver.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject table at the placeholder
html_content = re.sub(
    r'(<div id="drivers-table">).*?(</div>)',
    f"\\1{table_html}\\2",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML
with open("driver.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("driver.html updated with new table!")
