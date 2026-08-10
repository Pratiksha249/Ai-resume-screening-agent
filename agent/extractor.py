import re


# ============================================================
# Helper functions
# ============================================================

def clean_text(text):
    """
    Clean extracted PDF text while preserving useful
    line and section information.
    """

    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def get_section(text, start_heading, end_headings):
    """
    Extract text between one section heading and
    the next known section heading.
    """

    pattern = re.escape(start_heading)

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    if not match:
        return ""

    start = match.end()

    remaining_text = text[start:]

    end_positions = []

    for heading in end_headings:

        heading_match = re.search(
            re.escape(heading),
            remaining_text,
            flags=re.IGNORECASE
        )

        if heading_match:
            end_positions.append(
                heading_match.start()
            )

    if end_positions:

        end = min(end_positions)

        return remaining_text[:end].strip()

    return remaining_text.strip()


# ============================================================
# Name extraction
# ============================================================

def extract_name(text):
    """
    Extract candidate name.

    Assumes the first meaningful line of the resume
    is the candidate's name.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return "Unknown"

    # Usually the first line of a resume is the name.
    first_line = lines[0]

    # Avoid treating common headings as names
    invalid_names = {
        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "summary"
    }

    if first_line.lower() in invalid_names:
        return "Unknown"

    return first_line


# ============================================================
# Skills extraction
# ============================================================

def extract_skills(text):
    """
    Extract skills that are actually present in the resume.

    This avoids adding every skill from a predefined list.
    """

    skills = []

    # Skills that we recognize.
    # We only add them if they actually occur in the resume.
    skill_patterns = {

        "Python": r"\bpython\b",

        "Java": r"\bjava\b",

        "JavaScript": r"\bjavascript\b",

        "SQL": r"\bsql\b",

        "Machine Learning": r"\bmachine learning\b|\bml\b",

        "Deep Learning": r"\bdeep learning\b",

        "Artificial Intelligence":
            r"\bartificial intelligence\b|\bai-focused\b|\bai/ml\b",

        "Generative AI":
            r"\bgenerative ai\b|\bgenai\b",

        "NLP":
            r"\bnatural language processing\b|\bnlp\b",

        "LLM":
            r"\bllms?\b|\blarge language models?\b",

        "Transformers":
            r"\btransformers\b|\bhuggingface transformers\b",

        "PyTorch":
            r"\bpytorch\b",

        "TensorFlow":
            r"\btensorflow\b",

        "Scikit-learn":
            r"\bscikit-learn\b|\bsklearn\b",

        "Pandas":
            r"\bpandas\b",

        "NumPy":
            r"\bnumpy\b",

        "OpenCV":
            r"\bopencv\b",

        "FastAPI":
            r"\bfastapi\b",

        "Streamlit":
            r"\bstreamlit\b",

        "REST API":
            r"\brest api\b|\brest apis\b",

        "MySQL":
            r"\bmysql\b",

        "MongoDB":
            r"\bmongodb\b",

        "AWS":
            r"\baws\b",

        "Azure":
            r"\bazure\b",

        "GCP":
            r"\bgcp\b|\bgoogle cloud platform\b",

        "Git":
            r"\bgit\b",

        "GitHub":
            r"\bgithub\b",

        "Jupyter":
            r"\bjupyter\b",

        "Power BI":
            r"\bpower bi\b",

        "OpenCV":
            r"\bopencv\b",

        "TensorFlow":
            r"\btensorflow\b",

        "CNN":
            r"\bcnns?\b",

        "Prompt Engineering":
            r"\bprompt engineering\b",

        "AI Agent Development":
            r"\bai agent development\b",

        "Multi-Agent Systems":
            r"\bmulti-agent systems?\b",

        "Google ADK":
            r"\bgoogle adk\b",

        "MediaPipe":
            r"\bmediapipe\b",

        "PyBullet":
            r"\bpybullet\b",

        "Three.js":
            r"\bthree\.js\b",

        "NLTK":
            r"\bnltk\b",

        "spaCy":
            r"\bspacy\b",

        "REST APIs":
            r"\brest api\b|\brest apis\b"
    }


    for skill, pattern in skill_patterns.items():

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):

            if skill not in skills:

                skills.append(skill)


    return skills


# ============================================================
# Education extraction
# ============================================================

def extract_education(text):
    """
    Extract education section.
    """

    section = get_section(
        text,
        "EDUCATION",
        [
            "PUBLICATION",
            "ACHIEVEMENTS",
            "ACHIEVEMENTS & LEADERSHIP",
            "LEADERSHIP"
        ]
    )

    if not section:
        return ""

    return section.strip()


# ============================================================
# Experience extraction
# ============================================================

def extract_experience(text):
    """
    Extract work experience section.
    """

    section = get_section(
        text,
        "WORK EXPERIENCE",
        [
            "PROJECTS",
            "EDUCATION",
            "PUBLICATION",
            "ACHIEVEMENTS",
            "ACHIEVEMENTS & LEADERSHIP"
        ]
    )

    if not section:
        return ""

    return section.strip()


# ============================================================
# Projects extraction
# ============================================================

def extract_projects(text):
    """
    Extract project descriptions.
    """

    section = get_section(
        text,
        "PROJECTS",
        [
            "EDUCATION",
            "PUBLICATION",
            "ACHIEVEMENTS",
            "ACHIEVEMENTS & LEADERSHIP"
        ]
    )

    if not section:
        return []

    projects = []

    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]

    current_project = ""

    for line in lines:

        # Ignore standalone "Tech:" lines by attaching
        # them to the previous project.
        if line.lower().startswith("tech:"):

            current_project += " " + line

        else:

            if current_project:

                projects.append(
                    current_project.strip()
                )

            current_project = line

    if current_project:

        projects.append(
            current_project.strip()
        )

    return projects


# ============================================================
# Research / Publication extraction
# ============================================================

def extract_research(text):
    """
    Extract publication/research information.
    """

    section = get_section(
        text,
        "PUBLICATION",
        [
            "ACHIEVEMENTS",
            "ACHIEVEMENTS & LEADERSHIP",
            "LEADERSHIP"
        ]
    )

    return section.strip()


# ============================================================
# Main extraction function
# ============================================================

def extract_resume_information(text):
    """
    Main resume information extraction function.

    Returns structured candidate information.
    """

    text = clean_text(text)

    candidate = {

        "name":
            extract_name(text),

        "skills":
            extract_skills(text),

        "education":
            extract_education(text),

        "experience":
            extract_experience(text),

        "projects":
            extract_projects(text),

        "research":
            extract_research(text)
    }

    return candidate