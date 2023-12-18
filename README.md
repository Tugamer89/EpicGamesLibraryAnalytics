# Epic Games Data Analyzer

A Python script that makes it easy to analyze the receipts received from Epic Games. Automatically extracts data from your game library and creates an easily searchable CSV file. The project also includes tools to generate interactive graphs that provide in-depth insights.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tuononen/epic-games-data-analyzer.git
   cd epic-games-data-analyzer
   ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Place your Epic Games receipts emails (.eml files) in the `emls` folder.
2. Run the `runner.py` script:
    ```bash
    python runner.py
    ```
    This script performs the following tasks:
    - Extracts receipts and data from emails (`emailToCsv.py`).
    - Calculates the price and creates multiple CSV files (`priceFixer.py`).
    - Generates insightful plots based on the extracted data (`plotter.py`).
3. Find the results in the `output.csv` file and the generated plots in the `images` folder.

## Additional Details
- `emailToCsv.py`: Processes Epic Games emails, extracts HTML content, and converts it into a CSV file (output.csv).
- `priceFixer.py`: Fixes and updates prices using web scraping and Google search queries. Please note that this process might take a considerable amount of time as it involves making one or two requests to Google for games with null prices (e.g., free games or games without the price in the receipt). Note: Be mindful of potential rate limiting or restrictions imposed by Google on automated queries.
- `plotter.py`: Creates various plots, including price trends over time, average prices by month, average prices by distributor, distributors over time, and the number of orders over time.

Feel free to contribute or provide feedback!

## Disclaimer
This tool is for personal use, and usage may be subject to Epic Games' terms and conditions. Use responsibly.
