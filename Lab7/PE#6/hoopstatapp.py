from hoopstatsview import HoopStatsView
import pandas as pd

def cleanStats(df):

    target_columns = ["FG", "3PT", "FT"]  

    for col in target_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.split('-').str[0]  
            df[col] = pd.to_numeric(df[col], errors='coerce')  

    return df

def main():
    """Loads, cleans, and passes the data to the GUI."""
    frame = pd.read_csv("cleanbrogdonstats.csv")  
    frame = cleanStats(frame)  
    app = HoopStatsView(frame)  
    app.mainloop()  

if __name__ == "__main__":
    main()
    