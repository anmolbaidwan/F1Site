from urllib.request import urlopen
import json
import re

index = 0
teams = {}
points = {}
#manually got each teams logo, need to find solution
team_logos = {
  "Alpine": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/alpine/2026alpinelogowhite.webp",
  "Aston Martin": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/astonmartin/2026astonmartinlogowhite.webp",
  "Audi": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/audi/2026audilogowhite.webp",
  "Cadillac": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/cadillac/2026cadillaclogowhite.webp",
  "Ferrari": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/ferrari/2026ferrarilogowhite.webp",
  "Haas F1 Team": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/haasf1team/2026haasf1teamlogowhite.webp",
  "McLaren": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/mclaren/2026mclarenlogowhite.webp",
  "Mercedes": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/mercedes/2026mercedeslogowhite.webp",
  "Racing Bulls": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/racingbulls/2026racingbullslogowhite.webp",
  "Red Bull Racing": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/redbullracing/2026redbullracinglogowhite.webp",
  "Williams": "https://media.formula1.com/image/upload/c_lfill,w_48/q_auto/v1740000000/common/f1/2026/williams/2026williamslogowhite.webp",
  }

#get all teams
response = urlopen('https://api.openf1.org/v1/championship_teams?session_key=latest')
data = json.loads(response.read().decode('utf-8'))
if data:
  for teamdic in data:
    points[teamdic["team_name"]] = teamdic["points_current"] #get points
else: 
  for team in team_logos:
    points[team] = 0 #get points

response = urlopen('https://api.openf1.org/v1/drivers?&session_key=latest') #get all team colors
data = json.loads(response.read().decode('utf-8'))
for datadic in data:
  teams[datadic["team_name"]] = datadic["team_colour"]

sorted_teams = dict(sorted(teams.items()))
sortedbyPoints = {k: v for k, v in sorted(points.items(), key=lambda item: item[1], reverse = True)} #sort teams by points

#Initial Table
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
    #add team info to table
    table_html += f"""
      <tr style="text-align:center; background-color:#{color};">
      <th style="border:1px solid #ffffff; padding:12px; width:1%; white-space:nowrap"><img src="{image}" alt="{team}" width="111" style="border-radius:8px;"></th>
      <td style="border:1px solid #ffffff; padding:12px; font-size: 32px;">{team}</td>
      <th style="border:1px solid #ffffff; padding:20px; font-size: 32px;">{point}</th>
    </tr>
    """

#finish table off
table_html += "</tbody></table>"

# Read teams.html
with open("docs/team.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject table at placeholder
html_content = re.sub(
    r'(<div id="teams-table">).*?(</div>)',
    f"\\1{table_html}\\2",
    html_content,
    flags=re.DOTALL
)

# Save teams.html
with open("docs/team.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("team.html updated with new table!")