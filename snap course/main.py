import os
import exec as exc
os.chdir(os.path.dirname(__file__))

def main():
    exc.getCourse()
    exc.disconnect()

if __name__ == "__main__":
    if exc.link():
        main()
