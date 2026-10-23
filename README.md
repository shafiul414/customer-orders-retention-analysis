# Customer Orders and Retention Analysis

A beginner-friendly data analytics portfolio project using **Python, pandas, SQLite SQL, Matplotlib, Jupyter Notebook, Streamlit, and Plotly** to explore order outcomes, delivered sales, repeat purchasing, sales channels, and city-level performance.

> **Dataset disclaimer:** All records in this repository are synthetic practice data generated for learning. They do not represent real customers, a real company, or verified business performance. Monetary figures are shown in unspecified sample currency units, not BDT.

## Business questions

- How many orders were delivered, returned, or cancelled?
- Which product categories had the highest delivered sales?
- How did delivered sales change month by month?
- How common were repeat delivered purchases in the sample?
- Which sales channels and cities had the most orders or delivered sales?

## Tools and skills demonstrated

- **Python** for data analysis and workflow automation
- **pandas** for loading, cleaning, joining, grouping, and summarizing data
- **SQLite SQL** for querying order data and aggregating results
- **Matplotlib** for charts
- **Jupyter Notebook** for documenting a reproducible analysis
- Basic data cleaning, aggregation, exploratory data analysis, and business interpretation

## Project structure

```text
customer_orders_retention_analysis/
├── Customer_Orders_and_Retention_Analysis.ipynb
├── app.py
├── README.md
├── requirements.txt
└── data/
    ├── customers.csv
    ├── orders.csv
    └── products.csv
```

## Key findings from the included sample data

- **Orders:** 1,000 total; 789 delivered (78.9%), 125 returned (12.5%), and 86 cancelled (8.6%).
- **Top category by delivered sales:** Furniture, with 1,252,730 sample currency units.
- **Best month by delivered sales:** February 2025, with 330,983.50 sample currency units.
- **City:** Dhaka had the highest delivered sales among the cities in the sample.
- **Channel:** Website had the largest number of orders.
- **Repeat purchasing:** 95.5% of customers with at least one delivered order had two or more delivered orders in this synthetic sample. This unusually high share is a property of the practice data and is not a real-world benchmark.

These findings describe only the included synthetic dataset. They should not be presented as results from a real business.

## Interactive Streamlit dashboard

The project includes `app.py`, an interactive dashboard with:

- Date, city, channel, and category filters
- KPI cards for orders, delivered sales, delivery rate, return rate, and repeat-customer share
- Interactive charts for order outcomes, monthly delivered sales, category performance, and city performance
- Channel and category risk tables
- A profitability-improvement scenario simulator
- A filtered-data CSV download

### Run the dashboard on Windows

1. Install Python if it is not already installed.
2. Extract or clone the repository and open Command Prompt in the project folder (the folder containing `app.py`).
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

5. Streamlit should open the dashboard in your browser. If it does not, use the local URL printed in Command Prompt.

### Profitability analysis: important limitation

The scenario simulator is illustrative only. The dataset contains order values and statuses, but not unit costs, shipping/fulfilment costs, marketing spend, payment fees, or return-handling costs. Therefore, the project cannot calculate actual profit or prove that a strategy will increase profit. The simulator uses an adjustable assumed gross margin and average delivered order value to help demonstrate how an analyst could explore scenarios. Replace assumptions with verified business data before making decisions.

## How to run the notebook

1. Install Python. Jupyter can be installed directly or through Anaconda.
2. Download or clone this repository and keep the `data` folder alongside the notebook.
3. Open a terminal in the project folder.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

6. Open `Customer_Orders_and_Retention_Analysis.ipynb`.
7. Run the notebook cells from top to bottom.

## Suggested next improvements

- Add data-quality checks for missing values, duplicate order IDs, and invalid quantities or prices.
- Compare calculated order values with the provided order values and investigate any differences.
- Add a return/cancellation rate chart by category and sales channel.
- When working with a real dataset, document the source, definitions, time period, and any privacy protections.

## GitHub publishing checklist

- [ ] Upload `app.py`, the notebook, `README.md`, `requirements.txt`, and all three CSV files in `data/`.
- [ ] Confirm the notebook opens and the charts/results are visible.
- [ ] Test the dashboard locally with `streamlit run app.py`.
- [ ] Keep the synthetic-data disclaimer in the README.
- [ ] Do not upload passwords, API keys, tokens, or private customer information.
- [ ] Add the repository link to your CV or portfolio after publishing.
