# redrob-ai-candidate-ranking-system
AI-powered candidate ranking system built for the Redrob Data &amp; AI Challenge. Uses hybrid scoring, behavioral signals, retrieval relevance, and anti-skill-stuffing heuristics to identify the best-fit candidates from 100,000 profiles.
AI-Powered Candidate Ranking System
Problem Statement
Traditional Applicant Tracking Systems (ATS) rely heavily on keyword matching and often fail to identify genuinely qualified candidates. The objective of this challenge is to build an intelligent ranking system that evaluates candidates the way an experienced recruiter would, considering skills, experience, behavioral signals, and career progression rather than simple keyword overlap.
________________________________________
Solution Overview
This solution implements a hybrid candidate ranking framework that combines:
•	Technical Relevance
•	Retrieval & Ranking Experience
•	Product Company Exposure
•	Behavioral Signals
•	Experience Alignment
•	Location & Relocation Preference
•	Skill-Stuffing Detection
The system processes candidate profiles and generates a ranked list of the Top 100 candidates for the target role.
________________________________________
Architecture
Job Requirements
        │
        ▼
Feature Extraction
        │
        ├── Technical Skills
        ├── Retrieval Experience
        ├── Product Experience
        ├── Behavioral Signals
        ├── Location Fit
        │
        ▼
Candidate Scoring Engine
        │
        ▼
Anti-Stuffing Validation
        │
        ▼
Final Ranking
        │
        ▼
Top 100 Candidates
________________________________________
Features Used
Technical Relevance (35%)
Identifies experience related to:
•	LLMs
•	Machine Learning
•	NLP
•	Deep Learning
•	RAG
•	MLOps
•	Prompt Engineering
Retrieval & Search Experience (20%)
Identifies:
•	Search Systems
•	Recommendation Systems
•	Ranking Systems
•	Retrieval Systems
•	Embeddings
•	Vector Databases
•	Semantic Search
Product Company Fit (15%)
Boosts candidates with experience in:
•	SaaS
•	Product Companies
•	Technology Startups
•	Software Organizations
Experience Alignment (10%)
Preferred range:
5 - 9 years
Behavioral Signals (15%)
Uses:
•	Profile Completeness
•	Recruiter Response Rate
•	Interview Completion Rate
•	Open To Work Status
•	Saved By Recruiters
Location Fit (5%)
Boosts:
•	India-based candidates
•	Candidates willing to relocate
________________________________________
Skill Stuffing Detection
Some candidates contain numerous AI-related keywords without relevant professional experience.
The system penalizes profiles that:
•	Mention many AI keywords
•	Lack AI/ML-related job titles
•	Show inconsistent career trajectories
________________________________________
Ranking Formula
Final Score

= 35% Technical Relevance
+ 20% Retrieval Experience
+ 15% Product Company Fit
+ 10% Experience Fit
+ 15% Behavioral Signals
+ 5% Location Fit
- Skill Stuffing Penalty
________________________________________
Output
The system produces:
candidate_id
rank
score
reasoning
and returns the Top 100 ranked candidates.
________________________________________
How to Run
python src_ranker.py
Generated output:
final_submission.csv
________________________________________
Future Improvements
•	Learning-to-Rank Models
•	Sentence Transformer Embeddings
•	LLM Re-ranking
•	Graph-Based Candidate Similarity
•	Recruiter Feedback Loop
________________________________________
requirements.txt
pandas
numpy

