COMPANIES_MAX_SIZES = [-1, 10, 50, 200, 500, 1000, 5000, 10000]
MAX_COMPANY_RANGE = COMPANIES_MAX_SIZES[-1]
INVALID_COMPANY_APPROXIMATE_MESSAGE = 'Invalid company approximate'


def get_company_range_field(employee_range_fields: dict):
    """
    Extract the relevant range field, for the get_company_range method.
    """
    total_fields = filter(lambda key: 'total' in key, employee_range_fields)
    latest_version_range_field = sorted(total_fields, key=lambda key: int(key[1:key.index('_')]), reverse=True)
    return latest_version_range_field[0]


def get_company_range(company_approximate: int):
    """
    Return the range to which the company belongs.
    """
    if company_approximate >= 0:
        if company_approximate <= MAX_COMPANY_RANGE:
            return _find_relevant_company_range(0, len(COMPANIES_MAX_SIZES) - 1, company_approximate)
        return str(MAX_COMPANY_RANGE) + '+'
    return INVALID_COMPANY_APPROXIMATE_MESSAGE


def _find_relevant_company_range(start_index, end_index, company_approximate):
    """
    Return the relevant company range.
    """
    if end_index - start_index == 1:
        return str(COMPANIES_MAX_SIZES[start_index] + 1) + '-' + str(COMPANIES_MAX_SIZES[end_index])
    middle_index = (end_index + start_index) // 2
    if COMPANIES_MAX_SIZES[middle_index] < company_approximate:
        return _find_relevant_company_range(middle_index, end_index, company_approximate)
    elif COMPANIES_MAX_SIZES[middle_index] > company_approximate:
        return _find_relevant_company_range(start_index, middle_index, company_approximate)
    else:
        return str(COMPANIES_MAX_SIZES[middle_index - 1] + 1) + '-' + str(COMPANIES_MAX_SIZES[middle_index])
