import time
from selenium import webdriver
import random
import math
#made by daniel goldberg 2021. averages about 100 level 2 accounts an hour (1 every 30 s). or one level 1 acount in 13 s
words=[] #holds da words used to search. i have a list of 1000 popular words.
f=open("words.txt") #the list of popular words

for word in f.readlines(): #add them words to the list
    words.append(word[:-1])
f=open("email3.txt") #da list of bing account emails
driver = webdriver.Chrome('pathToChromeDriver')
emailCounter=1 #what number are we on
totalEmails=len(f.readlines())
programStartTime=time.perf_counter()
totalPointsEarnedInRun=0
totalPointsEarnedTotal=0
errorsEncountered=0
f=open("email3.txt") #da list of bing account emails
emails={}
for email in f.readlines(): #go through each one, homie
    if email[-1] == '\n':
        email = email[0:len(email) - 1]#gets rid of \n
    print("Email in use: " +str(emailCounter)+'/'+str(totalEmails)+' '+ email)
    emailCounter+=1
    #vvv go to the login page vvvv
    driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1611539831&rver=6.7.6631.0&wp=MBI_SSL&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253fwlexpsignin%253d1%26sig%3d334A818C1EDD6FAC2EB88E461F556EBE&lc=1033&id=264960&CSRFToken=136dce96-1e93-492a-a85e-e41e3678db28&aadredir=1")
    print("Signing in...")
    while True:
        try:
            emailSignin = driver.find_element_by_id('i0116') # tries to type in the email into the email text box
            emailSignin.send_keys(email)
            break
        except:
            errorFound=False
            try:
                driver.find_element_by_id('idTD_Error')
                errorFound=True
            except:
                pass

            if  errorFound==True or driver.current_url!="https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1611539831&rver=6.7.6631.0&wp=MBI_SSL&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253fwlexpsignin%253d1%26sig%3d334A818C1EDD6FAC2EB88E461F556EBE&lc=1033&id=264960&CSRFToken=136dce96-1e93-492a-a85e-e41e3678db28&aadredir=1":
                print("Login error. Restarting driver.")
                errorsEncountered += 1
                driver.close()  # if we found the error, restart the driver.
                driver = webdriver.Chrome('pathToChromeDriver')
                driver.get(
                    "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1611539831&rver=6.7.6631.0&wp=MBI_SSL&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253fwlexpsignin%253d1%26sig%3d334A818C1EDD6FAC2EB88E461F556EBE&lc=1033&id=264960&CSRFToken=136dce96-1e93-492a-a85e-e41e3678db28&aadredir=1")
                while True:  # now we try to enter the email again lol
                    try:
                        emailSignin = driver.find_element_by_id(
                            'i0116')  # tries to type in the email into the email text box
                        emailSignin.send_keys(email)
                        break
                    except:  # just incase a weird happens, reload page.. or just wait because its loading
                        time.sleep(.1)
                break
            time.sleep(.1)
    while True:
        try:
            # if it can find this vvvv then it knows its on the Enter Email page still and needs to click next
            if driver.find_element_by_partial_link_text('Create one!').text=="Create one!":
                driver.find_element_by_id('idSIButton9').click() #clicks next
                break
            else: #else it automatically went to the next page, so continue anyway
                break
        except: #except element hasnt loaded yet, wait

            time.sleep(.1)
    while True:
        try:
            driver.find_element_by_id('msaTileTitle').click() #clicks "personal profile"
            break
        except:#except sometimes, bing skips that^^^ step. check if password header is there vv,  that means it skipped
            try:
                if driver.find_element_by_id('loginHeader').text == "Enter password": #continue to password
                    break
            except: #except no password header, it hasnt loaded, wait.
                time.sleep(.1)
    while True:
        try:
            passwordSignin = driver.find_element_by_id('i0118') #find dat password box
            break
        except: #except it hasnt loaded
            time.sleep(.1)
    passwordSignin.send_keys("PASSWORD REDACTED lol")#hehe dont copy my password!!
    while True:
        try:
            driver.find_element_by_id('idSIButton9').click()#SIGN IN, BABY!!!
            break
        except:# except it hasnt loaded, wait
            time.sleep(.1)
    print("Getting point info...")
    #we are now taken to the bing.com search page!
    while True:#check if profile name switches from "sign in" to "alfred", the first name of every profile
        try:
            if driver.find_element_by_id("id_n").text == "alfred":
                break
            else:
                account = driver.find_element_by_id('id_l')  # find and 'click' profile button
                account.send_keys("\n")

        except: #it hasnt properly loaded, wait.
            time.sleep(.1)
    driver.get("https://www.bing.com/") #reloads the page so the points load:
    while True:  # lets me know when points load so we can click the rewards button..
        try:
            startingPoints = int(driver.find_element_by_id("id_rc").text)
            time.sleep(.1)
            m = int(driver.find_element_by_id("id_rc").text)
            if m == startingPoints:
                break
        except:
            time.sleep(.1)
    #the next three lines find a url inside the dropdown menu that takes us to some point stats we want.
    while True:
        try:
            driver.find_element_by_id('id_rh').click()  # rewards button. drop down menu showing point stats
            menu = driver.find_element_by_xpath('//*[@id="id_rh"]//../div[@id="bepfo"]/iframe')
            driver.get(menu.get_attribute('src'))  # go to url
            break
        except:
            time.sleep(.1)
    points=driver.find_element_by_class_name("mfo_c_es").text
    driver.get("https://www.bing.com/") #got da info, heading back to comman. go back to bing, squad
    if points[:2]=="PC":
        points=points[11:]#gets rid of substring "PC search: " at the start of the point tally
    else:
        pass
    pointsEarned=""
    for char in points: #loop seperates how many points we got today so far (probably 0, but just incase) from our limit
        if char!="/":
            pointsEarned=pointsEarned+char
        else:
            break
    #so in our '20/50' scenario i mentioned above, just as an example:
    totalPointsEarnable=points[len(pointsEarned)+1:] # this will be 50
    pointsLeftToEarn=int(totalPointsEarnable)-int(pointsEarned) #this will be 30
    timesToSearch=int(pointsLeftToEarn/5) #it will need to search 6 times (5 points per search) to get 30 points
    #and pointsEarned will be 20
    print("Points at start: " + str(startingPoints))
    print("Points to earn: " + str(pointsLeftToEarn))
    print("Times to search: " + str(timesToSearch))
    endingPoints=startingPoints+pointsLeftToEarn #how many points we should have once finished.
    #SEARCH LOOP FAM
    print("Searching...")
    while timesToSearch>0: #in our example above, we will loop/search 6 times!
        driver.find_element_by_id('sb_form_q').clear() #clears search box
        #vvvv searches 4 random words, fam.
        driver.find_element_by_id('sb_form_q').send_keys(words[random.randint(0, len(words) - 1)]+' '+words[random.randint(0, len(words) - 1)]+' '+words[random.randint(0, len(words) - 1)]+' '+words[random.randint(0, len(words) - 1)]+'\n')
        #makes sure page is loaded for next search via alfred showing. and idk im afraid it wont work if it doesnt load
        while True:
            if driver.find_element_by_id("id_n").text=="alfred":
                break
            else:
                time.sleep(.1)
        timesToSearch-=1 #one search complete
    print("Points at end: " + str(endingPoints) + '\n') #done, onto the next account!
    account=driver.find_element_by_id('id_l') #find and 'click' profile button
    while True:
        try:
            account.send_keys("\n")
            break
        except:
            time.sleep(.1)
    account.send_keys("\n")
    driver.execute_script("arguments[0].scrollIntoView();", account)#scroll to it so its in view of browser
    while True:#then click the sign out button!
        try:
            driver.find_element_by_xpath('//*[@id="id_h"]/span[@id="id_d"]//a').click()
            break

        except:
            try:
                account.send_keys("\n")
            except:
                pass
    totalPointsEarnedInRun+=pointsLeftToEarn
    totalPointsEarnedTotal+=endingPoints
    emails[email]=endingPoints
programEndTime=time.perf_counter()
print("\n\nAccounts in order of least to most points:\n")
sorted_keys = sorted(emails, key=emails.get)
for w in sorted_keys:
    print(w+": "+str(emails[w])+" points")
print("\n\nTotal Time to run "+str(totalEmails)+" accounts: "+str(math.ceil(programEndTime-programStartTime))+" s (around "+str(round((programEndTime-programStartTime)/totalEmails,1))+" s / per account)")
print("Total points in your pocession, sire: "+str(totalPointsEarnedTotal))
print("Total points earned from this run: "+str(totalPointsEarnedInRun))
print("Number of errors bing sent: "+str(errorsEncountered))
driver.close()
