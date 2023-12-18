import os
import shutil

def main(n=5):
    print('\nExtracting receipts & data from emails...')
    os.system("python emailToCsv.py")

    print("\nCalculating price...")
    for i in range(n):
        os.system(f"python priceFixer.py")
        shutil.move("output.csv", f"output-{i}.csv")
        shutil.move("new_output.csv", "output.csv")

    print('\nPlotting data...')
    os.system("python plotter.py")

if __name__ == "__main__":
    main()
