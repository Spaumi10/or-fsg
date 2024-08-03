import re
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By

# Setup webdriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# Setup database connection.
conn = sqlite3.connect("instance/fsg_app.sqlite")
cur = conn.cursor()
# cur.execute('USE fsg_app')

# TODO
"""
You could use a list of the division numbers and loop through them. One problem
with this is that each division will have different rules. You could use a conditional
check though. List is [722, 723, 724, 4730]
"""

# Starting division number.
division_num = 722

url = f"https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision={division_num}"
driver.implicitly_wait(5)
driver.get(url)

rules = driver.find_elements(By.CLASS_NAME, "rule_div")


# Obtain crime rankings, statute, crime name, and ranking factors.
rank_i = 2
for rule in rules:
    # Get rankings.
    ranking_text = rule.find_element(
        By.XPATH, f'//*[@id="content"]/div[{rank_i}]/p[1]/strong[2]'
    ).text
    ranking_list = ranking_text.split()
    if ranking_list[-1].isdecimal():
        ranking = ranking_list[-1]
        print(ranking)

    # Get ORSs
    # Ranking 11 has special path structure.
    if ranking == "11":
        ors = rule.find_element(By.XPATH, f'//*[@id="content"]/div[2]/p[3]').text
    else:
        ors_i = 1
        ors = rule.find_elements(
            By.XPATH, f'//*[@id="content"]/div[{rank_i}]/p/span'
        )
        for line in ors:
            if "ORS" in line.text:


    # Get crime name
    rank_i += 1

driver.quit()