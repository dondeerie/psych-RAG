# Psychology 101 Dataset Documentation

## Overview
This dataset contains student performance and feedback data for a Psychology 101 course from Fall 2024. The data is split into two CSV files: one containing quantitative metrics and demographics, and another containing qualitative feedback and learning preferences.

## File Structure
- psych101-quantitative.csv: Contains numerical data and demographic information
- psych101-qualitative.csv: Contains text-based feedback and categorical assessments

## Common Fields
### student_id (Both files)
- Format: PSY101_F24_XXX
- Description: Unique identifier for each student
- Example: PSY101_F24_001
- Note: Used to link records between quantitative and qualitative files

## Quantitative Variables (psych101-quantitative.csv)

### Demographic Information

#### age
- Type: Integer
- Range: 18-22
- Description: Student's age in years
- Notes: Typical undergraduate age range

#### gender
- Type: Categorical
- Values: Female, Male, Non-binary
- Description: Student's gender identity

#### ethnicity
- Type: Categorical
- Values: Asian, Black, Hispanic, Middle Eastern, White
- Description: Student's ethnic background

#### first_gen_student
- Type: Boolean
- Values: Yes/No
- Description: Indicates if the student is a first-generation college student
- Note: "Yes" means neither parent completed a 4-year college degree

#### international_student
- Type: Boolean
- Values: Yes/No
- Description: Indicates if the student is an international student

### Academic Performance Metrics

#### midterm_grade
- Type: Numeric
- Range: 0-100
- Description: Score on midterm examination
- Note: Higher scores indicate better performance

#### final_exam
- Type: Numeric
- Range: 0-100
- Description: Score on final examination
- Note: Higher scores indicate better performance

#### assignment_avg
- Type: Numeric
- Range: 0-100
- Description: Average score across all course assignments
- Note: Weighted average of multiple assignments throughout the semester

#### participation_score
- Type: Numeric
- Range: 0-100
- Description: Measure of student's active participation in class
- Components: In-class discussion, online forum participation, group work contribution

### Engagement Metrics

#### attendance_rate
- Type: Numeric
- Range: 0-100
- Description: Percentage of classes attended
- Calculation: (Classes attended / Total classes) × 100

#### study_hours_per_week
- Type: Numeric
- Range: 0-15
- Description: Average number of hours spent studying per week
- Note: Self-reported by students

#### group_work_score
- Type: Numeric
- Range: 0-100
- Description: Performance in collaborative assignments
- Components: Peer evaluations, group project grades, team participation

#### office_hours_attended
- Type: Integer
- Range: 0-10
- Description: Number of office hour sessions attended
- Note: Includes both professor and TA office hours

## Qualitative Variables (psych101-qualitative.csv)

#### year
- Type: Categorical
- Values: Freshman, Sophomore, Junior, Senior
- Description: Student's academic year

#### major
- Type: Categorical
- Description: Student's declared academic major
- Note: Includes various disciplines across the university

#### course_review
- Type: Text
- Description: Detailed student feedback about the course
- Components: Course structure, teaching effectiveness, content relevance
- Length: Typically 2-4 sentences

#### learning_outcomes_assessment
- Type: Text
- Description: Student's self-assessment of their learning
- Components: Knowledge gained, skills developed, practical applications
- Length: Typically 1-3 sentences

#### engagement_level
- Type: Categorical
- Values: Low, Medium, High, Very High
- Description: Overall level of student engagement with course material

#### preferred_learning_style
- Type: Categorical
- Values: Visual, Auditory, Kinesthetic, Analytical, Verbal, Logical, Mixed
- Description: Student's primary learning style preference
- Note: Self-reported by students

#### online_participation
- Type: Categorical
- Values: Low, Moderate, Active, Very Active
- Description: Level of participation in online components
- Components: Forum posts, online discussions, virtual collaboration

## Data Usage Notes

### Missing Values
- Numerical fields: No missing values in the dataset
- Text fields: All fields contain complete responses
- Categorical fields: No undefined or null values

### Privacy Considerations
- Student IDs are anonymized
- Demographic data is included for analytical purposes
- Personal identifying information has been removed

### Interpretation Guidelines
1. Academic Performance:
   - Grades above 90: Excellent
   - 80-89: Good
   - 70-79: Satisfactory
   - Below 70: Needs improvement

2. Engagement Metrics:
   - Attendance Rate > 95%: Excellent
   - 85-95%: Good
   - Below 85%: Needs improvement

3. Study Hours:
   - 8+ hours: High engagement
   - 5-7 hours: Moderate engagement
   - <5 hours: Low engagement

## Sample Queries and Analysis
1. Demographic Analysis:
   - Compare performance across different demographic groups
   - Analyze engagement patterns by student background

2. Performance Correlations:
   - Study hours vs. grades
   - Attendance vs. participation
   - Office hours attendance vs. academic performance

3. Qualitative Analysis:
   - Common themes in course reviews
   - Learning style preferences by major
   - Engagement patterns across different years