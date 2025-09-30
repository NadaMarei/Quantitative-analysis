# 🔬 Scientific Correlation Analyzer

A powerful, user-friendly Streamlit application for comprehensive correlation analysis and scientific reporting. Analyze relationships between variables in your dataset and generate detailed PDF reports with professional visualizations.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)

## ✨ Features

### 📊 **Interactive Analysis**
- **Real-time correlation calculations** with Pearson's r and R² values
- **Automated strength assessment** (strong, moderate, weak relationships)
- **Direction analysis** (positive/negative correlations)
- **Interactive scatter plots** for visual relationship exploration

### 📁 **Flexible Data Input**
- **Upload your own CSV files** or use built-in sample data
- **Smart data preprocessing** with automatic handling of missing values
- **Intelligent column filtering** to exclude IDs and constant variables
- **Real-time data preview** before analysis

### 📄 **Professional Reporting**
- **Comprehensive PDF reports** with detailed interpretations
- **Professional formatting** using ReportLab
- **Sample data tables** and statistical summaries
- **Automated chart inclusion** with explanatory captions

### 🎨 **User Experience**
- **Modern, responsive interface** with custom styling
- **Progress indicators** for long-running operations
- **One-click analysis** with intuitive controls
- **Download-ready reports** with direct PDF generation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <your-repo-url>
   cd scientific-correlation-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in your terminal

## 📖 How to Use

### Step 1: Data Input
- **Option A**: Use the built-in sample data (recommended for first-time users)
- **Option B**: Upload your own CSV file using the sidebar file uploader

### Step 2: Configure Analysis
- Select your **target variable (Y)** from the dropdown menu
- Review the data preview to ensure proper loading

### Step 3: Run Analysis
- Click the **"Run Comprehensive Analysis"** button
- Watch real-time progress as each variable is analyzed

### Step 4: Explore Results
- View **correlation metrics** for each variable pair
- Examine **scatter plots** visualizing relationships
- Read **detailed interpretations** of each correlation

### Step 5: Generate Report
- Download a **comprehensive PDF report** with all findings
- Share professional-quality reports with stakeholders

## 📊 Sample Data

The application includes built-in sample data demonstrating:
- **LoadTime_s**: Website loading times (seconds)
- **SatisfactionScore_100**: User satisfaction scores (0-100 scale)
- **ObservationID**: Unique identifier (automatically filtered out)
- **RandomNoise**: Random data for comparison

## 🛠 Technical Details

### Analysis Methodology
- **Correlation Calculation**: Pearson's correlation coefficient (r)
- **Strength Classification**:
  - Strong: |r| ≥ 0.7
  - Moderate: 0.3 ≤ |r| < 0.7
  - Weak: |r| < 0.3
- **Variance Explanation**: R-squared (R²) calculation
- **Statistical Filtering**: Automatic exclusion of non-informative columns

### Supported Data Types
- ✅ Numeric variables (integer, float)
- ✅ CSV file format
- ✅ Mixed-type datasets (automatically filters numeric columns)

### Output Features
- **Interactive metrics** with color-coded strength indicators
- **Professional scatter plots** with correlation annotations
- **Sample data tables** showing first 5 rows
- **Detailed interpretations** in plain language
- **PDF reports** with academic-quality formatting

## 📁 Project Structure

```
scientific-correlation-analyzer/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── sample_quantitative_data.csv  # Auto-generated sample data
└── Comprehensive_Scientific_Report.pdf  # Generated reports
```

## 🔧 Customization

### Adding New Analysis Types
The modular architecture makes it easy to extend:
```python
# Add new analysis functions following the existing pattern
def perform_custom_analysis(df, x_col, y_col):
    # Your custom analysis here
    return results
```

### Modifying Styling
Customize the appearance by editing the CSS in `app.py`:
```python
st.markdown("""
<style>
    .your-custom-class {
        /* Your custom styles */
    }
</style>
""", unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### Common Issues

**"No suitable numeric X features found"**
- Ensure your CSV contains numeric columns beyond the target variable
- Check that columns have sufficient variability (not constant values)

**"File not found" errors**
- Verify CSV file path and permissions
- Ensure file is not open in another program

**Memory issues with large datasets**
- Consider sampling your data before analysis
- Remove unnecessary columns to reduce memory footprint

### Getting Help
1. Check the console for detailed error messages
2. Verify your CSV format and data types
3. Ensure all dependencies are properly installed

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New features
- Documentation improvements
- Performance enhancements

**Ready to uncover insights in your data?** Launch the app and start exploring correlations today! 🚀
