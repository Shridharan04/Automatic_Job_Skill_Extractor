# Day 7 Task : Building Rule Based Skill Extractor

import pandas as pd

# Define our base dictionary of skills to search for
skills_to_find = [
    "python", 
    "sql", 
    "power bi", 
    "tableau", 
    "excel", 
    "aws"
]
print("Skill dictionary loaded with", len(skills_to_find), "skills.")

def extract_skills(text):
    """
    Scans the input text and returns a list of skills found from our dictionary.
    """
    found_skills = []
    
    # Make sure the text is a string and lowercase for exact matching
    text = str(text).lower()
    
    for skill in skills_to_find:
        if skill in text:
            found_skills.append(skill)
            
    return found_skills

# Test it on a dummy sentence
test_sentence = "We need someone with advanced Excel skills and Python experience."
print("Test Extraction:", extract_skills(test_sentence)) 

# Loading the cleaned dataset
print("Loading clean_jobs.csv...")
df = pd.read_csv("clean_jobs.csv")

# Applying our extraction function to the clean_description column
print("Extracting skills across all job postings...")
df['extracted_skills'] = df['clean_description'].apply(extract_skills)

# Filter for rows where skills were actually found
successful_extractions = df[df['extracted_skills'].map(len) > 0]

print("\nSample extractions:")
# Use print() instead of display() for a .py script
print(successful_extractions[['title', 'extracted_skills']].head())

