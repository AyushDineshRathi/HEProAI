import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def load_data():
    try:
        students_df = pd.read_csv('../Data/students_with_scores_v2.csv')
        mentors_df = pd.read_csv('mentors.csv')
        return students_df, mentors_df
    except FileNotFoundError:
        print("Error: specific file not found. Please ensure 'students_with_scores_v2.csv' is in '../Data/' and 'mentors.csv' is in the current directory.")
        return None, None

def perform_clustering(df):
    # Select features for clustering (same as Assignment 3)
    features = ['gpa', 'attendance', 'stress_level', 'mental_wellbeing', 
                'productivity_score', 'career_clarity', 'engagement_score']
    
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # K=4 for High Performer, Average, Struggling, At-Risk
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # Determine Cluster Labels based on mean GPA
    cluster_means = df.groupby('Cluster')['gpa'].mean()
    sorted_clusters = cluster_means.sort_values().index.tolist()
    
    # Mapping logic (simplified heuristic): 
    # Lowest GPA -> At Risk (Red)
    # Second lowest -> Struggling/Needs Support (Yellow)
    # Second highest -> Average/Good (Blue)
    # Highest GPA -> High Performer (Green)
    
    cluster_map = {
        sorted_clusters[0]: 'At Risk',
        sorted_clusters[1]: 'Struggling',
        sorted_clusters[2]: 'Average',
        sorted_clusters[3]: 'High Performer'
    }
    
    df['Cluster_Label'] = df['Cluster'].map(cluster_map)
    return df

def assign_mentor(student, mentors_df):
    cluster = student['Cluster_Label']
    stress = student['stress_level']
    career_clarity = student['career_clarity']
    
    needed_expertise = "General"
    intervention = "Regular Check-in"
    alert = "No"

    # Logic for Intervention and Expertise
    if cluster == 'At Risk':
        if stress > 7:
            needed_expertise = "Emotional Wellness"
            intervention = "Wellness Counseling + Remedial Support"
            alert = "High Risk - Immediate Attention"
        else:
            needed_expertise = "Academic Support"
            intervention = "remedial Classes & Peer Tutoring"
            alert = "Academic Alert"
            
    elif cluster == 'Struggling':
        if career_clarity < 4:
            needed_expertise = "Career Guidance"
            intervention = "Career Workshop & Academic Planning"
        else:
            needed_expertise = "Academic Support"
            intervention = "Extra Office Hours"
            
    elif cluster == 'Average':
        if career_clarity < 6:
            needed_expertise = "Career Guidance"
            intervention = "Internship Prep"
        else:
            needed_expertise = "Career Generlist" # Typo in csv, matching it
            intervention = "Skill Building"

    elif cluster == 'High Performer':
        if stress > 8:
             needed_expertise = "Emotional Wellness"
             intervention = "Stress Management for High Achievers"
             alert = "Burnout Risk"
        else:
            needed_expertise = "Advanced Research"
            intervention = "Research Projects & Mentorship"

    # Find a mentor
    # Simple matching: Find first mentor with needed expertise and capacity
    # In a real system, we'd handle load balancing more dynamically
    
    # Filter mentors by expertise
    potential_mentors = mentors_df[mentors_df['Expertise'] == needed_expertise]
    
    # If no specific match, fallback to generalist or available
    if potential_mentors.empty:
         potential_mentors = mentors_df[mentors_df['Expertise'].isin(['Career Generlist', 'Career Guidance'])]
    
    # Sort by Current_Mentees to balance load
    potential_mentors = potential_mentors.sort_values('Current_Mentees')
    
    selected_mentor = "Unassigned"
    
    if not potential_mentors.empty:
        # Check if capacity allows - simple check, in a batch process we increment
        # For this row-by-row simulation without updating the DF in place for speed, 
        # we will just pick the one with lowest current (simulated). 
        # To strictly enforce limit, we need to update the dataframe.
        
        # Let's try to update the dataframe to track count
        best_mentor_idx = potential_mentors.index[0]
        if mentors_df.at[best_mentor_idx, 'Current_Mentees'] < mentors_df.at[best_mentor_idx, 'Max_Mentees']:
             selected_mentor = mentors_df.at[best_mentor_idx, 'Name']
             mentors_df.at[best_mentor_idx, 'Current_Mentees'] += 1
        else:
             selected_mentor = "Waitlist (Capacity Full)"
    
    return [selected_mentor, intervention, alert]

def main():
    print("Loading data...")
    students_df, mentors_df = load_data()
    if students_df is None:
        return

    print("Clustering students...")
    students_df = perform_clustering(students_df)
    
    print("Matching mentors and generating recommendations...")
    # Apply matching logic
    recommendations = []
    
    for i, student in students_df.iterrows():
        matches = assign_mentor(student, mentors_df)
        recommendations.append(matches)
        
    recommendations_df = pd.DataFrame(recommendations, columns=['Assigned_Mentor', 'Intervention', 'Alert_Status'])
    
    # Reset index to ensure alignment (though iterrows and append preserve order, explicit reset is safer)
    students_df = students_df.reset_index(drop=True)
    recommendations_df = recommendations_df.reset_index(drop=True)
    
    # Combine results
    final_df = pd.concat([students_df[['student_id', 'gpa', 'Cluster_Label']], recommendations_df], axis=1)
    
    # Save results
    final_df.to_csv('recommendations.csv', index=False)
    mentors_df.to_csv('mentors_updated.csv', index=False)
    
    print("\n--- Matching Complete ---")
    print(f"Recommendations saved to 'recommendations.csv'")
    print(f"Updated mentor capacity saved to 'mentors_updated.csv'")
    
    print("\n--- Alerts Simulation ---")
    high_risk = final_df[final_df['Alert_Status'] != 'No']
    print(f"Total Alerts Triggered: {len(high_risk)}")
    print(high_risk.head(10))

if __name__ == "__main__":
    main()
