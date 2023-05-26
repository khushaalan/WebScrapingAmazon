import os

def git_push():
    os.system('git status')
    os.system('git add -A')
    os.system('git commit -m "update"')
    os.system('git push origin main')

git_push()
