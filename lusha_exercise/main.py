import os
import sys

from lusha_exercise.company_manager import CompanyManager
from lusha_exercise.utils.iteration_utils import iterate_records


def update_company_manager_with_record(company_manager, record):
    """
    Update the company manager with the record data.
    """
    company_manager.companies_count += 1
    company_manager.update_field_names_counter(record)
    company_manager.update_companies_keywords(record)
    company_manager.update_company_range(record)
    company_manager.update_european_countries_companies_map_if_necessary(record)


def write_results(company_manager, resource_folder):
    """
    Write the company_manager result analysis to the disk.
    """
    company_manager.write_companies_field_to_csv(company_manager.companies_keywords.items(),
                                                 ['Company Name', 'Keywords'],
                                                 os.path.join(resource_folder, 'companies_keywords.csv'))
    company_manager.write_companies_field_to_csv(company_manager.companies_ranges.items(), ['Company Name', 'Range'],
                                                 os.path.join(resource_folder, 'companies_ranges.csv'))
    company_manager.write_companies_field_to_csv(company_manager.european_countries_companies.items(),
                                                 ['Country', 'Companies Count'],
                                                 os.path.join(resource_folder, 'european_countries_companies.csv'))
    company_manager.write_companies_field_to_csv(company_manager.field_names_counter.items(),
                                                 ['Field', 'Count'], os.path.join(resource_folder, 'data_points.csv'))


def main():
    resource_json_file_path = sys.argv[1]
    resource_folder = os.path.join(os.path.dirname(__file__), 'resources')

    company_manager = CompanyManager()
    records = iterate_records(resource_json_file_path)
    for record in records:
        update_company_manager_with_record(company_manager, record)
        if company_manager.companies_count > 10000:
            break
    company_manager.update_field_names_counter_to_store_percent()
    write_results(company_manager, resource_folder)


if __name__ == '__main__':
    main()
