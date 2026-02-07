import pandas as pd
import numpy as np
import random

def generate_complex_dataset(num_students=500):
    data = []
    programs = ['B.Tech', 'BCA', 'B.Sc', 'MBA']
    
    # Define "Archetypes"
    # We will generate students based on these profiles + random variation
    archetypes = [
        {'name': 'High Achiever', 'weight': 0.25, 
         'gpa_range': (8.5, 10.0), 'att_range': (90, 100), 'stress_range': (2, 5), 'career_range': (8, 10)},
        
        {'name': 'Average Student', 'weight': 0.35, 
         'gpa_range': (6.5, 8.5), 'att_range': (70, 90), 'stress_range': (4, 7), 'career_range': (5, 8)},
        
        {'name': 'Struggling Student', 'weight': 0.20, 
         'gpa_range': (4.0, 6.5), 'att_range': (50, 75), 'stress_range': (6, 9), 'career_range': (2, 5)},
        
        {'name': 'At-Risk', 'weight': 0.10, 
         'gpa_range': (0.0, 4.0), 'att_range': (0, 50), 'stress_range': (8, 10), 'career_range': (1, 3)},
    ]
    
    # Specific Pattern Injections (approx 10% total)
    # These inject specific combinations requested in the assignment
    patterns = [
        # Pattern 1: High Stress + Low Productivity (Burnout)
        {'name': 'Burnout', 'count': 25, 
         'gpa': (7.0, 9.5), 'stress': (8, 10), 'prod': (1, 4), 'career': (5, 9)},
        
        # Pattern 2: Low GPA + High Engagement (The "Grinder" who tries hard but struggles)
        {'name': 'Grinder', 'count': 25, 
         'gpa': (4.0, 6.0), 'att': (80, 100), 'eng': (80, 100), 'assign': (80, 100)},
        
        # Pattern 3: Strong Academics + Unclear Career Goals (The "Drifter")
        {'name': 'Drifter', 'count': 25, 
         'gpa': (8.5, 10.0), 'career': (1, 3), 'skill': (6, 9)} 
    ]
    
    # Helper to clamp values
    def clamp(val, min_v, max_v):
        return max(min_v, min(val, max_v))

    student_counter = 1
    
    # 1. Generate Archetype Students
    for arch in archetypes:
        count = int(num_students * arch['weight'])
        for _ in range(count):
            program = random.choice(programs)
            semester = random.randint(1, 8)
            base_age = 18 if program != 'MBA' else 22
            age = base_age + (semester // 2)
            
            # Base Stats from Archetype
            gpa = random.uniform(*arch['gpa_range'])
            attendance = random.uniform(*arch['att_range'])
            career = random.randint(*arch['career_range'])
            stress = random.randint(*arch['stress_range'])
            
            # Derived Stats (with noise)
            # High GPA usually means high completion, but not always
            assign_comp = attendance + random.uniform(-10, 10)
            engagement = attendance + random.uniform(-15, 10)
            skill = (gpa * 10) + random.uniform(-20, 10)
            
            # Stress/Wellbeing/Sleep correlations
            # High stress -> Lower sleep, Lower wellbeing
            sleep = random.uniform(5, 9) - (stress * 0.2) 
            wellbeing = 10 - stress + random.randint(-2, 2)
            
            # Productivity
            prod_score = random.randint(1, 10)
            if gpa > 8: prod_score = random.randint(7, 10)
            elif gpa < 5: prod_score = random.randint(1, 5)
            
            distractions = 10 - prod_score + random.randint(-2, 2)
            
            # CLAMP ALL
            data.append({
                'student_id': f"S{student_counter:03d}",
                'age': age,
                'program': program,
                'semester': semester,
                'gpa': clamp(gpa, 0, 10),
                'attendance': clamp(attendance, 0, 100),
                'assignments_completion': clamp(assign_comp, 0, 100),
                'stress_level': clamp(stress, 1, 10),
                'sleep_hours': clamp(sleep, 0, 10),
                'mental_wellbeing': clamp(wellbeing, 1, 10),
                'productivity_score': clamp(prod_score, 1, 10),
                'distractions': clamp(distractions, 1, 10),
                'career_clarity': clamp(career, 1, 10),
                'skill_readiness': clamp(skill / 10, 1, 10), # scale back to 1-10
                'engagement_score': clamp(engagement, 0, 100)
            })
            student_counter += 1

    # 2. Generate Pattern Students (Overwrite/Inject)
    # We explicitly create these and add them
    for pat in patterns:
        for _ in range(pat['count']):
            program = random.choice(programs)
            semester = random.randint(1, 8)
            base_age = 18 if program != 'MBA' else 22
            age = base_age + (semester // 2)
            
            # Defaults (Average)
            gpa = random.uniform(6, 8)
            att = random.uniform(70, 90)
            stress = random.randint(4, 7)
            prod = random.randint(5, 8)
            career = random.randint(5, 8)
            eng = random.uniform(60, 90)
            assign = random.uniform(70, 90)
            sleep = random.uniform(6, 8)
            wellbeing = random.randint(5, 8)
            dist = random.randint(3, 7)
            skill = random.randint(5, 8)

            # Apply Overrides
            if 'gpa' in pat: gpa = random.uniform(*pat['gpa'])
            if 'stress' in pat: stress = random.randint(*pat['stress'])
            if 'prod' in pat: prod = random.randint(*pat['prod'])
            if 'career' in pat: career = random.randint(*pat['career'])
            if 'att' in pat: att = random.uniform(*pat['att'])
            if 'eng' in pat: eng = random.uniform(*pat['eng'])
            if 'assign' in pat: assign = random.uniform(*pat['assign'])
            if 'skill' in pat: skill = random.randint(*pat['skill'])
            
            # Logic consistencies for injected patterns
            if pat['name'] == 'Burnout':
                # High stress implies low wellbeing/sleep
                wellbeing = random.randint(1, 4)
                sleep = random.uniform(3, 5)
            
            if pat['name'] == 'Drifter':
                # High academic but low career
                # skill might be high (academic) or low (practical). Let's keep skill high-ish but career low.
                pass 
                
            data.append({
                'student_id': f"S{student_counter:03d}",
                'age': age,
                'program': program,
                'semester': semester,
                'gpa': clamp(gpa, 0, 10),
                'attendance': clamp(att, 0, 100),
                'assignments_completion': clamp(assign, 0, 100),
                'stress_level': clamp(stress, 1, 10),
                'sleep_hours': clamp(sleep, 0, 10),
                'mental_wellbeing': clamp(wellbeing, 1, 10),
                'productivity_score': clamp(prod, 1, 10),
                'distractions': clamp(dist, 1, 10),
                'career_clarity': clamp(career, 1, 10),
                'skill_readiness': clamp(skill, 1, 10),
                'engagement_score': clamp(eng, 0, 100)
            })
            student_counter += 1
            
    # Shuffle
    random.shuffle(data)
    
    # Re-assign IDs to be sequential after shuffle if desired, or keep as is. 
    # Let's keep IDs as is to show they are distinct records, or re-index for cleanliness.
    # Re-indexing:
    for i, d in enumerate(data):
        d['student_id'] = f"S{i+1:03d}"

    df = pd.DataFrame(data)
    
    # Rounding
    df['gpa'] = df['gpa'].round(2)
    df['attendance'] = df['attendance'].round(1)
    df['assignments_completion'] = df['assignments_completion'].round(1)
    df['sleep_hours'] = df['sleep_hours'].round(1)
    df['engagement_score'] = df['engagement_score'].round(1)
    
    return df

# Execution
df_final = generate_complex_dataset(600) # Generating slightly more to ensure good mix
df_final.to_csv('students_v2.csv', index=False)
print(f"Generated {len(df_final)} students with complex behavioral patterns.")