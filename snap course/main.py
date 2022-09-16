import os
import exec as exc
os.chdir(os.path.dirname(__file__))

def main():
    exc.getCourse()
    exc.disconnect()

if __name__ == "__main__":
    #version = '1.0.0@142441'
    #Time = 'Sat Jun  5 01:55:02 2021'
    if exc.link():
        main()
