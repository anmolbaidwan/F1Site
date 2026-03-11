from urllib.request import urlopen
import json
import re

index = 0
teams = {}
points = {}
team_logos = {
  "Alpine": "../logos/alpine.avif",
  "Aston Martin": "../logos/aston.avif",
  "Audi": "../logos/audi.avif",
  "Cadillac": "../logos/cadillac.avif",
  "Ferrari": "../logos/ferrari.avif",
  "Haas F1 Team": "../logos/haas.avif",
  "McLaren": "../logos/mclaren.avif",
  "Mercedes": "../logos/mercedes.avif",
  "Racing Bulls": "../logos/vcarb.avif",
  "Red Bull Racing": "../logos/redbull.avif",
  "Williams": "../logos/williams.avif",
  }

response = urlopen('https://api.openf1.org/v1/championship_teams?session_key=latest')
data = json.loads(response.read().decode('utf-8'))
if data:
  for teamdic in data:
    points[teamdic["team_name"]] = teamdic["points_current"] #get points
else: 
  for team in team_logos:
    points[team] = 0 #get points

response = urlopen('https://api.openf1.org/v1/drivers?&session_key=latest')
data = json.loads(response.read().decode('utf-8'))
for datadic in data:
  teams[datadic["team_name"]] = datadic["team_colour"]

sorted_teams = dict(sorted(teams.items()))
sortedbyPoints = {k: v for k, v in sorted(points.items(), key=lambda item: item[1], reverse = True)}

table_html = """
<table style="width:100%; border-collapse: separate; border-spacing: 3px; margin-top: 20px;">
  <thead>
    <tr style="background-color:#1c1c1c;">
      <th style="border:1px solid #ffffff; padding:20px; font-size: 24px;">Team Logo</th>
      <th style="border:1px solid #ffffff; padding:20px; font-size: 24px;">Team Name</th>
      <th style="border:1px solid #ffffff; padding:20px; font-size: 24px;">Points</th>
    </tr>
  </thead>
  <tbody>
"""
for team in sortedbyPoints:  
    image = team_logos[team]
    color = teams[team]
    point = points[team]
    table_html += f"""
      <tr style="text-align:center; background-color:#{color};">
      <th style="border:1px solid #ffffff; padding:12px; width:1%; white-space:nowrap"><img src="{image}" alt="{team}" width="111" style="border-radius:8px;"></th>
      <td style="border:1px solid #ffffff; padding:12px; font-size: 32px;">{team}</td>
      <th style="border:1px solid #ffffff; padding:20px; font-size: 32px;">{point}</th>
    </tr>
    """

table_html += "</tbody></table>"

# Read your existing teams.html
with open("docs/team.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject table at the placeholder
html_content = re.sub(
    r'(<div id="teams-table">).*?(</div>)',
    f"\\1{table_html}\\2",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML
with open("docs/team.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("team.html updated with new table!")