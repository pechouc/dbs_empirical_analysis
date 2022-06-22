import os
import time

import numpy as np
import pandas as pd


def get_preprocessed_trade_data():

    path_to_dir = os.path.dirname(__file__)

    dataframes = {
        year: pd.read_csv(
            os.path.join(path_to_dir, 'data', 'BACI_HS12_V202201', f'BACI_HS12_Y{year}_V202201.csv')
        ) for year in [2016, 2017, 2018, 2019]
    }

    long_df = pd.concat(list(dataframes.values()))

    df = long_df.groupby(
        ['t', 'i', 'j']
    ).agg(
        {'v': 'sum'}
    ).reset_index()

    country_codes = pd.read_csv('data/BACI_HS12_V202201/country_codes_V202201.csv', encoding='latin')

    country_codes_imputed = {
        490: 'OASIA',
        697: 'EFTA',
        849: 'USPAC'
    }

    df = df.merge(
        country_codes[['country_code', 'iso_3digit_alpha']],
        how='left',
        left_on='i', right_on='country_code'
    )

    df['iso_3digit_alpha_EXPORTER'] = df.apply(
        lambda row: country_codes_imputed.get(row['i'], row['iso_3digit_alpha']),
        axis=1
    )

    df = df.drop(columns=['country_code', 'iso_3digit_alpha', 'i'])

    df = df.merge(
        country_codes[['country_code', 'iso_3digit_alpha']],
        how='left',
        left_on='j', right_on='country_code'
    )

    df['iso_3digit_alpha_IMPORTER'] = df.apply(
        lambda row: country_codes_imputed.get(row['j'], row['iso_3digit_alpha']),
        axis=1
    )

    df = df.drop(columns=['country_code', 'iso_3digit_alpha', 'j'])

    return df.copy()


def get_preprocessed_gravity_data():

    path_to_dir = os.path.dirname(__file__)
    path_to_data = os.path.join(path_to_dir, 'data')
    file_name = os.path.join(path_to_data, 'Gravity_csv_V202202', 'Gravity_V202202.csv')

    if 'gravity_dtypes.csv' not in os.listdir(path_to_data):
        gravity = pd.read_csv(file_name)

        gravity.dtypes.to_csv(os.path.join(path_to_data, 'gravity_dtypes.csv'))

    else:
        dtypes = pd.read_csv(
            os.path.join(path_to_data, 'gravity_dtypes.csv')
        ).set_index(
            'Unnamed: 0'
        ).to_dict()['0']

        gravity = pd.read_csv(file_name, dtype=dtypes)

    gravity = gravity[gravity['year'].isin([2016, 2017, 2018, 2019])].copy()

    gravity = gravity[
        [
            'year', 'iso3_o', 'iso3_d', 'country_exists_o', 'country_exists_d',
            'dist', 'contig', 'comlang_off', 'comlang_ethno', 'comcol', 'col45', 'rta'
        ]
    ].copy()

    gravity = gravity[
        np.logical_and(
            gravity['country_exists_d'] == 1,
            gravity['country_exists_o'] == 1
        )
    ].copy()
    gravity = gravity.drop(columns=['country_exists_o', 'country_exists_d'])

    gravity = gravity[gravity['iso3_o'] != gravity['iso3_d']].copy()

    gravity['log_dist'] = np.log(gravity['dist'])

    gravity = gravity.rename(
        columns={
            'year': 't',
            'iso3_o': 'iso_3digit_alpha_EXPORTER',
            'iso3_d' : 'iso_3digit_alpha_IMPORTER'
        }
    )

    return gravity.copy()


def get_merged_data():
    df = get_preprocessed_trade_data()
    gravity = get_preprocessed_gravity_data()

    merged_df = df.merge(
        gravity,
        on=['t', 'iso_3digit_alpha_EXPORTER', 'iso_3digit_alpha_IMPORTER'],
        how='left'
    )

    merged_df = merged_df.dropna()

    return merged_df.copy()


if __name__ == '__main__':
    print('Loading and preprocessing the data')
    start_time = time.time()

    merged_df = get_merged_data()

    end_time = time.time()
    print('Output saved!')
    print(f'Computation time: ', round(end_time - start_time), 'seconds')

    merged_df.to_csv('foreign_market_access_data.csv', index=False)
