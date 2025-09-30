import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import math
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Scientific Correlation Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e86ab;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- CORE ANALYSIS FUNCTIONS (Unchanged) ---

def generate_plot(df, x_col, y_col, r_value):
    """Generates a scatter plot and returns the path to the saved image."""
    chart_filename = f'plot_{x_col}_vs_{y_col}.png'
    
    plt.figure(figsize=(8, 5))
    plt.scatter(df[x_col], df[y_col], alpha=0.5, color='darkred')
    plt.title(f'Scatter Plot: {x_col} vs. {y_col} (r = {r_value})', fontsize=14)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    plt.savefig(chart_filename)
    plt.close()
    return chart_filename

def perform_analysis(df, x_col, y_col):
    """Performs correlation, generates plot, and creates enhanced interpretation."""
    
    # 1. Numeric Output: Correlation
    # Use pandas correlation function
    correlation_r = df[x_col].corr(df[y_col])
    
    # 2. Small Table: First 5 rows (pd.head)
    small_table_df = df[[x_col, y_col]].head(5) 

    # 3. Chart/Scatter Plot
    plot_path = generate_plot(df, x_col, y_col, correlation_r.round(4))
    
    # 4. Enhanced Interpretation (Using ReportLab <b> and Unicode for R-squared)
    r_sq = correlation_r**2
    r_abs = abs(correlation_r)
    
    # --- Strength Evaluation ---
    if r_abs >= 0.7:
        strength = "strong"
        linearity = f"This relationship is highly linear, with the X-feature explaining {r_sq:.1%} (R²) of the variance in {y_col}."
    elif r_abs >= 0.3:
        strength = "moderate"
        linearity = f"This relationship shows moderate linearity, accounting for {r_sq:.1%} (R²) of the variance in {y_col}. Other non-linear or external factors likely play a significant role."
    else:
        strength = "weak or negligible"
        linearity = f"The fit is poor, explaining only {r_sq:.1%} of the variance. The data suggests a non-linear relationship, no significant relationship, or that the feature is a poor predictor."
        
    # --- Direction Evaluation ---
    if correlation_r > 0:
        direction = "positive (increasing)"
        direction_phrase = f"This means that as {x_col} increases, {y_col} also tends to increase."
    elif correlation_r < 0:
        direction = "negative (decreasing)"
        direction_phrase = f"This means that as {x_col} increases, {y_col} tends to decrease."
    else:
        direction = "no discernable linear"
        direction_phrase = "There is no clear linear tendency in the data."
        
    interpretation = (
        f"The analysis revealed {strength} {direction} linear relationship (r = {correlation_r:.4f}) between {x_col} and {y_col}. "
        f"{direction_phrase} {linearity}"
    )
    
    return small_table_df, correlation_r.round(4), plot_path, interpretation, strength, direction, r_sq

# --- PDF GENERATION FUNCTION (Unchanged) ---

