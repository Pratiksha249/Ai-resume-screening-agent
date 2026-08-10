# 🤖 AI Resume Screening Agent

An AI-powered resume screening and ranking system that analyzes job descriptions, processes multiple candidate resumes, evaluates candidate-job fit, and generates explainable screening results.

The system combines semantic similarity, skill matching, experience evaluation, education relevance, and rule-based reasoning to rank candidates against a given job description.

---

## 🎯 Problem Statement

Recruiters often need to manually review a large number of resumes against a job description.

This process can be:

- Time-consuming
- Repetitive
- Difficult to scale
- Inconsistent across candidates
- Dependent on simple keyword matching

The goal of this project is to build an AI-powered screening agent that can automatically analyze resumes and provide a structured ranking of candidates based on their relevance to a job description.

---

## 💡 Solution

The AI Resume Screening Agent takes:

1. A Job Description
2. Multiple Candidate Resumes

It then:

1. Analyzes the job description
2. Extracts required skills and experience requirements
3. Parses candidate resumes
4. Extracts candidate information
5. Calculates semantic similarity between the JD and resumes
6. Evaluates required skills
7. Evaluates experience duration and relevance
8. Evaluates education
9. Calculates an overall candidate score
10. Ranks candidates
11. Identifies strengths and skill gaps
12. Generates a screening recommendation
13. Exports the results as CSV

---

# 🧠 System Architecture

```text
                         JOB DESCRIPTION
                                │
                                ▼
                    ┌──────────────────────┐
                    │    JD Analyzer       │
                    │                      │
                    │ Required Skills      │
                    │ Experience           │
                    │ Education            │
                    └──────────┬───────────┘
                               │
                               ▼
                 ┌─────────────────────────┐
                 │   Resume Processing     │
                 └────────────┬────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
           PDF              DOCX             TXT
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Resume Parser   │
                    └────────┬─────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Information         │
                  │ Extraction          │
                  │                     │
                  │ Name                │
                  │ Skills              │
                  │ Education           │
                  │ Experience          │
                  │ Projects            │
                  │ Research            │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Semantic Matcher    │
                  │                     │
                  │ JD ↔ Resume         │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Candidate Scorer    │
                  │                     │
                  │ Semantic Similarity │
                  │ Skills              │
                  │ Experience          │
                  │ Education           │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Candidate Ranker    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Reasoning Engine    │
                  │                     │
                  │ Strengths           │
                  │ Skill Gaps          │
                  │ Recommendation      │
                  └──────────┬──────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Streamlit UI    │
                    │                 │
                    │ Ranking         │
                    │ Scores          │
                    │ Candidate Detail│
                    │ CSV Export      │
                    └─────────────────┘