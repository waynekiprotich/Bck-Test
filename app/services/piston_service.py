import requests

PISTON_URL = "https://emkc.org/api/v2/piston/execute"

# map our frontend language names to the exact versions Piston expects
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
    if language not in LANG_MAP:
        raise ValueError(f"Unsupported language: {language}. Use 'python' or 'javascript'.")

    lang_cfg = LANG_MAP[language]

    # securely execute the user's code using the external piston api
    payload = {
        "language": lang_cfg["language"],
        "version": lang_cfg["version"],
        "files": [{"content": code}],
        "stdin": stdin or "",
        "run_timeout": 5000,      # ms
        "compile_timeout": 10000, # ms
        "run_memory_limit": 128,  # mb
    }

    try:
        # give the request 15 seconds before we assume it's stuck and give up
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