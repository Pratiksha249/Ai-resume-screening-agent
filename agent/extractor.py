import re


# ============================================================
# Helper Functions
# ============================================================

def clean_text(text):
    """
    Clean extracted resume text while preserving
    section and line information.
    """

    text = text.replace("\r", "\n")

    # Normalize excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def get_section(text, start_headings, end_headings):
    """
    Extract text between a starting section heading
    and the next known section heading.

    Supports headings such as:

        Experience:
        EXPERIENCE
        WORK EXPERIENCE
        Education:
        EDUCATION
    """

    # Allow a single string OR a list of headings
    if isinstance(start_headings, str):

        start_headings = [start_headings]

    if isinstance(end_headings, str):

        end_headings = [end_headings]

    # --------------------------------------------------------
    # Find the first matching start heading
    # --------------------------------------------------------

    start_match = None

    for heading in start_headings:

        match = re.search(
            rf"(?im)^\s*{re.escape(heading)}\s*:?\s*$",
            text
        )

        if match:

            if (
                start_match is None
                or match.start() < start_match.start()
            ):

                start_match = match

    if start_match is None:

        return ""

    # Text after the heading
    start_position = start_match.end()

    remaining_text = text[start_position:]

    # --------------------------------------------------------
    # Find the next section
    # --------------------------------------------------------

    end_positions = []

    for heading in end_headings:

        match = re.search(
            rf"(?im)^\s*{re.escape(heading)}\s*:?\s*$",
            remaining_text
        )

        if match:

            end_positions.append(
                match.start()
            )

    # --------------------------------------------------------
    # Extract section
    # --------------------------------------------------------

    if end_positions:

        end_position = min(end_positions)

        section = remaining_text[
            :end_position
        ]

    else:

        section = remaining_text

    return section.strip()


# ============================================================
# Name Extraction
# ============================================================

def extract_name(text):
    """
    Extract candidate name.

    Supports:

    Name: Priya Nair

    and:

    PRATIKSHA P NAIK
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:

        return "Unknown"

    # --------------------------------------------------------
    # Case 1: Explicit Name field
    # --------------------------------------------------------

    for line in lines[:5]:

        match = re.match(
            r"^name\s*:\s*(.+)$",
            line,
            flags=re.IGNORECASE
        )

        if match:

            name = match.group(1).strip()

            if name:

                return name

    # --------------------------------------------------------
    # Case 2: First meaningful line
    # --------------------------------------------------------

    first_line = lines[0]

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
# Skills Extraction
# ============================================================

def extract_skills(text):
    """
    Extract skills that actually occur in the resume.
    """

    skills = []

    skill_patterns = {

        "Python":
            r"\bpython\b",

        "Java":
            r"\bjava\b",

        "JavaScript":
            r"\bjavascript\b",

        "SQL":
            r"\bsql\b",

        "Machine Learning":
            r"\bmachine learning\b|\bml\b",

        "Deep Learning":
            r"\bdeep learning\b",

        "Artificial Intelligence":
            r"\bartificial intelligence\b"
            r"|\bai-focused\b"
            r"|\bai/ml\b",

        "Generative AI":
            r"\bgenerative ai\b"
            r"|\bgenai\b",

        "NLP":
            r"\bnatural language processing\b"
            r"|\bnlp\b",

        "LLM":
            r"\bllms?\b"
            r"|\blarge language models?\b",

        "Transformers":
            r"\btransformers\b"
            r"|\bhuggingface transformers\b",

        "PyTorch":
            r"\bpytorch\b",

        "TensorFlow":
            r"\btensorflow\b",

        "Scikit-learn":
            r"\bscikit-learn\b"
            r"|\bsklearn\b",

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
            r"\brest api\b"
            r"|\brest apis\b",

        "MySQL":
            r"\bmysql\b",

        "MongoDB":
            r"\bmongodb\b",

        "AWS":
            r"\baws\b",

        "Azure":
            r"\bazure\b",

        "GCP":
            r"\bgcp\b"
            r"|\bgoogle cloud platform\b",

        "Git":
            r"\bgit\b",

        "GitHub":
            r"\bgithub\b",

        "Jupyter":
            r"\bjupyter\b",

        "Power BI":
            r"\bpower bi\b",

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
            r"\bspacy\b"
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
# Education Extraction
# ============================================================

def extract_education(text):
    """
    Extract education section.

    Supports:

        EDUCATION

    and:

        Education:
    """

    section = get_section(
        text,

        [
            "EDUCATION",
            "Education"
        ],

        [
            "PUBLICATION",
            "Publication",
            "ACHIEVEMENTS",
            "Achievements",
            "ACHIEVEMENTS & LEADERSHIP",
            "Achievements & Leadership",
            "LEADERSHIP",
            "Leadership"
        ]
    )

    return section.strip()


# ============================================================
# Experience Extraction
# ============================================================

def extract_experience(text):
    """
    Extract work experience section.

    Supports:

        WORK EXPERIENCE

    and:

        Experience:
    """

    section = get_section(
        text,

        [
            "WORK EXPERIENCE",
            "Work Experience",
            "EXPERIENCE",
            "Experience"
        ],

        [
            "PROJECTS",
            "Projects",
            "EDUCATION",
            "Education",
            "PUBLICATION",
            "Publication",
            "ACHIEVEMENTS",
            "Achievements",
            "ACHIEVEMENTS & LEADERSHIP",
            "Achievements & Leadership",
            "LEADERSHIP",
            "Leadership"
        ]
    )

    return section.strip()


# ============================================================
# Projects Extraction
# ============================================================

def extract_projects(text):
    """
    Extract project descriptions.
    """

    section = get_section(
        text,

        [
            "PROJECTS",
            "Projects"
        ],

        [
            "EDUCATION",
            "Education",
            "PUBLICATION",
            "Publication",
            "ACHIEVEMENTS",
            "Achievements",
            "ACHIEVEMENTS & LEADERSHIP",
            "Achievements & Leadership",
            "LEADERSHIP",
            "Leadership"
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

        if line.lower().startswith("tech:"):

            current_project += " " + line

        elif line.startswith("-"):

            if current_project:

                projects.append(
                    current_project.strip()
                )

            current_project = line.lstrip("-").strip()

        else:

            if current_project:

                current_project += " " + line

            else:

                current_project = line

    if current_project:

        projects.append(
            current_project.strip()
        )

    return projects


# ============================================================
# Research Extraction
# ============================================================

def extract_research(text):
    """
    Extract research/publication information.
    """

    # First try PUBLICATION
    section = get_section(
        text,

        [
            "PUBLICATION",
            "Publication"
        ],

        [
            "ACHIEVEMENTS",
            "Achievements",
            "ACHIEVEMENTS & LEADERSHIP",
            "Achievements & Leadership",
            "LEADERSHIP",
            "Leadership"
        ]
    )

    # If publication doesn't exist,
    # try Research
    if not section:

        section = get_section(
            text,

            [
                "RESEARCH",
                "Research"
            ],

            [
                "EDUCATION",
                "Education",
                "PROJECTS",
                "Projects",
                "ACHIEVEMENTS",
                "Achievements"
            ]
        )

    return section.strip()


# ============================================================
# Main Extraction Function
# ============================================================

def extract_resume_information(text):
    """
    Extract structured candidate information
    from resume text.
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