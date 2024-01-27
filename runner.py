import os
import shutil

def main(n=10):
    print('\nExtracting receipts & data from emails...')
    os.system("python emailToCsv.py")

    print("\nCalculating price...")
    for i in range(n):
        os.system("python priceFixer.py" + ' last' if i == n-1 else '')
        if os.path.exists("new_output.csv"):
            shutil.move("new_output.csv", "output.csv")

    print('\nPlotting data...')
    os.system("python plotter.py")

if __name__ == "__main__":
    main()
