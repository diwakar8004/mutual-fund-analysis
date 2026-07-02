# recommender.py
import pandas as pd
import numpy as np

def run_fund_recommender(user_appetite):
    """
    Inputs: user_appetite string ('Low', 'Moderate', 'High')
    Outputs: Top 3 recommendation recommendations filtered by Sharpe limits
    """
    # Load scorecard data generated in previous modules
    try:
        scorecard = pd.read_csv("fund_scorecard.csv")
    except FileNotFoundError:
        # Fallback framework generation if local storage links mismatch
        print("Pre-existing fund_scorecard.csv not found. Running dynamic recommender lookup simulation...")
        funds = [f"Scheme_{i:02d}" for i in range(1, 41)]
        np.random.seed(10)
        scorecard = pd.DataFrame({
            "Fund": funds,
            "Sharpe_Ratio": np.random.uniform(0.4, 2.1, 40),
            "Risk_Grade": np.random.choice(["Low", "Moderate", "High"], 40)
        })
    
    # Normalize character formatting matching
    scorecard['Risk_Grade'] = scorecard['Risk_Grade'].str.capitalize()
    target_risk = str(user_appetite).capitalize()
    
    if target_risk not in ["Low", "Moderate", "High"]:
        return "Invalid input profile selection. Choose either 'Low', 'Moderate', or 'High'."
    
    # Isolate targets matching threshold parameters
    subset = scorecard[scorecard['Risk_Grade'] == target_risk]
    top_3 = subset.nlargest(3, "Sharpe_Ratio")
    
    print(f"\n=========================================")
    print(f" BLUESTOCK ALGO-RECOMMENDER: {target_risk.upper()} RISK PROFILE")
    print(f"=========================================")
    print(top_3[["Fund", "Sharpe_Ratio", "Risk_Grade"]].to_string(index=False))
    print("=========================================\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_fund_recommender(sys.argv[1])
    else:
        # Fallback profile evaluation run
        run_fund_recommender("Moderate")