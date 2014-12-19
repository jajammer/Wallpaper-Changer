# This script creates a sqlite database file with all of the
# files in a directory added as entries
#
import sqlite3
import os

dbFile = '/home/james/.wallpaper.db'
paperRootPath = '/home/james/Stuff/Pictures/Wallpapers/'

conn = sqlite3.connect(dbFile)
c = conn.cursor()

c.execute("""create table wallpapers (location, tag1, tag2, tag3,
                                      tag4, tag5, tag6, tag7,
                                      tag8, tag9)""")

for shortFile in os.listdir(paperRootPath):
    fullFile = paperRootPath + shortFile
    c.execute("""insert into wallpapers values (?,
                                                '', '', '',
                                                '', '', '',
                                                '', '', '')""",
                                                (fullFile,))
conn.commit()
print("Testing...")
c.execute("""select * from wallpapers where ROWID=?""", (10000,))
for row in c: print(row)
