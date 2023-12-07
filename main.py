# Click documentation:
# https://click.palletsprojects.com/en/8.1.x/#documentation
#
# Setuptools:
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
#
# Start virtual environment:
# . .venv/bin/activate

from pathlib import Path
import random
import click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from datetime import datetime

from dotenv import load_dotenv
from dotenv import set_key
import time, os
import functions

load_dotenv()

send_sms_message = False
send_email_message = False

def add_course(cat, driver):
    #add button
    driver.find_element(By.NAME, '5.1.27.1.23').click()
    time.sleep(3)
    course_box = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/span[2]/input[1]')

    course_box.send_keys(cat)
    time.sleep(2)
    driver.find_element(By.NAME, '5.1.27.7.9').click()
    time.sleep(2)
    
    #IF CAT CODE IS <6 CHARS
    try:
        result = driver.find_element(By.CLASS_NAME, 'alert')
        click.echo(result.text)
        driver.find_element(By.XPATH,'/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[3]/tbody/tr/td/span/a').click()
    except NoSuchElementException:

        #add button
        driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[7]/td[2]/input[1]').click()
        
        result = driver.find_elements(By.XPATH, "//span[@class='bodytext']/font/b")
    
        res = []
        for text in result:
            res.append(text.text)
        string = ' '.join(res)

        #IF COURSE WAS ADDDED
        if "The course has been successfully added." in string:
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[2]/span').text
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            #click.echo(f"The course {cur_course} has been successfully added.\nTHIS ACTION HAS FINANCIAL IMPACT TO YOUR FINANCIAL ACCOUNT\nVISIT https://sfs.yorku.ca FOR UPDATED TUTION INFORMATION.")
            body=f"\nThe course {cur_course} has been successfully added.\nTHIS ACTION HAS FINANCIAL IMPACT TO YOUR STUDENT FINANCIAL ACCOUNT.VISIT HTTPS://SFS.YORKU.CA FOR UPDATED TUTION INFORMATION."
            click.echo(body)
            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.23.9').click()
            return 0

        #IF COURSE WAS NOT ADDED BECAUSE IT IS FULL
        elif "The course you are trying to add is full." in string:
            time.sleep(3)
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            click.echo(f"The course {cur_course} has not been added. The course you are trying to add is full.")
            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.27.11').click()
            return -1

        #IF COURSE WAS NOT ADDED BECAUSE IT IS RESERVED
        elif "The spaces in this course are reserved." in string:
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            click.echo(f"The course {cur_course} has not been added. The spaces in this course are reserved.")
            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.27.11').click()
            return -1

        else:
            click.echo(string)

def transfer_course(cat, driver):
    #transfer button
    driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[4]/tbody/tr[1]/td[3]/div/input').click()
    time.sleep(3)
    
    course_box = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/input[1]')
    course_box.send_keys(cat)
    time.sleep(2)
    driver.find_element(By.NAME, '5.1.27.7.9').click() # "Transfer Course" button
    time.sleep(2)
    
        # The catalogue number for the course you wish to transfer does not match the existing course. Please try again. 
    try:
        result = driver.find_element(By.CLASS_NAME, 'alert')
        click.echo(result.text)
        time.sleep(3)
        driver.find_element(By.XPATH,'/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[4]/tbody/tr/td/span/a').click()
        
    except NoSuchElementException:
        time.sleep(3)
        driver.find_element(By.NAME, '5.1.27.11.11').click() #Please confirm that you want to: Transfer to: YES
        
        result = driver.find_elements(By.XPATH, "//span[@class='bodytext']/font/b")

        res = []
        for text in result:
            res.append(text.text)
        string = ' '.join(res)

        # The course has been successfully transferred.
        if "The course has been successfully transferred." in string: 
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[2]/span').text       
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            
            body=f"\nYou have successfully been transferred into {cur_course}.\nTHIS ACTION HAS FINANCIAL IMPACT TO YOUR STUDENT FINANCIAL ACCOUNT. VISIT HTTPS://SFS.YORKU.CA FOR UPDATED TUTION INFORMATION.",
            
            if send_sms_message: functions.send_sms(body)
            if send_email_message: functions.send_email(body)

            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.19.9').click() #continue button

        #The course has not been transfered. The spaces in this course are reserved.
        elif "The spaces in this course are reserved." in string:
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text       
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            click.echo(f"The course {cur_course} has not been transfered to.\nThe spaces in this course are reserved.")
            time.sleep(3)
            driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[8]/td[2]/input').click() #continue button 
        
        # The course has not been transfered.
        # The course you are trying to add is full.
        elif "The course you are trying to add is full." in string: 
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text       
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            click.echo(f"The course {cur_course} has not been transfered to - The course is full.")
            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.23.11').click()
        else:
            click.echo(string)
        #click.echo result

