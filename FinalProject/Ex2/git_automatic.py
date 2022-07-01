##### version 0.1 #####

# A script that pushes things to GitHub every 5 seconds

from git import Repo
import time
import os

def git_push():
    # From the FlatSatChallenge, a function to automatically upload to GitHub
    try:
        repo = Repo('/home/nicom26/AstroBeever') #TODO: MAKE SURE TO REPLACE "nicom26" you YOUR username
        repo.git.add('/home/nicom26/AstroBeever') #TODO: SAME THING HERE
        repo.index.commit('New Commit')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')

while True:
    cmd = 'git pull'
    os.system(cmd)
    git_push()
    print()
    time.sleep(5)
    
