import re


secret_patterns = [
    re.compile(r'''api[_-]?key\s*[:=]\s*["'][^"']+["']''', re.IGNORECASE),
    re.compile(r'''token\s*[:=]\s*["'][^"']+["']''', re.IGNORECASE),
    re.compile(r'''secret\s*[:=]\s*["'][^"']+["']''', re.IGNORECASE),
    re.compile(r'''password\s*[:=]\s*["'][^"']+["']''', re.IGNORECASE),
    re.compile(r'''api_[a-z0-9]+''', re.IGNORECASE),
]


def redact_secrets(input_text):
    output = input_text

    for pattern in secret_patterns:
        output = pattern.sub("[REDACTED_SECRET]", output)

    return output