def login(webDriver, url, noDuo=False):
    click.echo("Logging in...")
    webDriver.set_window_size(1200, 1000)
    webDriver.get(url)
    #fill username
    username = webDriver.find_element(By.XPATH, "//*[@id='mli']")
    username.send_keys(os.getenv("PPY_USERNAME"))
    time.sleep(3)

    #fill password
    password = webDriver.find_element(By.XPATH, "//*[@id='password']")
    password.send_keys(os.getenv("PPY_PASSWORD"))
    time.sleep(3)

    #click on submit button
    webDriver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/form/div[2]/div[2]/p[2]/input").click()
    time.sleep(3)

    #duo 2fa
    if (not noDuo):
        click.echo("Trying to authenticate...")
        WebDriverWait(webDriver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='duo_iframe']")))
        WebDriverWait(webDriver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[4]/div/div/div/button'))).click()
        WebDriverWait(webDriver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/form/div[2]/div/label/input"))).click()
        WebDriverWait(webDriver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button"))).click()
        click.echo("Authentication request sent, press twice (10s)")
        time.sleep(10)
        
    webDriver.get(url)

def isFull(webDriver):
    #courseDiv= WebDriverWait(webDriver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "")))
    time.sleep(5)
    try:
        webDriver.find_element(By.CLASS_NAME, "seatText")
        return False
    except:
        return True

def loadREM(webDriver):
    click.echo("Loading REM...")
    webDriver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")
    select_element = WebDriverWait(webDriver, 60).until(EC.visibility_of_element_located((By.NAME, "5.5.1.27.1.11.0")))

    # Create a Select object
    select = Select(select_element)
    select.select_by_value("3")

    time.sleep(3)

    webDriver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input').click()
    time.sleep(3)

def loadVSB(webDriver, cat):
    click.echo("Loading VSB...")
    webDriver.get("https://schedulebuilder.yorku.ca/vsb/")
    time.sleep(3)
    webDriver.find_element(By.XPATH, '//*[@id="code_number"]').send_keys(cat)
    time.sleep(2)
    webDriver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[4]/div/table/tbody/tr/td[1]/div[4]/div[1]/div[2]/div[2]/div[3]/label').click()
    time.sleep(2)
    webDriver.find_element(By.XPATH, '//*[@id="addCourseButton"]').click()
    time.sleep(3)
    click.echo(webDriver.current_url)
    return webDriver.current_url


watchlist = [["C57E01", 'A']]
''' 
    X44V01 - EECS 3221 A - What I actually want
    G84J01 - MATH 1014 A - An example of a successful add.
    F46T02 - EECS 3101 A - An example of a full course.
    V21Y01 - EECS 2911 M - An example of a reserved course.

    TRANSFER SECTIONS Successfully
        C27P02 -> C27P03 or C27P04 - EECS 1022
    TRANSFER TO FULL SECTION
        1015 A (N59W02) to 1015 B (H06X02)
    TRANSFER TO RESERVED SECTION
        3101 M (X87W02) TO 3101 Z (S81Q02)
'''

@click.group()
def cli():

    # Create .env if it doesn't exist
    try:
        env_file_path = Path(".env")
        # Create an .env file if it doesn't exist
        env_file_path.touch(mode=0o600, exist_ok=False)
    except:
        pass

    # Create courses.txt if it doesn't exist

    try:
        f = open("courses.txt", "x")
    except:
        pass

@cli.command()
@click.argument('interval', default=120)
def set_interval(interval):
    env_file_path = Path(".env")
    # Save some values to the file.
    set_key(dotenv_path=env_file_path, key_to_set="INTERVAL", value_to_set=interval)

@cli.command()
def list():

    # List all courses in courses.txt

    path = Path("courses.txt")
    
    f = open("courses.txt", "r")

    # If courses file is empty

    if (path.stat().st_size == 0):
        click.echo("No courses are currently being monitored.")
        click.echo("hint: Add courses with 'command add course'")
        f.close()
        exit()

    click.echo("These courses are currently being monitored:")
    for i, line in enumerate(f):
        arr = line.split(",")
        action = arr[-1]
        if (action == 'A\n'):
            print(f"{i}: {arr[0]} (course add)")
        if (action == 'T\n'):
            print(f"{i}: {arr[1]} (transferring from {arr[0]})")
       
    f.close()

    click.echo("hint: Remove an entry with 'command remove ENTRY_NUMBER' eg. 'command remove 0'.")

    

@cli.command()
@click.argument('course')
def add(course):

    # Append new course to end of file

    f = open("courses.txt", "a")
    f.write(f"{course},A\n")
    f.close()
    click.echo(f"Course {course} successfully added to the list.")
    click.echo(f"hint: View course list with 'command list'.")

@cli.command()
@click.argument('removed_course')
@click.argument('added_course')
def transfer(removed_course, added_course):
    f = open("courses.txt", "a")
    f.write(f"{removed_course},{added_course},T\n")
    f.close()

    click.echo(f"Transfer from {removed_course} to {added_course} successfully added to the list.")
    click.echo(f"hint: View list with 'command list'.")

@cli.command()
@click.argument('entry_number', type=int)
def remove(entry_number):

    f = open("courses.txt", "r")

    # Check if courses file is empty
    path = Path("courses.txt")
    if (path.stat().st_size == 0):
        click.echo("No courses are currently being monitored. Add courses with 'command add course'")
        f.close()
        exit()

    # Read course information, apply removal

    arr = []
    for line in f:
        arr.append(line)
    click.echo(f"Entry {arr[entry_number]} removed")
    arr.remove(arr[entry_number])
    f.close()

    # Write new information

    f = open("courses.txt", "w")
    for line in arr:
        f.write(line)
    f.close()

   

@click.command()
@click.argument('email')
def set_email(email):
    env_file_path = Path(".env")
    # Save some values to the file.
    set_key(dotenv_path=env_file_path, key_to_set="EMAIL", value_to_set=email)


@click.command()
@click.argument('username')
def set_user(username):
    env_file_path = Path(".env")
    # Save some values to the file.
    set_key(dotenv_path=env_file_path, key_to_set="PPY_USERNAME", value_to_set=username)


@click.command()
@click.option("--password", prompt=True, hide_input=True)
def set_pass(password):
    env_file_path = Path(".env")
    # Save some values to the file.
    set_key(dotenv_path=env_file_path, key_to_set="PPY_PASSWORD", value_to_set=password)

#def set_path():
    

@click.command()
@click.option('--headless', is_flag=True, help="Run CourseSnipe without displaying browser", default=False, show_default=True)
def run(headless):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = "/snap/bin/geckodriver"  # fix this to not be hardcoded, find path automatically somehow
    driver_service = Service(executable_path=path)

    driver = webdriver.Firefox(options=options, service=driver_service)

    login(driver, "https://schedulebuilder.yorku.ca/vsb/")

    linkDict = {}

    click.echo("Fetching course code URLs...")

    for entry in watchlist:
        cat, action = entry
        linkDict[cat] = loadVSB(driver, cat)


    time.sleep(4)
    startTime = datetime.now().time()
    while (len(watchlist) != 0):
        for entry in watchlist:
            cat, action = entry
            if action == 'A':
                driver.get(linkDict[cat])
                full = isFull(driver)
                if (not full):
                    click.echo(f"Attempting to enroll into {cat}")
                    loadREM(driver)
                    add_course(cat, driver)
                    watchlist.remove(entry)
                else:
                    click.echo(f"Course {cat} is full, pinging again in 60 seconds")
                    time.sleep(5)
            try:
                username = driver.find_element(By.XPATH, "//*[@id='mli']")
                password = driver.find_element(By.XPATH, "//*[@id='password']")
                click.echo("Booted from VSB, relogging")
                login(driver, "https://schedulebuilder.yorku.ca/vsb/", True)
            except:
                pass
            try:
                banned = ( driver.find_element(By.XPATH, '/html/body/h1').text == "Forbidden" )
                if (banned):
                    click.echo(f"Banned from VSB, total duration of session {datetime.now().time() - startTime}")
                    driver.quit()
                    exit()
            except:
                pass
            time.sleep(200 + random.randint(-10,20)) # Randomness to make behaviour look human

    driver.quit()


cli.add_command(run)
cli.add_command(set_email)
cli.add_command(set_pass)
cli.add_command(set_user)
cli.add_command(set_interval)
cli.add_command(add)
cli.add_command(remove)
cli.add_command(list)

if __name__ == "__main__":
    cli()



