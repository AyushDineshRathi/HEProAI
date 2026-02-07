
import pandas as pd
import numpy as np

# --- HELPER FUNCTIONS FOR NORMALIZATION ---
def normalize_1_to_10(val):
    """Converts 1-10 scale to 0-100"""
    # Ensure val is numeric
    return val * 10

def invert_1_to_10(val):
    """Inverts 1-10 scale (where 10 is bad) to 0-100 (where 100 is good)"""
    return (10 - val) * 10

def normalize_sleep(hours):
    """Normalizes sleep. 8 hours = 100%. Caps at 100%."""
    # Assuming hours can be float
    score = (hours / 8.0) * 100
    return min(score, 100.0)

# --- SCORING FUNCTIONS ---

def calculate_aps(row):
    # APS = 60% GPA + 20% Assignments + 20% Attendance
    gpa_norm = normalize_1_to_10(row['gpa'])
    aps = (gpa_norm * 0.60) + \
          (row['assignments_completion'] * 0.20) + \
          (row['attendance'] * 0.20)
    return round(aps, 1)

def calculate_wws(row):
    # WWS = 40% Wellbeing + 30% Sleep + 30% Low Stress
    wellbeing_norm = normalize_1_to_10(row['mental_wellbeing'])
    stress_score = invert_1_to_10(row['stress_level'])
    sleep_score = normalize_sleep(row['sleep_hours'])
    
    wws = (wellbeing_norm * 0.40) + \
          (sleep_score * 0.30) + \
          (stress_score * 0.30)
    return round(wws, 1)

def calculate_ptms(row):
    # PTMS = 50% Productivity + 30% Low Distractions + 20% Platform Engagement
    prod_norm = normalize_1_to_10(row['productivity_score'])
    distraction_score = invert_1_to_10(row['distractions'])
    
    ptms = (prod_norm * 0.50) + \
           (distraction_score * 0.30) + \
           (row['engagement_score'] * 0.20)
    return round(ptms, 1)

def calculate_crs(row):
    # CRS = 50% Career Clarity + 50% Skill Readiness
    clarity_norm = normalize_1_to_10(row['career_clarity'])
    skill_norm = normalize_1_to_10(row['skill_readiness'])
    
    crs = (clarity_norm * 0.50) + (skill_norm * 0.50)
    return round(crs, 1)

def classify_student(sri):
    if sri >= 80: return 'Green'   # Excellent
    elif sri >= 60: return 'Blue'  # Good
    elif sri >= 40: return 'Yellow' # Warning
    else: return 'Red'             # Critical

def run_scoring_pipeline():
    print("Loading students_v2.csv...")
    try:
        # Load from Assignment 1 directory to be safe, or local if copied
        # Assuming script is run in Assignment 2 dir, and data is in Assignment 1
        # adjusting path to be relative or absolute based on known structure
        try:
            df = pd.read_csv('../Data/students_v2.csv')
        except FileNotFoundError:
            df = pd.read_csv('../Data/students_v2.csv')
            
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print(f"Loaded {len(df)} records.")

    # 1. Calculate Individual Component Scores
    df['APS'] = df.apply(calculate_aps, axis=1)
    df['WWS'] = df.apply(calculate_wws, axis=1)
    df['PTMS'] = df.apply(calculate_ptms, axis=1)
    df['CRS'] = df.apply(calculate_crs, axis=1)

    # 2. Calculate Master Index (SRI)
    # Formula: 0.3 APS + 0.25 WWS + 0.20 PTMS + 0.25 CRS
    df['SRI'] = (df['APS'] * 0.30) + \
                (df['WWS'] * 0.25) + \
                (df['PTMS'] * 0.20) + \
                (df['CRS'] * 0.25)
    df['SRI'] = df['SRI'].round(1)

    # 3. Categorize
    df['Risk_Category'] = df['SRI'].apply(classify_student)
    
    # 4. Validation Checks
    print("\n--- Validation Checks ---")
    
    # Check 1: Burnout (High Stress, Low Productivity)
    burnout_cases = df[(df['stress_level'] >= 8) & (df['productivity_score'] <= 4)]
    print(f"Burnout Cases (Stress>=8, Prod<=4): {len(burnout_cases)}")
    if not burnout_cases.empty:
        print(burnout_cases[['student_id', 'stress_level', 'productivity_score', 'Risk_Category']].head())

    # Check 2: Drifter (High GPA, Low Career Clarity)
    drifter_cases = df[(df['gpa'] >= 8.0) & (df['career_clarity'] <= 4)]
    print(f"Drifter Cases (GPA>=8.0, Career<=4): {len(drifter_cases)}")
    if not drifter_cases.empty:
        print(drifter_cases[['student_id', 'gpa', 'career_clarity', 'CRS', 'Risk_Category']].head())
        
    # Check 3: Grinder (Low GPA, High Engagement)
    grinder_cases = df[(df['gpa'] <= 6.0) & (df['engagement_score'] >= 80)]
    print(f"Grinder Cases (GPA<=6.0, Eng>=80): {len(grinder_cases)}")
    if not grinder_cases.empty:
        print(grinder_cases[['student_id', 'gpa', 'engagement_score', 'APS', 'Risk_Category']].head())

    # Export
    output_path = '../Data/students_with_scores_v2.csv'
    df.to_csv(output_path, index=False)
    print(f"\nSaved scored dataset to {output_path}")

if __name__ == "__main__":
    run_scoring_pipeline()
