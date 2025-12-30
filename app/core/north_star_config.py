# north_star_config.py

"""
NORTH STAR CONFIGURATION
------------------------
This file governs the baseline logic for the Contract AI. 
It applies to ALL personas and ALL roles.
"""

# 1. GLOBAL GUIDANCE
# These rules apply to the entire document, regardless of the section.
GLOBAL_GUIDANCE = """
1. **Governing Law**: Ensure the governing law is always New York or Delaware. Flag anything else.
2. **Clarity**: Prefer active voice. Break up run-on sentences longer than 4 lines.
3. **Defined Terms**: Ensure capitalized terms (e.g., "Services", "Data") are actually defined or standard.
4. **Dates**: Flag any hardcoded dates that have already passed.
"""

# 2. SECTION-SPECIFIC GUIDANCE
# The AI will check if a paragraph falls into these categories. 
# If it does, it applies these specific rules ON TOP of the persona instructions.
SECTION_MAP = {
    "Indemnification": """
        - We do NOT accept uncapped indemnification for "all claims."
        - Limit to third-party claims only.
        - Ensure mutual indemnification for IP infringement.
    """,
    "Limitation of Liability": """
        - Cap must not exceed 12 months of fees paid.
        - Carve-outs are only acceptable for: Fraud, Gross Negligence, and Willful Misconduct.
        - Reject 'Lost Profits' exclusions if they are direct damages.
    """,
    "Termination": """
        - We require at least 30 days' notice for termination for convenience.
        - Ensure we have the right to retrieve data for 60 days post-termination.
    """,
    "Confidentiality": """
        - Definition must include "all business and technical information."
        - Exceptions must include "independently developed" and "already known."
        - Duration should be at least 3 years, or perpetual for trade secrets.
    """
}