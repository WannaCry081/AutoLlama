import re

DEFAULT_BUCKET = "general"

CODE_HINTS = re.compile(
    r"```|"
    r"\b(code|function|class|method|bug|refactor|debug|stack ?trace|implement|"
    r"compile|lint|unit ?test|regex|sql|api|endpoint|typescript|javascript|"
    r"python|rust|golang|\bgo\b|java|kotlin|swift|c\+\+|c#|bash|shell)\b|"
    r"\.(py|ts|tsx|js|jsx|go|rs|java|kt|swift|cpp|cs|sh|sql)\b",
    re.IGNORECASE,
)

REASON_HINTS = re.compile(
    r"\b(prove|theorem|derive|step[- ]by[- ]step|reason|reasoning|"
    r"why does|explain why|math|equation|integral|derivative|logic|"
    r"puzzle|riddle|calculate|deduce|chain[- ]of[- ]thought)\b",
    re.IGNORECASE,
)

CLASSIFIER_PROMPT = """\
You are a request router. Classify the user's prompt into ONE bucket.
Reply with exactly one lowercase word, no punctuation, no explanation:

- coder     : programming, debugging, code review, software design, devops
- reasoner  : math, multi-step logic, formal proofs, hard puzzles
- fast      : short, simple, conversational, small talk
- general   : everything else (knowledge, writing, brainstorming, summarising)

User prompt:
\"\"\"{prompt}\"\"\"

One word:"""
