Wallpaper-Changer
=================

Changes wallpapers pseudo-randomly with options for picture navigation. Unless your file system mirrors mine, be prepared to edit the known location of the pictures/picture database.

Requires sqlite3 for python.
Requires idesktop and feh for linux.

This program requires a database of all the wallpapers in the rotation.
The Directory_to_DB.py file can be used to create the database, just edit the file locations in the program.
A blank text file called "command.txt" is also required in the idesktop folder in the home directory.
idesktop can be used to create icons on the desktop which once clicked will have the effect of writing to command.txt.
The program understands "remove" which appends the current wallpaper to a list of files to be taken out of rotation.
"prev" and "next" are also understood to move the program within the rotation of pictures without waiting for a time limit.

Once the program has what it needs to begin, it can be run in the background through the .xinitrc file with a command like "python scripts/wallpaper.py &".
