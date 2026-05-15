from evals.run_app_eval import EvalCase, check_case


def test_check_case_detects_required_and_forbidden() -> None:
    case = EvalCase(
        id="x",
        prompt="prompt",
        required=["timeout"],
        forbidden=["requests.get(url) without timeout"],
    )

    passed = check_case(case, "requests.get(url, timeout=10)")
    failed = check_case(case, "requests.get(url) without timeout")

    assert passed["passed"]
    assert not failed["passed"]
    assert failed["present_forbidden"]
