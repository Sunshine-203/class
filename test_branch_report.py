from branch_report import flag_large_withdrawals, format_kwd


def test_amount_above_threshold_is_flagged():
    data = [{"amount_kwd": 15000}]
    assert flag_large_withdrawals(data) == data


def test_amount_below_threshold_is_not_flagged():
    data = [{"amount_kwd": 9999.999}]
    assert flag_large_withdrawals(data) == []


def test_amount_exactly_at_threshold_is_flagged():
    data = [{"amount_kwd": 10000}]
    assert flag_large_withdrawals(data) == data


def test_custom_threshold_boundary_is_flagged():
    data = [{"amount_kwd": 500}]
    assert flag_large_withdrawals(data, threshold=500) == data


def test_format_kwd_uses_three_decimals():
    assert format_kwd(10000) == "10,000.000 KWD"
