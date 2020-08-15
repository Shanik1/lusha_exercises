import os
import pickle
from collections import Counter

from pandas import DataFrame

from lusha_exercise.enums.records_fields import RecordsFields
from lusha_exercise.utils.company_ranges_utils import get_company_range_field, get_company_range
from lusha_exercise.utils.filtering_utils import get_clean_description
from lusha_exercise.utils.geographic_utils import get_region_name
from lusha_exercise.utils.keywords_utils import create_model, get_keywords

RESOURCE_FOLDER = os.path.join(os.path.dirname(__file__), 'resources')


class CompanyManager:
    """
    Execute the company records data.
    """

    def __init__(self):
        self.companies_count = 0
        self.field_names_counter = Counter()
        self.european_countries_companies = Counter()
        self.companies_ranges = {}
        self.companies_keywords = {}
        self.companies_descriptions = {}
        self.count_vectorizer = pickle.load(
            open(os.path.join(RESOURCE_FOLDER, 'stemmer_count_vectorizer.pickle'), 'rb'))
        self.tfidf_transformer = pickle.load(
            open(os.path.join(RESOURCE_FOLDER, 'stemmer_tfidf_transformer.pickle'), 'rb'))

    def update_field_names_counter(self, record):
        self.field_names_counter.update([key for key, value in record.items() if value])

    def update_company_range(self, record):
        company_name = record[RecordsFields.COMPANY_NAME.value]
        company_rage_field = get_company_range_field(record[RecordsFields.COMPANY_SIZE.value])
        self.companies_ranges[company_name] = get_company_range(
            int(record[RecordsFields.COMPANY_SIZE.value][company_rage_field]))

    def update_european_countries_companies_map_if_necessary(self, record):
        """
        Update the european countries companies map, if the country is from Europe.
        """
        country_name = record[RecordsFields.COUNTRY.value]
        if country_name:
            continent_name = get_region_name(country_name)
            if continent_name == 'Europe':
                self.european_countries_companies.update([country_name.lower()])

    def update_companies_descriptions(self, record):
        if record.get(RecordsFields.DESCRIPTION.value) is not None:
            description = get_clean_description(record[RecordsFields.DESCRIPTION.value])
        else:
            description = ''
        self.companies_descriptions[record[RecordsFields.COMPANY_NAME.value]] = description

    def update_companies_keywords(self, record):
        if record.get(RecordsFields.DESCRIPTION.value) is not None:
            description = get_clean_description(record[RecordsFields.DESCRIPTION.value])
        else:
            description = ''
        self.set_company_keywords(record[RecordsFields.COMPANY_NAME.value], description)

    def set_model(self):
        """
        Set the ftidf model from the description values for later keyword extraction.
        """
        count_vectorizer, tfidf_transformer = create_model(filter(None, self.companies_descriptions.values()))
        self.count_vectorizer = count_vectorizer
        self.tfidf_transformer = tfidf_transformer

    def set_companies_keywords(self):
        """
        Set the companies description keywords.
        """
        for company, description in self.companies_descriptions.items():
            if description:
                self.set_company_keywords(company, description)

    def set_company_keywords(self, company, description):
        """
        Set the company keywords.
        """
        self.companies_keywords[company] = ', '.join(
            get_keywords(self.count_vectorizer, self.tfidf_transformer,
                         description))

    def update_field_names_counter_to_store_percent(self):
        self.field_names_counter = {field_name: str(count / self.companies_count * 100)[:3] + '%'
                                    for field_name, count in self.field_names_counter.items()}

    @staticmethod
    def write_companies_field_to_csv(company_items, columns, csv_path):
        df = DataFrame(company_items, columns=columns)
        df.to_csv(csv_path)
