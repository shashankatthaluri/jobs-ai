"""ATS Resume Templates and Action Verbs.

Based on Stanford Career Center guidelines.
These templates ensure ATS compatibility while maintaining professional structure.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# ACTION VERBS BY SKILL AREA - Use these for powerful bullet points
# ═══════════════════════════════════════════════════════════════════════════════

ACTION_VERBS = {
    "communication": [
        "Advised", "Arbitrated", "Clarified", "Collaborated", "Consulted",
        "Coordinated", "Counseled", "Formulated", "Influenced", "Informed",
        "Interpreted", "Mediated", "Negotiated", "Promoted", "Publicized",
        "Recommended", "Represented", "Resolved"
    ],
    "creative": [
        "Conceptualized", "Created", "Designed", "Developed", "Directed",
        "Generated", "Illustrated", "Innovated", "Integrated", "Performed",
        "Planned", "Problem-solved", "Synthesized", "Visualized", "Wrote"
    ],
    "detail_oriented": [
        "Analyzed", "Approved", "Arranged", "Classified", "Compiled",
        "Documented", "Enforced", "Met deadlines", "Prepared", "Processed",
        "Recorded", "Retrieved", "Set priorities", "Systematized"
    ],
    "financial": [
        "Administered", "Allocated", "Analyzed", "Appraised", "Audited",
        "Budgeted", "Calculated", "Computed", "Evaluated", "Forecasted",
        "Managed", "Planned", "Projected"
    ],
    "leadership": [
        "Administered", "Chaired", "Convinced", "Directed", "Executed",
        "Expanded", "Facilitated", "Improved", "Initiated", "Managed",
        "Oversaw", "Produced", "Reviewed", "Supervised"
    ],
    "research": [
        "Analyzed", "Cataloged", "Collected", "Computed", "Conducted",
        "Critiqued", "Diagnosed", "Discovered", "Evaluated", "Examined",
        "Experimented", "Identified", "Inspected", "Investigated",
        "Monitored", "Proved", "Surveyed", "Tested"
    ],
    "technical": [
        "Assembled", "Built", "Calculated", "Computed", "Designed",
        "Engineered", "Fabricated", "Maintained", "Operated", "Programmed",
        "Remodeled", "Repaired", "Solved", "Troubleshot", "Upgraded"
    ],
    "teaching": [
        "Adapted", "Advised", "Clarified", "Coached", "Developed",
        "Encouraged", "Evaluated", "Informed", "Inspired", "Mentored",
        "Motivated", "Taught", "Trained", "Tutored"
    ]
}

# Words to AVOID in ATS resumes (vague, passive, overused)
WORDS_TO_AVOID = [
    "Responsible for",  # Use action verbs instead
    "Duties included",  # Be specific about achievements
    "Helped with",      # Quantify your contribution
    "Worked on",        # Too vague
    "Assisted with",    # Show ownership
    "Familiar with",    # Demonstrate expertise
    "Hard-working",     # Show don't tell
    "Team player",      # Demonstrate with examples
    "Detail-oriented",  # Show with achievements
    "Self-motivated",   # Prove with results
    "References available upon request",  # Outdated
]

# ═══════════════════════════════════════════════════════════════════════════════
# RESUME TEMPLATE STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

CHRONOLOGICAL_TEMPLATE = """# {name}
{email} | {phone} | {location}

## Summary
{summary}

## Experience

{experience_section}

## Skills
{skills_section}

## Education
{education_section}

{additional_section}"""

FUNCTIONAL_TEMPLATE = """# {name}
{email} | {phone} | {location}

## Objective
{objective}

## Education
{education_section}

## Skills & Expertise

{skills_by_category}

## Employment History
{employment_history}

{additional_section}"""

COMBINATION_TEMPLATE = """# {name}
{email} | {phone} | {location}

## Summary
{summary}

## Core Competencies
{core_competencies}

## Professional Experience

{experience_section}

## Education
{education_section}

