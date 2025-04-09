import os
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
from pathlib import Path

# Function to read all CSV files in a directory
def read_csv_files(directory):
    csv_data = {}
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            file_path = os.path.join(directory, file)
            try:
                # Read CSV file
                df = pd.read_csv(file_path)
                
                # Convert date column to datetime
                date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
                if date_cols:
                    df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
                    df.set_index(date_cols[0], inplace=True)
                
                csv_data[file] = df
                print(f"Successfully loaded {file}")
            except Exception as e:
                print(f"Error loading {file}: {e}")
    
    return csv_data

# Function to create candlestick chart for price movement
def create_price_chart(data_dict, output_dir):
    for filename, df in data_dict.items():
        # Check if the dataframe has OHLC data
        required_cols = ['open', 'high', 'low', 'close']
        
        # Find columns matching OHLC data (case-insensitive)
        ohlc_cols = {}
        for req_col in required_cols:
            for col in df.columns:
                if req_col.lower() in col.lower():
                    ohlc_cols[req_col] = col
                    break
        
        if len(ohlc_cols) == 4:
            # Prepare data for mplfinance
            df_ohlc = df[[ohlc_cols[col] for col in required_cols]].copy()
            df_ohlc.columns = required_cols
            
            # Create candlestick chart
            fig, ax = plt.subplots(figsize=(12, 8))
            mpf.plot(df_ohlc, type='candle', style='yahoo', 
                     title=f'Price Movement - {Path(filename).stem}',
                     ylabel='Price', ax=ax)
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{Path(filename).stem}_price.png"))
            plt.close()
            print(f"Created price chart for {filename}")
        else:
            print(f"Cannot create price chart for {filename}: OHLC data not found")

# Function to create volume chart
def create_volume_chart(data_dict, output_dir):
    for filename, df in data_dict.items():
        # Check if the dataframe has volume data
        volume_cols = [col for col in df.columns if 'volume' in col.lower() or 'vol' in col.lower()]
        
        if volume_cols:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(df.index, df[volume_cols[0]], color='blue', alpha=0.6)
            ax.set_title(f'Volume Analysis - {Path(filename).stem}')
            ax.set_ylabel('Volume')
            ax.grid(True, alpha=0.3)
            
            # Format x-axis dates
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{Path(filename).stem}_volume.png"))
            plt.close()
            print(f"Created volume chart for {filename}")
        else:
            print(f"Cannot create volume chart for {filename}: Volume data not found")

# Function to create technical indicator chart (Moving Averages)
def create_technical_indicator_chart(data_dict, output_dir):
    for filename, df in data_dict.items():
        # Check if we have at least closing price
        close_cols = [col for col in df.columns if 'close' in col.lower() or 'price' in col.lower()]
        
        if close_cols:
            close_col = close_cols[0]
            # Calculate moving averages
            df['SMA20'] = df[close_col].rolling(window=20).mean()
            df['SMA50'] = df[close_col].rolling(window=50).mean()
            df['EMA20'] = df[close_col].ewm(span=20, adjust=False).mean()
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df.index, df[close_col], label='Close Price', color='black', alpha=0.7)
            ax.plot(df.index, df['SMA20'], label='20-day SMA', color='red', linewidth=1.5)
            ax.plot(df.index, df['SMA50'], label='50-day SMA', color='blue', linewidth=1.5)
            ax.plot(df.index, df['EMA20'], label='20-day EMA', color='green', linewidth=1.5)
            
            ax.set_title(f'Technical Analysis - {Path(filename).stem}')
            ax.set_ylabel('Price')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format x-axis dates
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{Path(filename).stem}_technical.png"))
            plt.close()
            print(f"Created technical indicator chart for {filename}")
        else:
            print(f"Cannot create technical indicator chart for {filename}: Close price data not found")

def main():
    # Ask for the directory containing CSV files
    data_directory = input("Enter the directory path containing your CSV files: ")
    
    # Create output directory for graphs
    output_directory = os.path.join(data_directory, "quant_analysis_graphs")
    os.makedirs(output_directory, exist_ok=True)
    
    # Read all CSV files in the directory
    csv_data = read_csv_files(data_directory)
    
    if not csv_data:
        print("No valid CSV files found in the specified directory.")
        return
    
    # Create the three different types of graphs
    create_price_chart(csv_data, output_directory)
    create_volume_chart(csv_data, output_directory)
    create_technical_indicator_chart(csv_data, output_directory)
    
    print(f"All graphs have been saved to {output_directory}")

if __name__ == "__main__":
    main()
