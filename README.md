# 🎯 AI Talent Intelligence & Automatic Job Skill Extractor

An end-to-end Natural Language Processing (NLP) and Machine Learning platform designed to automate technical recruitment. This application instantly extracts structured skills from unstructured Job Descriptions (JDs) and calculates a real-time Match Score by comparing them against candidate PDF resumes.

## 🚀 Key Features

*   **Automated Skill Extraction:** Uses a custom taxonomy alongside **TF-IDF vectorization** and **Logistic Regression** to extract and categorize technical skills into domains (e.g., Cloud, Database, Programming).
*   **Candidate Match Scoring:** Upload a candidate's PDF resume to instantly calculate a `0-100%` overlap match score against the required JD skills.
*   **Robust Text Normalization:** Features an aggressive Regular Expression (Regex) pipeline that solves common PDF parsing anomalies (e.g., successfully mapping "PowerBI" or "Power-BI" to "Power BI").
*   **Interactive Recruiter Dashboard:** A modern, state-managed web interface built with **Streamlit** featuring real-time KPI metrics.
*   **Enterprise API Ready:** Automatically structures the extracted skills into JSON payloads and CSV formats for seamless integration with Applicant Tracking Systems (ATS).

## 🛠️ Technology Stack

*   **Language:** Python 3.x
*   **Machine Learning:** Scikit-learn (Logistic Regression, TF-IDF Vectorizer)
*   **NLP & Text Processing:** Regular Expressions (Regex), NLTK, spaCy
*   **Document Parsing:** PyPDF2
*   **Frontend / UI:** Streamlit
*   **Data Manipulation:** Pandas, NumPy

## 🧠 System Architecture & Pipeline

1.  **Data Ingestion & Cleaning:** Raw job descriptions are strictly lowercased, and alphanumeric noise/stopwords are removed.
2.  **Statistical Vectorization:** TF-IDF penalizes ubiquitous business buzzwords (like "team") while boosting the importance of rare technical terms.
3.  **Rule-Based & ML Classification:** Word-boundary Regex prevents partial matches (e.g., confusing "Java" with "JavaScript"), and a multiclass Logistic Regression pipeline accurately maps tools to their parent categories.
4.  **Match Engine:** Normalizes both the JD and the uploaded PDF resume text to strip all spacing/punctuation, ensuring flawless mathematical overlap calculation.

## 💻 Installation & Setup

Follow these steps to run the application locally on your machine.

**1. Clone the repository**
```bash
git clone [https://github.com/Shridharan04/Automatic_Job_Skill_Extractor.git](https://github.com/Shridharan04/Automatic_Job_Skill_Extractor.git)
cd Automatic_Job_Skill_Extractor