## Technical Skills
{technical_skills}

{additional_section}"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE FORMATTING RULES (ATS Compliance)
# ═══════════════════════════════════════════════════════════════════════════════

ATS_RULES = """
ATS COMPLIANCE RULES:
1. ONE-COLUMN LAYOUT - No tables, columns, or graphics
2. STANDARD SECTION HEADINGS - Summary, Experience, Skills, Education
3. REVERSE CHRONOLOGICAL ORDER - Most recent first
4. SIMPLE BULLET POINTS - Use hyphens (-) only
5. NO SPECIAL CHARACTERS - Avoid symbols ATS can't parse
6. DATE FORMAT - Use "Month Year" or "MM/YYYY" consistently
7. CONTACT INFO AT TOP - Name, email, phone on separate lines
8. KEYWORDS - Use exact keywords from job description
9. QUANTIFY ACHIEVEMENTS - Numbers, percentages, dollar amounts
10. ACTION VERBS - Start bullets with strong action verbs

FORMATTING DON'TS:
- Margins smaller than 1 inch
- Font smaller than 10pt
- Personal pronouns (I, me, we)
- Photos or graphics
- Headers/footers (ATS may not read them)
- Fancy fonts or colors
"""


def get_action_verbs_for_role(role_title: str) -> list[str]:
    """
    Get relevant action verbs based on role type.
    
    Maps common role types to appropriate skill categories.
    """
    role_lower = role_title.lower()
    
    # Map role types to verb categories
    if any(x in role_lower for x in ["engineer", "developer", "programmer", "architect"]):
        categories = ["technical", "research", "detail_oriented"]
    elif any(x in role_lower for x in ["manager", "director", "lead", "head"]):
        categories = ["leadership", "communication", "financial"]
    elif any(x in role_lower for x in ["analyst", "scientist", "researcher"]):
        categories = ["research", "detail_oriented", "technical"]
    elif any(x in role_lower for x in ["designer", "creative", "artist", "writer"]):
        categories = ["creative", "communication", "detail_oriented"]
    elif any(x in role_lower for x in ["sales", "marketing", "business"]):
        categories = ["communication", "leadership", "financial"]
    elif any(x in role_lower for x in ["teacher", "instructor", "trainer"]):
        categories = ["teaching", "communication", "leadership"]
    else:
        categories = ["leadership", "communication", "detail_oriented"]
    
    # Collect verbs from relevant categories
    verbs = []
    for cat in categories:
        verbs.extend(ACTION_VERBS.get(cat, []))
    
    return list(set(verbs))  # Remove duplicates


def get_template_for_experience_level(years_of_experience: int) -> str:
    """
    Select appropriate template based on experience level.
    
    - Entry-level (0-2 years): Functional or Combination
    - Mid-level (3-7 years): Chronological
    - Senior (8+ years): Chronological or Combination
    """
    if years_of_experience <= 2:
        return COMBINATION_TEMPLATE  # Emphasize skills over limited experience
    else:
        return CHRONOLOGICAL_TEMPLATE  # Standard, preferred by most employers


def validate_ats_compliance(resume_text: str) -> list[str]:
    """
    Check resume text for ATS compliance issues.
    
    Returns list of warnings/suggestions.
    """
    warnings = []
    
    # Check for words to avoid
    for word in WORDS_TO_AVOID:
        if word.lower() in resume_text.lower():
            warnings.append(f"Consider replacing '{word}' with specific achievements")
    
    # Check for personal pronouns
    pronouns = ["I ", " me ", " my ", " we ", " our "]
    for pronoun in pronouns:
        if pronoun.lower() in resume_text.lower():
            warnings.append("Remove personal pronouns (I, me, my, we, our)")
            break
    
    # Check for common symbols that may not parse
    problem_chars = ["•", "→", "★", "●", "■", "▪"]
    for char in problem_chars:
        if char in resume_text:
            warnings.append(f"Replace special character '{char}' with standard bullet (-)")
            break
    
    return warnings
