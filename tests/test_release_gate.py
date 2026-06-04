from fimrf.model_development.release_gate import decide_release


def test_release_gate_pass_and_block():
    status, reasons = decide_release({"kupiec_exception_rate": 0.01, "kupiec_p_value": 0.5}, 0.0, 12)
    assert status == "PASS"
    status2, _ = decide_release({"kupiec_exception_rate": 0.05, "kupiec_p_value": 0.01}, 0.0, 12)
    assert status2 == "BLOCK"
