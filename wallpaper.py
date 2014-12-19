#!/usr/bin/python

#By kurrata on https://bbs.archlinux.org/viewtopic.php?pid=927506
#Edited by James
#A script for setting the desktop to a random image from
#a given wallpaper directory.

# This program creates a connection to a database file from which the
# locations of all the wallpaper file locations are stored.
# It then reads a file to see whether it should increase or decrease
# which row of the table it will pull the next picture from.

# TO-DO
#  Add a down arrow which will append the file's name to another file
# which can later be gone through manually to remove. The database will
# have to be notified of the change. Maybe even just flip the up arrow.
#  Have a text box somewhere or something to allow the program to
# either tag the photo in the database, or make the select statement
# give greater priority to photos with a certain tag.

import os
import random
import subprocess
import time
import sqlite3

SLEEP_TIME = 1 # Time spent sleeping between reading the input file
CHANGE_DELAY = 100 # How long passes before the paper is automatically changed
IMAGE_FORMATS = ['jpg', 'png', 'gif', 'jpeg', 'bmp']
HOME = "/home/james/"
WALLPAPER_DIR = HOME + "Stuff/Pictures/Wallpapers/"
INPUT_FILE = HOME + ".idesktop/command.txt"
PAPERS_TO_SORT = HOME + "Stuff/Pictures/Needs\ Sorting.txt"
DB_FILE = HOME + ".wallpaper.db"
ERROR_LOG = HOME + ".script_errors.txt"
# The SEED increases the number of papers skipped by the program whenever
# it chooses the next paper. This is to prevent users from getting used 
# to the order of the papers.
SEED = random.randrange(100)

def is_type(file, extensions):
    for extension in extensions:
        if file.endswith(extension):
            return True
    return False

def get_external_input():
    with open(INPUT_FILE, "r+") as f:
        command = f.readline()
        if command != 'none':
            os.system("echo > " + INPUT_FILE)
    return command

def log_error(error):
    os.system("echo " + error + " > " + ERROR_LOG)

def get_wallpaper(dbcon, n):
    """dbcon = the sqlite3 cursor
    n = row number of picture to be selected
    """
    dbcon.execute("select location from wallpapers where ROWID=?", (n,))
    results = [row for row in dbcon]
    if len(results) and len(results[0]):
        return results[0][0]
    return False

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

paperNumber = len(os.listdir(WALLPAPER_DIR))
currentRow = random.randrange(1, paperNumber)
lastChangeTime = 0
currentPaper = get_wallpaper(c, currentRow)
if currentPaper: subprocess.call(('feh', '--bg-max', currentPaper))
else: log_error(str(currentPaper) + " " + str(currentRow))
while True:
    command = get_external_input()
    
    if command == 'remove':
        os.system("echo " + currentPaper + " >> " + PAPERS_TO_SORT)
    elif command == 'next' or lastChangeTime > CHANGE_DELAY:
        currentRow += SEED
        currentRow %= paperNumber
        currentPaper = get_wallpaper(c, currentRow)
        if currentPaper and is_type(currentPaper, IMAGE_FORMATS):
            subprocess.call(('feh', '--bg-max', currentPaper))
        else: log_error(str(currentPaper) + " " + str(currentRow))
        lastChangeTime = 0
    elif command == 'prev':
        currentRow -= SEED
        if currentRow < 1:
            currentRow = paperNumber - abs(currentRow)
        currentPaper = get_wallpaper(c, currentRow)
        if currentPaper and is_type(currentPaper, IMAGE_FORMATS):
            subprocess.call(('feh', '--bg-max', currentPaper))
        else: log_error(str(currentPaper) + " " + str(currentRow))
        lastChangeTime = 0
 
    lastChangeTime += SLEEP_TIME
    time.sleep(SLEEP_TIME)
