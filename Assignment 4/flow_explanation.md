# Assignment 4: End-to-End Flow Explanation

## Objective
Translate student insights (scores & clusters) into actionable mentoring recommendations by matching students with mentors and suggesting interventions.

---

## 1. Data Ingestion
- **Student Data**: Loaded from `students_with_scores_v2.csv` containing academic scores (GPA, Attendance), behavioral metrics (Stress Level, Career Clarity), and demographics.
- **Mentor Data**: Loaded from `mentors.csv` containing name, expertise (Academic Support, Career Guidance, Emotional Wellness, Advanced Research), and capacity (`Max_Mentees`).

---

## 2. Student Segmentation (Clustering)
- We use **K-Means Clustering (K=4)** to segment students based on:
  - GPA, Attendance, Stress Level, Mental Wellbeing, Productivity Score, Career Clarity, Engagement Score.
- **Cluster Labels**:
  - **High Performer**: Highest GPA/Engagement.
  - **Average**: Moderate performance.
  - **Struggling**: Lower GPA/Attendance.
  - **At Risk**: Lowest scores, high stress, or dropout risk.

---

## 3. Intervention & Matching Logic
For each student, we determine the intervention and required mentor expertise based on their Cluster and specific flags:

| Student Category | Condition | Required Expertise | Intervention | Alert |
| :--- | :--- | :--- | :--- | :--- |
| **At Risk** | Stress > 7 | Emotional Wellness | Wellness Counseling | High Risk - Immediate Attention |
| **At Risk** | Else | Academic Support | Remedial Classes | Academic Alert |
| **Struggling** | Career Clarity < 4 | Career Guidance | Career Workshop | - |
| **Struggling** | Else | Academic Support | Extra Office Hours | - |
| **Average** | Career Clarity < 6 | Career Guidance | Internship Prep | - |
| **Average** | Else | Career Generalist | Skill Building | - |
| **High Performer**| Stress > 8 | Emotional Wellness | Stress Management | Burnout Risk |
| **High Performer**| Else | Advanced Research | Research Mentorship | - |

---

## 4. Mentor Allocation
- The system filters mentors matching the **Required Expertise**.
- It sorts eligible mentors by current load (`Current_Mentees`) to ensure **Load Balancing**.
- It assigns the first available mentor.
- If a mentor reaches `Max_Mentees` capacity, the matching logic skips them.

---

## 5. Final Output
- **`recommendations.csv`**: Contains the final mapping of:
  - **Student ID**
  - **Cluster Label**
  - **Assigned Mentor**
  - **Intervention**
  - **Alert Status**
- **`mentors_updated.csv`**: Tracks the final mentee count for each mentor to verify capacity constraints.
