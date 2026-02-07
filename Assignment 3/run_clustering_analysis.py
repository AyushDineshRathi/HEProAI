import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def analyze_clusters():
    # 1. Load Data (Adjust path to where data actually is)
    try:
        df = pd.read_csv('../Data/students_with_scores_v2.csv')
    except Exception:
        # Fallback if running from a different root
        df = pd.read_csv('students_with_scores_v2.csv')

    print(f"Data Loaded: {len(df)} records")

    # 2. Select Features for Clustering
    # We focus on the behavioral/performance raw metrics, not the calculated scores (to avoid leakage/double counting)
    features = ['gpa', 'attendance', 'stress_level', 'mental_wellbeing', 
                'productivity_score', 'career_clarity', 'engagement_score']
    
    X = df[features]
    
    # 3. Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Clustering (K=4 to capture: High, Avg, Struggling, At-Risk/Burnout)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    df['Cluster'] = clusters
    
    # 5. Analysis
    # Calculate Mean values for each cluster
    print("\n--- Cluster Centers (Mean Values) ---")
    means = df.groupby('Cluster')[features].mean().round(2)
    print(means)
    
    # Add count
    print("\n--- Cluster Counts ---")
    print(df['Cluster'].value_counts().sort_index())
    
    # Compare with Rule-Based Risk Category
    print("\n--- Cluster vs Rule-Based Risk Category ---")
    print(pd.crosstab(df['Cluster'], df['Risk_Category']))
    
    # 6. Automate labeling (simple heuristic for the report)
    # We want to know which cluster ID corresponds to "High Performer", etc.
    # High Performer: Highest GPA/Attendance
    hp_cluster = means['gpa'].idxmax()
    print(f"\nPotential High Performer Cluster: {hp_cluster}")
    
    # At Risk: Lowest GPA/Attendance
    ar_cluster = means['gpa'].idxmin()
    print(f"Potential At-Risk Cluster: {ar_cluster}")
    
    # Career Confused: High GPA but Low Career Clarity?
    # We look for a cluster with decent GPA (>6) but low Career Clarity (<5)
    cc_cluster = means[(means['gpa'] > 6) & (means['career_clarity'] < 5)].index
    if not cc_cluster.empty:
        print(f"Potential Career-Confused Cluster: {cc_cluster[0]}")
    else:
        print("No obvious Career-Confused cluster mean found (might be mixed).")

if __name__ == "__main__":
    analyze_clusters()
