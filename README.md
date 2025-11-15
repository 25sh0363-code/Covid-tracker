# 🦠 COVID-19 Data Tracker

Interactive visualization of global and regional pandemic trends

## 📌 Project Summary

The COVID-19 Data Tracker is a dynamic dashboard that visualizes pandemic trends across countries and regions. Built with Python and Streamlit, it allows users to explore daily cases, deaths, and recoveries through interactive charts and maps.

## 🎯 Key Features

- **Country Dashboard** - Real-time metrics with tabbed interface (Graphics, Table Data, Chart Data)
- **Daily Metrics** - Visualize daily confirmed cases, deaths, and recoveries by country
- **Country Comparisons** - Compare trends across multiple countries with population normalization
- **Interactive Charts** - Line graphs, bar charts with zoom and hover tooltips
- **Global Maps** - Choropleth maps showing case density and mortality rates over time
- **Live Updates** - Auto-refresh to get latest data
- **Data Export** - Download data as CSV

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Programming | Python 3.8+ |
| Data Handling | Pandas |
| Visualization | Plotly |
| Web Interface | Streamlit |
| Data Sources | Our World in Data, Johns Hopkins University |

## 📊 Data Sources

- **Our World in Data (OWID)**: Global COVID-19 statistics including cases, deaths, testing, and vaccinations
- **Johns Hopkins University**: Time-series data for confirmed cases, deaths, and recoveries by country

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/covid-19-tracker.git
cd covid-19-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to:
```
http://localhost:8501
```

## 📁 Project Structure

```
covid-19-tracker/
├── app.py                 # Main Streamlit application
├── data_fetcher.py        # Data loading and processing
├── visualizations.py      # Chart and visualization functions
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## 🎨 Features in Detail

### Country Dashboard
- Select any country to view detailed statistics
- Real-time metric cards showing:
  - Total cases with daily change
  - Total deaths with daily change
  - Case fatality rate
  - Cases per 100K population

### Three Data Views
1. **Graphics Tab** - Interactive line charts and visualizations
2. **Table Data Tab** - Sortable data table with download option
3. **Chart Data Tab** - Multiple chart types for analysis

### Data Refresh
- Click "Refresh Data" button in sidebar to fetch latest statistics
- Data is cached for performance

## 💾 Data Features

- Automatic data fetching from Our World in Data
- Local caching for faster loading
- CSV export functionality
- Population-normalized comparisons

## 🔮 Future Enhancements

- [ ] Add vaccination tracking data
- [ ] Regional breakdowns within countries
- [ ] Predictive modeling for trend forecasting
- [ ] Custom report generation
- [ ] Multi-language support
- [ ] Mobile-responsive design

## 📈 Results & Impact

- Provides real-time insights into pandemic trends
- Empowers users to explore data independently
- Supports public health awareness and education
- Accessible and user-friendly interface

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- Data provided by Our World in Data and Johns Hopkins University
- Built with Streamlit and Plotly
