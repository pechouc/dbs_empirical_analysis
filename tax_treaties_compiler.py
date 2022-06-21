import os

import re

import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

import pycountry


url_base = 'https://eoi-tax.com'

path_to_dir = os.path.dirname(os.path.abspath(__file__))
path_to_data = os.path.join(path_to_dir, 'data')


def get_one_jurisdiction_data(href):
    response = requests.get(url_base + href)

    soup = BeautifulSoup(response.content, 'lxml')

    tables = soup.find_all('table', class_='table table-hover table-condensed table-responsive')

    table = str(tables[0])
    table = table.replace('\n', '')

    new_list = []
    pattern = '<span class="flag-icon flag-icon-.."></span></td>'

    for elt in re.split('<td rowspan="\d">', table):
        if re.match(pattern, elt):
            continue
        else:
            new_list.append(elt)

    data = {
        'partner_jurisdiction': [],
        'agreement_type': [],
        'agreement': [],
        'signed': [],
        'entered_into_force': [],
        'eoi': []
    }

    for elt in new_list[1:]:
        temp = elt.split('<td>')

        jurisdiction = temp[0]
        jurisdiction = jurisdiction[jurisdiction.find('>') + 1:jurisdiction[1:].find('<') + 1]

        elt = temp[1:].copy()

        for i in range(0, int(len(elt) / 5)):
            agreement_type = elt[i * 5 + 0]
            agreement = elt[i * 5 + 1]
            signed = elt[i * 5 + 2]
            entered_into_force = elt[i * 5 + 3]
            eoi = elt[i * 5 + 4]

            agreement_type = agreement_type[agreement_type.find('>') + 1:agreement_type[1:].find('<') + 1]
            agreement = agreement[agreement.find('>') + 1:agreement[1:].find('<') + 1]
            signed = signed.replace('</td>', '')
            entered_into_force = entered_into_force.replace('</td>', '')
            eoi = eoi[:eoi.find('<')]

            data['partner_jurisdiction'].append(jurisdiction)
            data['agreement_type'].append(agreement_type)
            data['agreement'].append(agreement)
            data['signed'].append(signed)
            data['entered_into_force'].append(entered_into_force)
            data['eoi'].append(eoi)

    return pd.DataFrame(data)


def get_all_jurisdictions_data():
    output = []

    response = requests.get(url_base + '/jurisdictions/')
    soup = BeautifulSoup(response.content, 'lxml')

    for col in soup.find_all(class_='col-md-2'):
        for country in col.find_all('a'):
            country_name = country.text.replace('\n', '')
            country_iso2_code = re.findall('flag-icon-(..)', str(country))[0]

            data = get_one_jurisdiction_data(country.get('href'))

            data['parent_jurisdiction_name'] = country_name
            data['parent_jurisdiction_iso2_code'] = country_iso2_code

            output.append(data)

    df = pd.concat(output)

    df['partner_jurisdiction'] = df['partner_jurisdiction'].map(
        lambda country_name: 'British Virgin Islands' if country_name == 'Virgin Islands (British)' else country_name
    )
    df['partner_jurisdiction'] = df['partner_jurisdiction'].map(
        lambda country_name: 'Democratic Republic of the Congo' if country_name == 'Congo (the Democratic Republic of the)' else country_name
    )
    df['partner_jurisdiction'] = df['partner_jurisdiction'].map(
        lambda country_name: 'State of Palestine' if country_name == 'Palestine, State of' else country_name
    )

    path_to_geographies = os.path.join(path_to_data, 'geographies.csv')
    geographies = pd.read_csv(path_to_geographies)

    df = df.merge(
        geographies[['NAME', 'CODE']],
        how='left',
        left_on='partner_jurisdiction',
        right_on='NAME'
    )

    codes_to_impute = {
        'Bonaire, Sint Eustatius and Saba': 'BES',
        'Falkland Islands [Malvinas]': 'FLK',
        'Réunion': 'REU',
        'Holy See': 'VAT'
    }

    df['CODE'] = df.apply(
        lambda row: codes_to_impute.get(row['partner_jurisdiction'], row['CODE']),
        axis=1
    )

    df = df.drop(columns=['NAME'])
    df = df.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE'
        }
    )

    df['parent_jurisdiction_iso3_code'] = df['parent_jurisdiction_iso2_code'].map(
        lambda code: pycountry.countries.get(alpha_2=code.upper()).alpha_3
    )

    df = df.rename(
        columns={
            'parent_jurisdiction_iso3_code': 'PARENT_COUNTRY_CODE'
        }
    )
    df = df.drop(columns=['parent_jurisdiction_name', 'partner_jurisdiction', 'parent_jurisdiction_iso2_code'])

    df['signed'] = pd.to_datetime(df['signed'])

    df['entered_into_force'] = df['entered_into_force'].map(lambda x: np.nan if x == 'No' else x)
    df['entered_into_force'] = pd.to_datetime(df['entered_into_force'])

    return df.copy()


if __name__ == '__main__':
    df = get_all_jurisdictions_data()

    df.to_csv(os.path.join(path_to_data, 'tax_treaties.csv'), index=False)
