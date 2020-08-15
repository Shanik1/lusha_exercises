import countryinfo
import pycountry
from pycountry_convert.convert_continent_code_to_continent_name import convert_continent_code_to_continent_name
from pycountry_convert.convert_country_alpha2_to_continent_code import country_alpha2_to_continent_code

SPECIAL_COUNTIES_WHITE_LIST = {'netherlands antilles': 'Europe'}


def get_region_name(country_name: str):
    """
    Return the country's region. For example, for Spain, will return Europe.
    """
    try:
        country_name = country_name.strip()
        country = pycountry.countries.get(name=country_name) or pycountry.countries.get(
            official_name=country_name) or pycountry.historic_countries.get(
            name=country_name)
        if country is not None:
            return convert_continent_code_to_continent_name(country_alpha2_to_continent_code(country.alpha_2))
        try:
            return countryinfo.countryinfo.CountryInfo(country_name=country_name).region()
        except KeyError:
            country = _find_country_by_iterate_all_relevant_countries(country, country_name)
            return convert_continent_code_to_continent_name(
                country_alpha2_to_continent_code(country.alpha_2))
    except Exception as error:
        return SPECIAL_COUNTIES_WHITE_LIST.get(country_name)


def _find_country_by_iterate_all_relevant_countries(country, country_name):
    """
    Iterate the all the countries and historic countries that the pycountry module supports, and try to match
    the country name to the module supported names.
    Try to handle with the fallowing cases:
        - The name is partial - for example, the country_name is Palestine, and the pycountry official name for
        Palestine is 'the State of Palestine'.
        - The characters are a bit different - for example - 'côte d’ivoire', which is saved as 'Côte d\'Ivoire'
        in pycountry.
        - The order ot the words is different - for example - for 'british virgin islands', the pycountry
        value is 'Virgin Islands, British'

    :return: the country that match to the country name, if found.
    :rtype: pycountry.countries.Country|None
    """
    possible_countries = [country for country in
                          list(pycountry.countries) + list(pycountry.historic_countries) if
                          country_name.lower() in country.name.lower() or (hasattr(country, 'official_name') and
                                                                           country_name.lower() in
                                                                           country.official_name.lower())]
    if len(possible_countries) > 0:
        country = possible_countries[0]
    else:
        possible_countries = [country for country in
                              list(pycountry.countries) + list(pycountry.historic_countries) if
                              country_name.split(" ")[0].lower() in country.name.lower()]
        if len(possible_countries) > 0:
            country = possible_countries[0]
    return country
