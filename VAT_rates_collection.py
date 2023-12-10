import os
import re

import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

path_to_dir = os.path.dirname(__file__)
path_to_data = os.path.join(path_to_dir, 'data')


def convert_or_NA(row):
    try:
        return float(row['VAT_RATE'])
    except:
        if row['VAT_RATE'] == 'NA':
            return 0

        elif len(re.findall(pattern='(\d+\.\d+) \(', string=row['VAT_RATE'])) > 0:
            return re.findall(pattern='(\d+\.\d+) \(', string=row['VAT_RATE'])[0]

        elif len(re.findall(pattern='(\d+) \(', string=row['VAT_RATE'])) > 0:
            return re.findall(pattern='(\d+) \(', string=row['VAT_RATE'])[0]

        elif len(re.findall(pattern=': (\d+\.\d+)', string=row['VAT_RATE'])) > 0:
            return re.findall(pattern=': (\d+\.\d+)', string=row['VAT_RATE'])[0]

        elif len(re.findall(pattern=': (\d+)', string=row['VAT_RATE'])) > 0:
            return re.findall(pattern=': (\d+)', string=row['VAT_RATE'])[0]

        else:
            return np.nan

def get_VAT_rates():
    # Fetching the PWC rates
    response = requests.get("https://taxsummaries.pwc.com/quick-charts/value-added-tax-vat-rates")

    soup = BeautifulSoup(response.content, 'lxml')

    table = soup.find('table')

    VAT_rates = {}

    for elt in table.find_all('tr', class_='territoryQuickCharts'):
        VAT_rates[elt.find('a').text] = elt.find_all('td')[1].text

    # A few specific cases that we treat separately

    # We remove Iraq from the dictionary
    VAT_rates.pop('Iraq')

    # https://worldpopulationreview.com/state-rankings/sales-tax-by-state
    # The average combined sales tax is 6.35%
    VAT_rates['United States'] = 6.35

    # https://www.oecd.org/tax/consumption/consumption-tax-trends-canada.pdf
    # The Canadian standard GST rate is 5.0%
    VAT_rates['Canada'] = 5

    VAT_rates['Brazil'] = 17

    # Building a DataFrame from the scrapped VAT rates
    df = pd.DataFrame.from_dict(VAT_rates, orient='index').reset_index()

    df = df.rename(
        columns={
            'index': 'COUNTRY',
            0: 'VAT_RATE'
        }
    )

    # Cleaning the VAT rates
    corrected_df = df.copy()
    corrected_df['VAT_RATE'] = corrected_df.apply(convert_or_NA, axis=1)

    manual_imputations = {
        'Chad': 18,
        "China, People's Republic of": 13,
        'Fiji': 9,
        'India': 18,
        'Myanmar': 5,
        'Pakistan': 17,
        'Taiwan': 5
    }
    corrected_df['VAT_RATE'] = corrected_df.apply(
        lambda row: manual_imputations.get(row['COUNTRY'], row['VAT_RATE']),
        axis=1
    )

    # Adding country codes
    geographies = pd.read_csv(os.path.join(path_to_data, 'geographies.csv'))

    corrected_df['COUNTRY'] = corrected_df['COUNTRY'].map(
        lambda name: name[:name.find(',')] if name.find(',') >= 0 and not name.startswith('Congo') else name
    )

    country_name_imputations = {
        'Hong Kong SAR': 'Hong Kong',
        "Ivory Coast (Côte d'Ivoire)": 'Ivory Coast',
        'Lao PDR': 'Laos',
        'Macau SAR': 'Macau',
        'Palestinian territories': 'State of Palestine'
    }
    corrected_df['COUNTRY'] = corrected_df['COUNTRY'].map(
        lambda name: country_name_imputations.get(name, name)
    )

    corrected_df = corrected_df.merge(
        geographies[['NAME', 'CODE']],
        how='left',
        left_on='COUNTRY', right_on='NAME'
    ).drop(columns='NAME')

    # Final formatting steps
    corrected_df = corrected_df.rename(
        columns={
            'CODE': 'COUNTRY_CODE'
        }
    )

    return corrected_df[['COUNTRY_CODE', 'VAT_RATE']].reset_index(drop=True)
