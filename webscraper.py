import time
from selenium import webdriver
from BetterBot.func import *

while True:
    '''''''''''''''''
    SELENIUM
    opens ucm course 
    page and grabs 
    source html
    '''''''''''''''''
    url = "https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_SelectSubject"
    driver = webdriver.Chrome(executable_path=r"C:\Users\colin\Downloads\chromedriver.exe")
    #driver.set_window_position(-1000, -1000)
    driver.get(url)
    springBtn = driver.find_elements_by_xpath("//input[@value='202110']")[0]
    allCourses = driver.find_elements_by_xpath("//input[@value='N' and @name='openclasses']")[0]
    submit_button = driver.find_elements_by_xpath('/html/body/div[3]/form/input')[0]
    allCourses.click()
    submit_button.click()
    html = driver.page_source
    newHTML = ''
    driver.close()
    clear = open("html.txt", "w")
    clear.write("")
    thing = open("html.txt", "a")
    for x in html:
        thing.write(x)
    '''''''''''''''''
    LOOKING THROUGH 
    HTML
    '''''''''''''''''
    category = '<tbody><tr bgcolor="#FFC605">\n<th class="ddlabel" scope="row"><p class="leftaligntext"><small>CRN</small></p></th>\n<th class="ddlabel" scope="row"><p class="leftaligntext"><small>Course #</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Course Title</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Units</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Actv</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Days</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Time</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Bldg/Rm</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Start - End</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Instructor</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Max Enrl</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Act Enrl</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Seats Avail</small></p></th>\n</tr>'
    absMin = html.find("NOTE: Schedule Subject to Change")
    absMax = html.find("This is table displays line separator at end of the page")
    newHTML = html[absMin+len("NOTE: Schedule Subject to Change")+29 : absMax-58]

    for x in range(41):
        min = newHTML.find("<h3>")
        max = newHTML.find("</h3>")
        if (min >= 0) and (max >= 0):
            newHTML = newHTML[0:min] + newHTML[max + 5:len(newHTML)]
    for x in range(41):
        if (newHTML.find("#FFC605") - 85 >= 0):
            newHTML = newHTML[0: newHTML.find("#FFC605") - 85] + newHTML[newHTML.find("#FFC605") - 85 + len(category) + 66: len(newHTML)]

    clear = open("newhtml.txt", "w")
    clear.write("")
    thing = open("newhtml.txt", "a")
    for x in newHTML:
        thing.write(x)


    '''''''''''''''''
    ADDING SEARCHED 
    VALUES TO ARRAY
    '''''''''''''''''
    arr=[[],[],[],[]]
    '[[subjcode],[crsenumb],[crn],[available]'
    def createArr(searchType, arrSpot, thingAfter):
        currentSpot = 0
        for x in range(1730):
            if (newHTML.find(searchType) >= 0):
                currentSpot = newHTML.find(searchType, currentSpot) - 1
                arr[arrSpot].append(newHTML[newHTML.find(searchType, currentSpot) + len(searchType): newHTML.find(thingAfter,newHTML.find(searchType, currentSpot) + len(searchType))])
                currentSpot += 2

    createArr("subjcode=", 0, "&amp")
    createArr("crsenumb=", 1, "&amp")
    createArr("crn=", 2, "\">")

    '''''''''''''''''
    SET AVAILABILITY
    '''''''''''''''''
    currentSpot = 0
    for x in range(1730):
        try:
            if (newHTML.find("</small></p></td>\n</tr>")-7 != 0):
                currentSpot = newHTML.find("</small></p></td>\n</tr>", currentSpot) - 7
                beforeAvail = newHTML.find(">", currentSpot) + 1
                afterAvail = newHTML.find("<", currentSpot)
                numAvail = newHTML[beforeAvail: afterAvail]

                if numAvail == "Closed":
                    numAvail = 0
                try:
                    if int(numAvail) < 0:
                        numAvail = 0
                except:
                    None
                arr[3].append(int(numAvail))
                currentSpot += 8
        except:
            None

    resetOld = open("oldMasterCourses.txt", "w")
    resetOld.write("")
    resetOld.close()
    old = open("oldMasterCourses.txt", "a")
    oldMaster = open("masterCourses.txt", "r")
    for x in oldMaster:
        old.write(x)
    old.close()
    resetMaster = open("masterCourses.txt", "w+")
    resetMaster.write("")
    resetMaster.close()
    master = open("masterCourses.txt", "a")
    for x in arr:
        master.write("!")
        for y in x:
            master.write(str(y))
            master.write("\n")
    master.close()

    arr = getArr("masterCourses.txt")
    old = getArr("oldMasterCourses.txt")
    changed = []
    writeFile("changes.txt", "")
    update = []

    for i, x in enumerate(arr[3]):
        if x != old[3][i]:
            changed.append(arr[2][i])
            update.append(i)
    # debug
    for x in update:
        print(arr[0][x] + arr[1][x] + "  new: " + arr[3][x] + "  old: " + old[3][x])
    if changed != []:
        for x in changed:
            appendFile("changes.txt", x)

    time.sleep(20)