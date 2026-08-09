# Word-boundary regex patterns, matched case-insensitively against
# description + location combined text.

WORK_MODE_PATTERNS = {
    "Remote": [
        r"\bremote\b",
        r"\bwork\s?from\s?home\b",
        r"\bwfh\b",
    ],
    "Hybrid": [
        r"\bhybrid\b",
    ],
    "Onsite": [
        r"\bon-?site\b",
        r"\bin-?office\b",
        r"\bwork\s?from\s?office\b",
        r"\bwfo\b",
    ],
}