def generate_report(df, y_feature):
    """
    Iterates through all suitable columns (X) against the Y feature, performs analysis,
    and compiles all results into a single PDF report.
    """
    
    # --- ROBUST FILTERING ---
    # Initialization of x_features is critical to avoid the NameError
    all_numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    x_features = [] # <--- THIS IS THE FIX for the NameError
    
    for col in all_numeric_cols:
        if col == y_feature:
            continue
            
        # 1. Filter common ID columns (spurious correlation)
        if col.lower() in ['id', 'observationid', 'rowid', 'index']:
            continue
            
        # 2. Filter constant columns (zero variance)
        if df[col].std() < 1e-6:
             continue
             
        x_features.append(col)
    
    if not x_features:
        st.error(f"No suitable numeric X features found to compare against {y_feature}. Check your CSV.")
        return None

    # --- PDF Report Setup ---
    pdf_filename = 'Comprehensive_Scientific_Report.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title Page/Executive Summary Intro
    story.append(Paragraph("Comprehensive Scientific Analysis Report", styles['Title']))
    story.append(Spacer(1, 12))
    # Using <b> for bolding the Y_feature in the title
    story.append(Paragraph(f"Dependent Variable: <b>{y_feature}</b>", styles['h1']))
    story.append(Spacer(1, 24))
    
    # Loop through each valid X feature
    for x_col in x_features:
        try:
            small_table_df, r_value, plot_path, interpretation, strength, direction, r_sq = perform_analysis(df, x_col, y_feature)

            # --- Add Section Header ---
            story.append(Paragraph(f"Section: Relationship between {x_col} and {y_feature}", styles['h2']))
            story.append(Spacer(1, 6))

            # --- Add Interpretation (Requested detailed explanation) ---
            story.append(Paragraph("Interpretation of Findings (Direction and Linearity):", styles['h3']))
            story.append(Paragraph(interpretation, styles['Normal']))
            story.append(Spacer(1, 12))
            
            # --- ADD NATIVE REPORTLAB TABLE (FIX for strange appearance) ---
            story.append(Paragraph("Numeric Output (Sample Data Head):", styles['h3']))
            
            # Convert DataFrame to list of lists (including header row)
            # Rounding data for cleaner presentation in the table
            table_data = [small_table_df.columns.tolist()] + small_table_df.values.round(2).tolist()
            
            # Create the Table object
            table = Table(table_data)
            
            # Apply styling for a professional look
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 12))

            # --- Add Chart/Scatter Plot ---
            story.append(Paragraph(f"Visualization ($r = {r_value}$):", styles['h3']))
            story.append(Image(plot_path, width=400, height=250))
            
            # --- NEW: Add a specific explanatory caption below the plot ---
            caption = f"Figure 1.{x_features.index(x_col) + 1}: Scatter plot illustrating the relationship between {x_col} and {y_feature}. The data points confirm the calculated correlation of $r = {r_value}$."
            # Using the 'Italic' style for a standard caption look
            story.append(Paragraph(caption, styles['Italic']))
            # --- END NEW ---
            
            story.append(Spacer(1, 24))

        except Exception as e:
            # Report the error to the console and in the PDF
            story.append(Paragraph(f"Analysis Failed for {x_col}: {e}", styles['Normal'])) 
            story.append(Spacer(1, 12))
            
    doc.build(story)
    return pdf_filename

def create_download_link(file_path, link_text):
    """Create a download link for files"""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/pdf;base64,{b64}" download="{file_path}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">{link_text}</a>'
    return href

