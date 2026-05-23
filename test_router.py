"""Quick sanity check: hit /v1/chat/completions with prompts that should
route to each bucket and print which model the router picked."""
import httpx

BASE = "http://localhost:8000/v1"

CASES = [
    ("coder",    "Write a Python function that debounces an async callable."),
    ("reasoner", "Prove that the square root of 2 is irrational, step by step."),
    ("fast",     "hey, how are you?"),
    ("general",  "Summarise the plot of Dune in three sentences for a 10-year-old."),
]

for expected, prompt in CASES:
    r = httpx.post(
        f"{BASE}/chat/completions",
        json={
            "model": "auto",
            "stream": False,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=300,
    )
    info = r.json().get("x_router", {})
    print(f"[{expected:8s}] -> bucket={info.get('bucket'):10s} model={info.get('model')}")
