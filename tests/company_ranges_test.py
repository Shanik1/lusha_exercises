from lusha_exercise.utils.company_ranges_utils import get_company_range, INVALID_COMPANY_APPROXIMATE_MESSAGE


def test_company_ranges_calculation():
    assert get_company_range(0) == '0-10'
    assert get_company_range(5) == '0-10'
    assert get_company_range(8) == '0-10'
    assert get_company_range(10) == '0-10'
    assert get_company_range(11) == '11-50'
    assert get_company_range(23) == '11-50'
    assert get_company_range(50) == '11-50'
    assert get_company_range(51) == '51-200'
    assert get_company_range(80) == '51-200'
    assert get_company_range(200) == '51-200'
    assert get_company_range(201) == '201-500'
    assert get_company_range(500) == '201-500'
    assert get_company_range(501) == '501-1000'
    assert get_company_range(700) == '501-1000'
    assert get_company_range(1000) == '501-1000'
    assert get_company_range(1001) == '1001-5000'
    assert get_company_range(3002) == '1001-5000'
    assert get_company_range(5000) == '1001-5000'
    assert get_company_range(5001) == '5001-10000'
    assert get_company_range(9000) == '5001-10000'
    assert get_company_range(10000) == '5001-10000'
    assert get_company_range(10001) == '10000+'
    assert get_company_range(120000) == '10000+'


def test_corner_cases_range_calculations():
    assert get_company_range(-16) == INVALID_COMPANY_APPROXIMATE_MESSAGE
    assert get_company_range(-500) == INVALID_COMPANY_APPROXIMATE_MESSAGE
