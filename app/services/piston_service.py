import requests

PISTON_URL = "https://emkc.org/api/v2/piston/execute"

# Map our language names to Piston's language + version identifiers
LANG_MAP = {
    "python": {
        "language": "python",
        "version": "3.10.0",
    },
    "javascript": {
        "language": "javascript",
        "version": "18.15.0",
    },
}


def run_code(language: str, code: str, stdin: str = "") -> dict:
    """
    Send code to the Piston API and return the execution result.

    Args:
        language: "python" or "javascript"
        code:     The student's source code as a string
        stdin:    The test case input to feed via standard input

    Returns a dict with keys:
        stdout  — program output
        stderr  — error output (if any)
        code    — exit code (0 = success)
        time    — execution time in seconds
    """
    if language not in LANG_MAP:
        raise ValueError(f"Unsupported language: {language}. Use 'python' or 'javascript'.")

    lang_cfg = LANG_MAP[language]

    payload = {
        "language": lang_cfg["language"],
        "version": lang_cfg["version"],
        "files": [{"content": code}],
        "stdin": stdin or "",
        "run_timeout": 5000,       # 5 seconds max runtime
        "compile_timeout": 10000,  # 10 seconds max compile
        "run_memory_limit": 128,   # 128 MB
    }

    try:
        resp = requests.post(PISTON_URL, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        return {"stdout": "", "stderr": "Execution timed out.", "code": 1, "time": 0}
    except requests.exceptions.RequestException as e:
        return {"stdout": "", "stderr": f"Piston API error: {str(e)}", "code": 1, "time": 0}

    run = data.get("run", {})
    return {
        "stdout": run.get("stdout", ""),
        "stderr": run.get("stderr", ""),
        "code": run.get("code", 1),
        "time": run.get("time", 0),
    }
