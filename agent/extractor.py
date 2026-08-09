import re


# Skills that our first version knows how to identify.
KNOWN_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "Generative AI",
    "LLM",
    "Large Language Models",
    "Transformers",
    "PyTorch",
    "TensorFlow",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "OpenCV",
    "LangChain",
    "RAG",
    "Git",
    "Docker",
    "AWS",
    "Azure",
    "GCP",
]


def extract_section(text, section_name, next_sections):
    """
    Extract the text belonging to one resume section.
    """

    pattern = rf"{section_name}\s*:\s*(.*?)(?=\n(?:{'|'.join(next_sections)})\s*:|\Z)"

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def extract_name(text):
    """
    Extract the candidate's name.
    """

    match = re.search(
        r"Name\s*:\s*(.+)",
        text,
        flags=re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return "Unknown"


def extract_skills(text):
    """
    Identify known technical skills in the resume.
    """

    found_skills = []

    text_lower = text.lower()

    for skill in KNOWN_SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_resume_information(text):
    """
    Convert raw resume text into structured information.
    """

    sections = [
        "Education",
        "Skills",
        "Experience",
        "Projects",
        "Research"
    ]

    education = extract_section(
        text,
        "Education",
        ["Skills", "Experience", "Projects", "Research"]
    )

    experience = extract_section(
        text,
        "Experience",
        ["Education", "Skills", "Projects", "Research"]
    )

    projects = extract_section(
        text,
        "Projects",
        ["Education", "Skills", "Experience", "Research"]
    )

    research = extract_section(
        text,
        "Research",
        ["Education", "Skills", "Experience", "Projects"]
    )

    return {
        "name": extract_name(text),
        "skills": extract_skills(text),
        "education": education,
        "experience": experience,
        "projects": projects,
        "research": research
    }