from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from getpass import getpass
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
sys.path.insert(0, "/Users/krishte/Documents/Programming/Python")
import Stuff as st
import urllib
import pandas as pd

#classes = ["https://portals-embed.veracross.eu/isbasel/student/classes/253873?", "https://portals-embed.veracross.eu/isbasel/student/classes/258506?", "https://portals-embed.veracross.eu/isbasel/student/classes/253997?","https://portals-embed.veracross.eu/isbasel/student/classes/257784?", "https://portals-embed.veracross.eu/isbasel/student/classes/273089?","https://portals-embed.veracross.eu/isbasel/student/classes/253744?","https://portals-embed.veracross.eu/isbasel/student/classes/267286?","https://portals-embed.veracross.eu/isbasel/student/classes/254639?", "https://portals-embed.veracross.eu/isbasel/student/classes/254734?"]


classes = ["https://portals-embed.veracross.eu/isbasel/student/classes/323037?","https://portals-embed.veracross.eu/isbasel/student/classes/323578?", "https://portals-embed.veracross.eu/isbasel/student/classes/310777?","https://portals-embed.veracross.eu/isbasel/student/classes/311850?","https://portals-embed.veracross.eu/isbasel/student/classes/311216?","https://portals-embed.veracross.eu/isbasel/student/classes/311051?","https://portals-embed.veracross.eu/isbasel/student/classes/310877?","https://portals-embed.veracross.eu/isbasel/student/classes/311577?","https://portals-embed.veracross.eu/isbasel/student/classes/311543?","https://portals-embed.veracross.eu/isbasel/student/classes/311895?","https://portals-embed.veracross.eu/isbasel/student/classes/311568?", "https://portals-embed.veracross.eu/isbasel/student/classes/311512?", "https://portals-embed.veracross.eu/isbasel/student/classes/326011?"]


options = Options()
options.add_argument('--headless')



nool = input("Class: ")
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, executable_path=r'/Users/krishte/chromedriver')



actualClasses = ["homeroom","homeroom extended","english", "german", "economics", "chemistry", "physics","math","tok core", "tok", "pe", "wellbeing", "counselling"]
#print(len(classes), len(actualClasses))
number = actualClasses.index(nool)


driver.get(classes[number])


username_box = driver.find_element_by_id("username")
password_box = driver.find_element_by_id("password")

username_box.send_keys(st.isbaselLogin)
password_box.send_keys(st.isbaselPassword)

final_box = driver.find_element_by_id("login-button")
final_box.click()


#assignments = driver.find_elements_by_class_name("assignment-description")
#grades = driver.find_elements_by_class_name("raw-score")

delay = 3 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "raw-score")))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time or no grades!")

    
assignmentgrades = driver.find_elements_by_class_name("raw-score")
assignmenttypes = driver.find_elements_by_class_name("assignment-type")
assignmentdates = driver.find_elements_by_class_name("assignment-due-date")
assignmentsdata = driver.find_elements_by_class_name("assignment-header")
assignmentdescriptions = driver.find_elements_by_class_name("assignment-description")

print(len(assignmentgrades), len(assignmenttypes), len(assignmentdates), len(assignmentsdata), len(assignmentdescriptions))

#assignmentgrades has the right size, for the rest check if it has a grade in assignmentsdata and use one less than length

counter = 0
typesvalues = ["", "", "","","", ""]
typeslist = ["Paper 1", "Paper 2", "Paper 3", "Oral", "Summative", "Test"]

for i in range(len(assignmentsdata)-1):
    if (assignmentsdata[i].text[-1].isdigit()):
        print(assignmentdates[i].text, assignmenttypes[i].text, assignmentdescriptions[i].text, assignmentgrades[counter].text)
        if assignmenttypes[i].text in typeslist:
            if typesvalues[typeslist.index(assignmenttypes[i].text)] == "":
                typesvalues[typeslist.index(assignmenttypes[i].text)] += assignmentgrades[counter].text
            else:
                typesvalues[typeslist.index(assignmenttypes[i].text)] += "," + assignmentgrades[counter].text
        else:
            print("There is a SERIOUS ISSUE " + assignmenttypes[i].text)
        counter += 1

for i in range(len(typesvalues)):
    print(typeslist[i] + ": " + typesvalues[i])


##html = driver.page_source

    

driver.close()
number = actualClasses.index(nool)
##dict_items = dict.items();
##dict_items = sorted(dict_items)
##
##print(dict_items)
##
##file = open("grades.txt", "r")
##if file.read().find(actualClasses[number].upper()) == -1:
##    file.close()
##    f = open("grades.txt", "a")
##    f.write("\n" + "\n" + actualClasses[number].upper())
##    
##    for key,val in dict.items():
##        f.write("\n"+ key + " = " + val)
##
##    f.close()

df = pd.read_csv("grades11.csv", index_col = False, dtype="str")
for i in range(len(typesvalues)):
   # print("Criterion " + i[0][0], i[1])
    #print(typesvalues[i])
    #df[typeslist[i]][number] = str(typesvalues[i])
    df.at[number, typeslist[i]] = str(typesvalues[i])

print(df)
df.to_csv("grades11.csv", index = False)

