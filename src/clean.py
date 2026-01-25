import re

# Read your existing drivers.html
with open("../html/driver.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject table at the placeholder
html_content = re.sub(
    r'(<div id="drivers-table">).*?(</div>)',
    f"\\1{" "}\\2",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML
with open("../html/driver.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Read your existing teams.html
with open("../html/team.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject table at the placeholder
html_content = re.sub(
    r'(<div id="teams-table">).*?(</div>)',
    f"\\1{" "}\\2",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML
with open("../html/team.html", "w", encoding="utf-8") as f:
    f.write(html_content)