def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 Scientific Correlation Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    st.sidebar.header("📁 Data Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=['csv'])
    
    # Sample data creation option
    if st.sidebar.checkbox("Use Sample Data", value=True):
        if not pd.io.common.file_exists('sample_quantitative_data.csv'):
            st.sidebar.info("Creating sample dataset...")
            N = 100
            np.random.seed(42)
            load_time = np.random.normal(loc=3.5, scale=1.0, size=N)
            load_time = np.clip(load_time, 1.5, 6.0)

            base_satisfaction = 90 - (load_time * 5)
            satisfaction_score = base_satisfaction + np.random.normal(loc=0, scale=8, size=N)
            satisfaction_score = np.clip(satisfaction_score, 50, 100).astype(int)

            data = pd.DataFrame({
                'ObservationID': range(1, N + 1),
                'LoadTime_s': load_time,
                'SatisfactionScore_100': satisfaction_score,
                'ConstantFeature': np.full(N, 10), # Will be filtered out due to low variability
                'RandomNoise': np.random.rand(N) * 10 
            })
            data.to_csv('sample_quantitative_data.csv', index=False)
        
        data_df = pd.read_csv('sample_quantitative_data.csv')
        data_df.dropna(inplace=True)
        st.sidebar.success("Sample data loaded successfully!")
        
    elif uploaded_file is not None:
        data_df = pd.read_csv(uploaded_file)
        data_df.dropna(inplace=True)
        st.sidebar.success("Uploaded data loaded successfully!")
    else:
        st.info("Please upload a CSV file or use the sample data to begin analysis.")
        return
    
    # Display dataset info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(data_df))
    with col2:
        st.metric("Total Columns", len(data_df.columns))
    with col3:
        numeric_cols = len([col for col in data_df.columns if pd.api.types.is_numeric_dtype(data_df[col])])
        st.metric("Numeric Columns", numeric_cols)
    
    # Target variable selection
    numeric_columns = [col for col in data_df.columns if pd.api.types.is_numeric_dtype(data_df[col])]
    y_feature = st.sidebar.selectbox(
        "Select Target Variable (Y)",
        numeric_columns,
        index=numeric_columns.index('SatisfactionScore_100') if 'SatisfactionScore_100' in numeric_columns else 0
    )
    
    # Data preview
    st.markdown('<div class="section-header">📋 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(data_df.head(), use_container_width=True)
    
    # Analysis section
    st.markdown('<div class="section-header">📊 Correlation Analysis</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Run Comprehensive Analysis", type="primary"):
        with st.spinner("Performing correlation analysis and generating insights..."):
            
            # Get suitable features
            all_numeric_cols = [col for col in data_df.columns if pd.api.types.is_numeric_dtype(data_df[col])]
            x_features = []
            
            for col in all_numeric_cols:
                if col == y_feature:
                    continue
                if col.lower() in ['id', 'observationid', 'rowid', 'index']:
                    continue
                if data_df[col].std() < 1e-6:
                    continue
                x_features.append(col)
            
            if not x_features:
                st.error(f"No suitable numeric X features found to compare against {y_feature}.")
                return
            
            progress_bar = st.progress(0)
            results = []
            
            for i, x_col in enumerate(x_features):
                progress_bar.progress((i + 1) / len(x_features))
                
                small_table_df, r_value, plot_path, interpretation, strength, direction, r_sq = perform_analysis(data_df, x_col, y_feature)
                
                results.append({
                    'feature': x_col,
                    'correlation': r_value,
                    'r_squared': r_sq,
                    'strength': strength,
                    'direction': direction,
                    'interpretation': interpretation,
                    'plot_path': plot_path,
                    'sample_data': small_table_df
                })
            
            # Display results
            for i, result in enumerate(results):
                st.markdown(f"### 🔍 Analysis: {result['feature']} vs {y_feature}")
                
                # Create columns for metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    # Color code based on correlation strength
                    corr_color = "green" if abs(result['correlation']) > 0.7 else "orange" if abs(result['correlation']) > 0.3 else "red"
                    st.metric("Correlation (r)", f"{result['correlation']:.4f}", delta=None, delta_color="normal")
                
                with col2:
                    st.metric("R-squared", f"{result['r_squared']:.4f}")
                
                with col3:
                    st.metric("Strength", result['strength'].title())
                
                with col4:
                    direction_icon = "📈" if result['correlation'] > 0 else "📉" if result['correlation'] < 0 else "➡️"
                    st.metric("Direction", f"{direction_icon} {result['direction'].title()}")
                
                # Interpretation
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.write("**Interpretation:**", result['interpretation'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Sample data and plot
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.write("**Sample Data (First 5 rows):**")
                    st.dataframe(result['sample_data'], use_container_width=True)
                
                with col_right:
                    st.write("**Scatter Plot:**")
                    st.image(result['plot_path'], use_container_width=True)
                
                st.markdown("---")
            
            # Generate PDF report
            st.markdown('<div class="section-header">📄 Report Generation</div>', unsafe_allow_html=True)
            
            with st.spinner("Generating comprehensive PDF report..."):
                pdf_filename = generate_report(data_df, y_feature)
                
                if pdf_filename:
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("✅ PDF report generated successfully!")
                    st.markdown(create_download_link(pdf_filename, "📥 Download Comprehensive Report"), unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':

    main()
