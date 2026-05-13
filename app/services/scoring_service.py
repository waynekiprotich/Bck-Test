from app.services.piston_service import run_code
from app.extensions import db


def evaluate_submission(submission, challenge, test_cases):
    passed = 0
    total = len(test_cases)
    last_stdout = ""
    last_stderr = ""
    last_time = 0.0
    per_test_results = []

    for tc in test_cases:
        output = run_code(
            language=submission.language,
            code=submission.code,
            stdin=tc.input_data or "",
        )

        actual = output["stdout"].strip()
        expected = tc.expected_output.strip()
        last_stdout = output["stdout"]
        last_stderr = output["stderr"]
        last_time = max(last_time, output.get("time", 0))

        if output["stderr"]:
            tc_status = "Runtime Error"
        elif actual == expected:
            tc_status = "Accepted"
            passed += 1
        else:
            tc_status = "Wrong Answer"

        per_test_results.append({
            "test_case_id": tc.id,
            "passed": tc_status == "Accepted",
            "status": tc_status,
            "is_hidden": tc.is_hidden,
            "expected": expected if not tc.is_hidden else None,
            "actual": actual if not tc.is_hidden else None,
        })

    # figure out how many points they get based on their pass ratio
    ratio = passed / total if total > 0 else 0
    score = int(ratio * challenge.points_reward)

    # give them an extra 50 points if they beat the active weekly challenge
    from app.models.challenge import WeeklyChallenge
    is_weekly = WeeklyChallenge.query.filter_by(
        challenge_id=challenge.id, is_active=True
    ).first()
    
    if is_weekly and passed == total and total > 0:
        score += 50

    # figure out the overall status for the submission
    if last_stderr:
        final_status = "Runtime Error"
    elif passed == total and total > 0:
        final_status = "Accepted"
    else:
        final_status = "Wrong Answer"

    # save the results back to the db model
    submission.status = final_status
    submission.score = score
    submission.passed_tests = passed
    submission.total_tests = total
    submission.stdout = last_stdout
    submission.stderr = last_stderr
    submission.execution_time = round(last_time, 4)

    return {
        "status": final_status,
        "score": score,
        "passed_tests": passed,
        "total_tests": total,
        "results": per_test_results,
    }


def update_user_points(user, score: int):
    # only update if they actually earned points, then recalculate rank
    if score > 0:
        user.points += score
        user.calculate_rank()
        db.session.commit()