from lusha_exercise.utils.geographic_utils import get_region_name


def test_get_region_name():
    assert get_region_name('spain ') == 'Europe'
    assert get_region_name('Spain') == 'Europe'
    assert get_region_name('island') == 'Europe'
    assert get_region_name('netherlands antilles') == 'Europe'
    assert get_region_name('côte d’ivoire') == 'Africa'
    assert get_region_name('côte d\'ivoire') == 'Africa'
    assert get_region_name('macedonia') == 'Europe'
    assert get_region_name('Macedonia ') == 'Europe'
    assert get_region_name('palestine ') == 'Asia'
    assert get_region_name('Palestine') == 'Asia'
    assert get_region_name('Palestine State') == 'Asia'
    assert get_region_name('israel') == 'Asia'
    assert get_region_name('Israel') == 'Asia'
    assert get_region_name('new ziland') == 'Oceania'
    assert get_region_name('usa') == 'Americas'
    assert get_region_name('United states') == 'North America'
    assert get_region_name('United states of america') == 'North America'
    assert get_region_name('canada') == 'North America'
    assert get_region_name('vietnam') == 'Asia'
    assert get_region_name('japan') == 'Asia'
    assert get_region_name('uk') == 'Europe'
    assert get_region_name('Britain') == 'Europe'
    assert get_region_name('britain') == 'Europe'
    assert get_region_name('Australia') == 'Oceania'
    assert get_region_name('australia') == 'Oceania'
    assert get_region_name('Netherlands') == 'Europe'
    assert get_region_name('netherlands') == 'Europe'
    assert get_region_name('british virgin islands') == 'North America'
