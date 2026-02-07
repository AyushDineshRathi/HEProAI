import pandas as pd
import numpy as np
import random

def generate_balanced_dataset(num_students=500):
    data = []
    programs = ['B.Tech', 'BCA', 'B.Sc', 'MBA']
    
    # Target Ratios to fix the bias
    # 10% Red (Critical), 30% Yellow (Warning), 40% Blue (Good), 20% Green (Excellent)
    counts = {
        'Red': int(num_students * 0.10),
        'Yellow': int(num_students * 0.30),
        'Blue': int(num_students * 0.40),
        'Green': int(num_students * 0.20)
    }
    
    current_counts = {'Red': 0, 'Yellow': 0, 'Blue': 0, 'Green': 0}
    
    for i in range(1, num_students + 1):
        s_id = f"S{i:03d}"
        program = random.choice(programs)
        semester = random.randint(1, 8)
        base_age = 18 if program != 'MBA' else 22
        age = base_age + (semester // 2)
        
        # Determine which bucket to fill
        # We look for a bucket that isn't full yet
        available_buckets = [k for k, v in current_counts.items() if v < counts[k]]
        if available_buckets:
            bucket = random.choice(available_buckets)
        else:
            bucket = 'Blue' # Fallback
            
        current_counts[bucket] += 1
        
        # --- GENERATE DATA BASED ON BUCKET ---
        
        if bucket == 'Red': # CRITICAL FAILURE (The "Dropout Risk")
            gpa = random.uniform(2.0, 5.0)           # Fails
            attendance = random.uniform(10, 60)      # Absent
            assign_comp = random.uniform(0, 40)      # No work submitted
            stress = random.randint(7, 10)           # High Stress
            sleep = random.uniform(3, 5)             # No Sleep
            wellbeing = random.randint(1, 4)         # Crisis
            prod_score = random.randint(1, 3)
            distractions = random.randint(8, 10)     # High distraction
            career = random.randint(1, 3)            # Lost
            skill = random.randint(1, 3)
            engagement = random.uniform(0, 30)       # Ghosting the platform
            
        elif bucket == 'Yellow': # WARNING SIGNS (The "Struggler")
            gpa = random.uniform(5.0, 7.0)           # Passing but low
            attendance = random.uniform(60, 75)      # Irregular
            assign_comp = random.uniform(50, 70)     # Late submissions
            stress = random.randint(6, 9)            # Anxious
            sleep = random.uniform(5, 7)
            wellbeing = random.randint(4, 6)
            prod_score = random.randint(3, 5)
            distractions = random.randint(5, 8)
            career = random.randint(3, 6)            # Unsure
            skill = random.randint(3, 5)
            engagement = random.uniform(40, 60)
            
        elif bucket == 'Blue': # STANDARD (The "Average Joe")
            gpa = random.uniform(7.0, 8.5)           # Good
            attendance = random.uniform(75, 90)      # Regular
            assign_comp = random.uniform(70, 90)
            stress = random.randint(3, 6)            # Manageable
            sleep = random.uniform(6, 8)
            wellbeing = random.randint(6, 8)
            prod_score = random.randint(6, 8)
            distractions = random.randint(3, 6)
            career = random.randint(5, 8)
            skill = random.randint(5, 7)
            engagement = random.uniform(60, 85)

        elif bucket == 'Green': # EXCELLENT (The "Star")
            gpa = random.uniform(8.5, 10.0)          # Topper
            attendance = random.uniform(90, 100)     # Present
            assign_comp = random.uniform(90, 100)    # Perfect
            stress = random.randint(1, 4)            # Eustress/Chill
            sleep = random.uniform(7, 9)             # Healthy
            wellbeing = random.randint(8, 10)
            prod_score = random.randint(8, 10)       # Machine
            distractions = random.randint(1, 3)      # Locked in
            career = random.randint(8, 10)           # Clear Goal
            skill = random.randint(8, 10)
            engagement = random.uniform(85, 100)

        # Add some noise so it doesn't look fake
        gpa += random.uniform(-0.2, 0.2)
        gpa = np.clip(gpa, 0, 10)
        
        data.append([
            s_id, age, program, semester, round(gpa, 2), 
            round(attendance, 1), round(assign_comp, 1),
            stress, round(sleep, 1), wellbeing, 
            prod_score, distractions, career, 
            skill, round(engagement, 1)
        ])

    columns = [
        'student_id', 'age', 'program', 'semester', 'gpa', 
        'attendance', 'assignments_completion', 'stress_level', 
        'sleep_hours', 'mental_wellbeing', 'productivity_score', 
        'distractions', 'career_clarity', 'skill_readiness', 
        'engagement_score'
    ]
    
    return pd.DataFrame(data, columns=columns)

# 1. Generate Better Data
df_v2 = generate_balanced_dataset(500)
df_v2.to_csv('students_v2.csv', index=False)
print("Created students_v2.csv with forced variance.")