import os
import json

import numpy as np
import pandas as pd

path_to_dir = os.path.dirname(__file__)
path_to_data = os.path.join(path_to_dir, 'data')

path_to_codes_to_impute_IRS = os.path.join(path_to_data, 'codes_to_impute_IRS.json')
path_to_industry_names_mapping = os.path.join(path_to_data, 'industry_names_mapping.json')

with open(path_to_codes_to_impute_IRS) as file:
    CODES_TO_IMPUTE_IRS = json.loads(file.read())

with open(path_to_industry_names_mapping) as file:
    industry_names_mapping = json.loads(file.read())


def impute_missing_codes(row, column, codes_to_impute):
    if row['AFFILIATE_COUNTRY_NAME'] in codes_to_impute.keys():
        return codes_to_impute[row['AFFILIATE_COUNTRY_NAME']][column]

    else:
        return row[column]


def get_multiplier_to_2021(year, growth_rates):
    col_name = f'uprusd21{year - 2000}'

    return growth_rates.loc[0, col_name]


def preprocess_aggregate_US_CbCR_data(positive_profits=False):
    # Loading the data
    dataframes = {}

    path_to_geographies = os.path.join(path_to_data, 'geographies.csv')
    geographies = pd.read_csv(path_to_geographies)

    for year in [2016, 2017, 2018, 2019, 2020]:

        if not positive_profits:
            path_to_file = os.path.join(path_to_data, 'irs', f'{year - 2000}it01acbc.xlsx')
        else:
            path_to_file = os.path.join(path_to_data, 'irs', f'{year - 2000}it01bcbc.xlsx')

        irs = pd.read_excel(
            path_to_file,
            engine='openpyxl'
        )

        irs = irs.drop(
            columns=list(irs.columns[12:])
        )

        irs.columns = [
            'AFFILIATE_COUNTRY_NAME',
            'NB_REPORTING_MNEs',
            'UNRELATED_PARTY_REVENUES', 'RELATED_PARTY_REVENUES', 'TOTAL_REVENUES',
            'PROFIT_BEFORE_TAX', 'TAXES_PAID', 'TAXES_ACCRUED',
            'STATED_CAPITAL', 'ACCUM_EARNINGS', 'NB_EMPLOYEES', 'TANGIBLE_ASSETS'
        ]

        irs = irs.loc[5:].copy()

        mask_stateless = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'stateless' in country_name.lower()
        )
        mask_total = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'total' in country_name.lower()
        )
        mask = ~np.logical_or(
            mask_stateless, mask_total
        )

        irs = irs[mask].copy()

        irs = irs.iloc[:-4].copy()

        # We rename fields of the form "Other [+ CONTINENT_NAME]"
        irs['AFFILIATE_COUNTRY_NAME'] = irs['AFFILIATE_COUNTRY_NAME'].map(
            (
                lambda country_name: ('Other ' + country_name.split(',')[0]).replace('&', 'and')
                if 'other' in country_name.lower() else country_name
            )
        )

        # We deal with a few specific country names
        irs['AFFILIATE_COUNTRY_NAME'] = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Bosnia and Herzegovina' if 'Bosnia' in country_name else country_name
        )
        irs['AFFILIATE_COUNTRY_NAME'] = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Ivory Coast' if 'Ivory' in country_name else country_name
        )
        irs['AFFILIATE_COUNTRY_NAME'] = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'United Kingdom' if 'United Kingdom' in country_name else country_name
        )
        irs['AFFILIATE_COUNTRY_NAME'] = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Korea' if country_name.startswith('Korea') else country_name
        )
        irs['AFFILIATE_COUNTRY_NAME'] = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Congo' if country_name.endswith('(Brazzaville)') else country_name
        )
        irs['AFFILIATE_COUNTRY_NAME'] = irs['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'US Virgin Islands' if country_name == 'U.S. Virgin Islands' else country_name
        )

        irs.reset_index(drop=True, inplace=True)

        merged_df = irs.merge(
            geographies[['NAME', 'CODE']],
            how='left',
            left_on='AFFILIATE_COUNTRY_NAME', right_on='NAME'
        )

        for column in ['NAME', 'CODE']:
            merged_df[column] = merged_df.apply(
                lambda row: impute_missing_codes(
                    row=row,
                    column=column,
                    codes_to_impute=CODES_TO_IMPUTE_IRS
                ),
                axis=1
            )

        merged_df.drop(columns=['NAME', 'AFFILIATE_COUNTRY_NAME'], inplace=True)

        merged_df['YEAR'] = year

        dataframes[year] = merged_df.copy()

    irs = pd.concat(list(dataframes.values()))

    if positive_profits:
        return irs.copy()

    else:

        # Merging with the positive profits sample
        posprofits_sample = preprocess_aggregate_US_CbCR_data(positive_profits=True)

        posprofits_sample = posprofits_sample.rename(
            columns={
                'PROFIT_BEFORE_TAX': 'PROFIT_BEFORE_TAX_POSPROFITS',
                'TAXES_PAID': 'TAXES_PAID_POSPROFITS',
                'TAXES_ACCRUED': 'TAXES_ACCRUED_POSPROFITS'
            }
        )

        posprofits_sample = posprofits_sample[
            [
                'CODE', 'YEAR',
                'PROFIT_BEFORE_TAX_POSPROFITS',
                'TAXES_PAID_POSPROFITS',
                'TAXES_ACCRUED_POSPROFITS'
            ]
        ].copy()

        irs = irs.merge(
            posprofits_sample,
            on=['CODE', 'YEAR'],
            how='left'
        )

        # for col in ['PROFIT_BEFORE_TAX', 'TAXES_PAID', 'TAXES_ACCRUED']:
        #     col_posprofits = col + '_POSPROFITS'

        #     irs[col_posprofits] = irs.apply(
        #         lambda row: row[col] if np.isnan(row[col_posprofits]) else row[col_posprofits],
        #         axis=1
        #     )

        # Adding columns with multipliers
        path_to_growth_rates = os.path.join(path_to_data, 'gdpgrowth.xlsx')

        growth_rates = pd.read_excel(path_to_growth_rates, engine='openpyxl')

        irs['MULTIPLIER'] = irs['YEAR'].map(lambda year: get_multiplier_to_2021(year, growth_rates))
        irs['MULTIPLIER'] *= (irs['PROFIT_BEFORE_TAX'] > 0) * 1

        for column in ['PROFIT_BEFORE_TAX', 'TAXES_ACCRUED', 'TAXES_PAID']:
            new_column = column + '_UPGRADED'

            irs[new_column] = irs[column] * irs['MULTIPLIER']

        irs['MULTIPLIER_POSPROFITS'] = irs['YEAR'].map(lambda year: get_multiplier_to_2021(year, growth_rates))
        irs['MULTIPLIER_POSPROFITS'] *= (irs['PROFIT_BEFORE_TAX_POSPROFITS'] > 0) * 1

        for column in ['PROFIT_BEFORE_TAX_POSPROFITS', 'TAXES_ACCRUED_POSPROFITS', 'TAXES_PAID_POSPROFITS']:
            new_column = column + '_UPGRADED'

            irs[new_column] = irs[column] * irs['MULTIPLIER']

        # Adding average Effective Tax Rates (ETRs) - Full sample
        temp = irs.groupby(
            'CODE'
        ).agg(
            {
                'PROFIT_BEFORE_TAX_UPGRADED': 'sum',
                'TAXES_PAID_UPGRADED': 'sum',
                'TAXES_ACCRUED_UPGRADED': 'sum'
            }
        ).reset_index()

        temp['AVERAGE_ETR_CASH'] = temp['TAXES_PAID_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100
        temp['AVERAGE_ETR_ACCRUED'] = temp['TAXES_ACCRUED_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100

        temp['AVERAGE_ETR_CASH'] = temp['AVERAGE_ETR_CASH'].map(lambda x: max(x, 0))
        temp['AVERAGE_ETR_ACCRUED'] = temp['AVERAGE_ETR_ACCRUED'].map(lambda x: max(x, 0))

        irs = irs.merge(
            temp[['CODE', 'AVERAGE_ETR_CASH', 'AVERAGE_ETR_ACCRUED']],
            on='CODE',
            how='left'
        )

        # Adding average Effective Tax Rates (ETRs) excluding the year being considered - Full sample
        temp_dataframes = {}

        for year in [2016, 2017, 2018, 2019, 2020]:
            temp = irs[irs['YEAR'] != year].copy()

            temp = temp.groupby(
                'CODE'
            ).agg(
                {
                    'PROFIT_BEFORE_TAX_UPGRADED': 'sum',
                    'TAXES_PAID_UPGRADED': 'sum',
                    'TAXES_ACCRUED_UPGRADED': 'sum'
                }
            ).reset_index()

            temp['AVERAGE_ETR_CASH_EXCL'] = temp['TAXES_PAID_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100
            temp['AVERAGE_ETR_ACCRUED_EXCL'] = temp['TAXES_ACCRUED_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100

            temp['AVERAGE_ETR_CASH_EXCL'] = temp['AVERAGE_ETR_CASH_EXCL'].map(lambda x: max(x, 0))
            temp['AVERAGE_ETR_ACCRUED_EXCL'] = temp['AVERAGE_ETR_ACCRUED_EXCL'].map(lambda x: max(x, 0))

            temp['YEAR'] = year

            temp_dataframes[year] = temp

        temp = pd.concat(list(temp_dataframes.values()))

        irs = irs.merge(
            temp[['CODE', 'YEAR', 'AVERAGE_ETR_CASH_EXCL', 'AVERAGE_ETR_ACCRUED_EXCL']],
            on=['CODE', 'YEAR'],
            how='left'
        )

        # Adding current year ETRs - Full sample
        irs['ETR_CASH'] = irs['TAXES_PAID'] / irs['PROFIT_BEFORE_TAX'] * 100
        irs['ETR_ACCRUED'] = irs['TAXES_ACCRUED'] / irs['PROFIT_BEFORE_TAX'] * 100

        irs['ETR_CASH'] = irs['ETR_CASH'].map(lambda x: max(x, 0))
        irs['ETR_ACCRUED'] = irs['ETR_ACCRUED'].map(lambda x: max(x, 0))

        # Adding previous year ETRs - Full sample
        temp = irs[['CODE', 'YEAR', 'ETR_CASH', 'ETR_ACCRUED']].copy()

        temp['YEAR'] += 1

        temp = temp.rename(
            columns={
                'ETR_CASH': 'ETR_CASH_PREVIOUS_YEAR',
                'ETR_ACCRUED': 'ETR_ACCRUED_PREVIOUS_YEAR'
            }
        )

        irs = irs.merge(
            temp,
            on=['CODE', 'YEAR'],
            how='left'
        )

        # Adding average Effective Tax Rates (ETRs) - Positive-profits sub-sample
        temp = irs.groupby(
            'CODE'
        ).agg(
            {
                'PROFIT_BEFORE_TAX_POSPROFITS_UPGRADED': 'sum',
                'TAXES_PAID_POSPROFITS_UPGRADED': 'sum',
                'TAXES_ACCRUED_POSPROFITS_UPGRADED': 'sum'
            }
        ).reset_index()

        temp['AVERAGE_ETR_CASH_POSPROFITS'] = (
            temp['TAXES_PAID_POSPROFITS_UPGRADED'] / temp['PROFIT_BEFORE_TAX_POSPROFITS_UPGRADED']
        ) * 100
        temp['AVERAGE_ETR_ACCRUED_POSPROFITS'] = (
            temp['TAXES_ACCRUED_POSPROFITS_UPGRADED'] / temp['PROFIT_BEFORE_TAX_POSPROFITS_UPGRADED']
        ) * 100

        temp['AVERAGE_ETR_CASH_POSPROFITS'] = temp['AVERAGE_ETR_CASH_POSPROFITS'].map(lambda x: max(x, 0))
        temp['AVERAGE_ETR_ACCRUED_POSPROFITS'] = temp['AVERAGE_ETR_ACCRUED_POSPROFITS'].map(lambda x: max(x, 0))

        irs = irs.merge(
            temp[['CODE', 'AVERAGE_ETR_CASH_POSPROFITS', 'AVERAGE_ETR_ACCRUED_POSPROFITS']],
            on='CODE',
            how='left'
        )

        # Adding average Effective Tax Rates (ETRs) excluding the year being considered - Positive-profits sub-sample
        temp_dataframes = {}

        for year in [2016, 2017, 2018, 2019, 2020]:
            temp = irs[irs['YEAR'] != year].copy()

            temp = temp.groupby(
                'CODE'
            ).agg(
                {
                    'PROFIT_BEFORE_TAX_POSPROFITS_UPGRADED': 'sum',
                    'TAXES_PAID_POSPROFITS_UPGRADED': 'sum',
                    'TAXES_ACCRUED_POSPROFITS_UPGRADED': 'sum'
                }
            ).reset_index()

            temp['AVERAGE_ETR_CASH_EXCL_POSPROFITS'] = (
                temp['TAXES_PAID_POSPROFITS_UPGRADED'] / temp['PROFIT_BEFORE_TAX_POSPROFITS_UPGRADED']
            ) * 100
            temp['AVERAGE_ETR_ACCRUED_EXCL_POSPROFITS'] = (
                temp['TAXES_ACCRUED_POSPROFITS_UPGRADED'] / temp['PROFIT_BEFORE_TAX_POSPROFITS_UPGRADED']
            ) * 100

            temp['AVERAGE_ETR_CASH_EXCL_POSPROFITS'] = temp['AVERAGE_ETR_CASH_EXCL_POSPROFITS'].map(
                lambda x: max(x, 0)
            )
            temp['AVERAGE_ETR_ACCRUED_EXCL_POSPROFITS'] = temp['AVERAGE_ETR_ACCRUED_EXCL_POSPROFITS'].map(
                lambda x: max(x, 0)
            )

            temp['YEAR'] = year

            temp_dataframes[year] = temp

        temp = pd.concat(list(temp_dataframes.values()))

        irs = irs.merge(
            temp[['CODE', 'YEAR', 'AVERAGE_ETR_CASH_EXCL_POSPROFITS', 'AVERAGE_ETR_ACCRUED_EXCL_POSPROFITS']],
            on=['CODE', 'YEAR'],
            how='left'
        )

        # Adding current year ETRs - Positive-profits sub-sample
        irs['ETR_CASH_POSPROFITS'] = irs['TAXES_PAID_POSPROFITS'] / irs['PROFIT_BEFORE_TAX_POSPROFITS'] * 100
        irs['ETR_ACCRUED_POSPROFITS'] = irs['TAXES_ACCRUED_POSPROFITS'] / irs['PROFIT_BEFORE_TAX_POSPROFITS'] * 100

        irs['ETR_CASH_POSPROFITS'] = irs['ETR_CASH_POSPROFITS'].map(lambda x: max(x, 0))
        irs['ETR_ACCRUED_POSPROFITS'] = irs['ETR_ACCRUED_POSPROFITS'].map(lambda x: max(x, 0))

        # Adding previous year ETRs - Full sample
        temp = irs[['CODE', 'YEAR', 'ETR_CASH_POSPROFITS', 'ETR_ACCRUED_POSPROFITS']].copy()

        temp['YEAR'] += 1

        temp = temp.rename(
            columns={
                'ETR_CASH_POSPROFITS': 'ETR_CASH_PREVIOUS_YEAR_POSPROFITS',
                'ETR_ACCRUED_POSPROFITS': 'ETR_ACCRUED_PREVIOUS_YEAR_POSPROFITS'
            }
        )

        irs = irs.merge(
            temp,
            on=['CODE', 'YEAR'],
            how='left'
        )

        # Selecting the relevant columns
        irs = irs[
            [
                'CODE', 'YEAR',
                'NB_REPORTING_MNEs',
                'UNRELATED_PARTY_REVENUES', 'RELATED_PARTY_REVENUES', 'TOTAL_REVENUES', 'PROFIT_BEFORE_TAX',
                'STATED_CAPITAL', 'ACCUM_EARNINGS', 'NB_EMPLOYEES', 'TANGIBLE_ASSETS',
                'AVERAGE_ETR_ACCRUED', 'AVERAGE_ETR_CASH',
                'AVERAGE_ETR_CASH_EXCL', 'AVERAGE_ETR_ACCRUED_EXCL',
                'ETR_CASH', 'ETR_ACCRUED',
                'ETR_CASH_PREVIOUS_YEAR', 'ETR_ACCRUED_PREVIOUS_YEAR',
                'AVERAGE_ETR_ACCRUED_POSPROFITS', 'AVERAGE_ETR_CASH_POSPROFITS',
                'AVERAGE_ETR_CASH_EXCL_POSPROFITS', 'AVERAGE_ETR_ACCRUED_EXCL_POSPROFITS',
                'ETR_CASH_POSPROFITS', 'ETR_ACCRUED_POSPROFITS',
                'ETR_CASH_PREVIOUS_YEAR_POSPROFITS', 'ETR_ACCRUED_PREVIOUS_YEAR_POSPROFITS',
            ]
        ].copy()

        return irs.copy()


def preprocess_per_industry_US_CbCR_data():
    # Loading the data
    dataframes = {}

    path_to_geographies = os.path.join(path_to_data, 'geographies.csv')
    geographies = pd.read_csv(path_to_geographies)

    for year in [2016, 2017, 2018, 2019, 2020]:

        path_to_file = os.path.join(path_to_data, 'irs', f'{year - 2000}it02cbc.xlsx')


        if year != 2020:
            data = pd.read_excel(
                path_to_file,
                engine='openpyxl'
            )

        else:
            data = pd.read_excel(
                path_to_file,
                engine='openpyxl',
                sheet_name='Table 2 No Disclosure'
            )

        # Eliminating irrelevant columns and rows
        data = data[data.columns[:13]].copy()

        data.columns = [
            'INDUSTRY',
            'AFFILIATE_COUNTRY_NAME',
            'NB_REPORTING_MNEs',
            'UNRELATED_PARTY_REVENUES',
            'RELATED_PARTY_REVENUES',
            'TOTAL_REVENUES',
            'PROFIT_BEFORE_TAX',
            'TAXES_PAID',
            'TAXES_ACCRUED',
            'STATED_CAPITAL',
            'ACCUM_EARNINGS',
            'NB_EMPLOYEES',
            'TANGIBLE_ASSETS'
        ]

        data = data[
            data.isnull().sum(axis=1) != len(data.columns)
        ].copy()
        data = data.iloc[4:-7].copy()

        data.reset_index(drop=True, inplace=True)

        data['INDUSTRY'] = data['INDUSTRY'].ffill()

        data = data[
            ~data['AFFILIATE_COUNTRY_NAME'].isin(['All jurisdictions', 'Stateless entities and other country'])
        ].copy()

        data = data[
            ~data['AFFILIATE_COUNTRY_NAME'].map(
                lambda country_name: 'total' in country_name.lower()
            )
        ].copy()

        data = data[
            data.drop(columns=['NB_REPORTING_MNEs']).applymap(
                lambda x: isinstance(x, str) and x == 'd'
            ).sum(axis=1) == 0
        ].copy()

        data['AFFILIATE_COUNTRY_NAME'] = data['AFFILIATE_COUNTRY_NAME'].map(
            (
                lambda country_name: f'Other {country_name.split(",")[0].replace("&", "and")}'
                if 'other' in country_name.lower() else country_name
            )
        )

        data['AFFILIATE_COUNTRY_NAME'] = data['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Bosnia and Herzegovina' if 'Bosnia' in country_name else country_name
        )
        data['AFFILIATE_COUNTRY_NAME'] = data['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Ivory Coast' if 'Ivory' in country_name else country_name
        )
        data['AFFILIATE_COUNTRY_NAME'] = data['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'United Kingdom' if 'United Kingdom' in country_name else country_name
        )
        data['AFFILIATE_COUNTRY_NAME'] = data['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Korea' if country_name.startswith('Korea') else country_name
        )
        data['AFFILIATE_COUNTRY_NAME'] = data['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'Congo' if country_name.endswith('(Brazzaville)') else country_name
        )
        data['AFFILIATE_COUNTRY_NAME'] = data['AFFILIATE_COUNTRY_NAME'].map(
            lambda country_name: 'US Virgin Islands' if country_name == 'U.S. Virgin Islands' else country_name
        )

        data = data.merge(
            geographies[['NAME', 'CODE']],
            how='left',
            left_on='AFFILIATE_COUNTRY_NAME', right_on='NAME'
        )

        data.drop(columns=['NAME'], inplace=True)

        data['CODE'] = data.apply(
            (
                lambda row: 'OASIAOCN' if isinstance(row['CODE'], float) and np.isnan(row['CODE'])
                and row['AFFILIATE_COUNTRY_NAME'] == 'Other Asia and Oceania' else row['CODE']
            ),
            axis=1
        )

        data.reset_index(drop=True, inplace=True)

        # Renaming industries for convenience
        data['INDUSTRY'] = data['INDUSTRY'].map(
            lambda industry: industry_names_mapping.get(industry, industry)
        )

        data['YEAR'] = year

        dataframes[year] = data.copy()

    df = pd.concat(list(dataframes.values()))

    # Adding average Effective Tax Rates (ETRs) - Aggregate level
    path_to_growth_rates = os.path.join(path_to_data, 'gdpgrowth.xlsx')

    growth_rates = pd.read_excel(path_to_growth_rates, engine='openpyxl')

    df['MULTIPLIER'] = df['YEAR'].map(lambda year: get_multiplier_to_2021(year, growth_rates))
    df['MULTIPLIER'] *= (df['PROFIT_BEFORE_TAX'] > 0) * 1

    for column in ['PROFIT_BEFORE_TAX', 'TAXES_ACCRUED', 'TAXES_PAID']:
        new_column = column + '_UPGRADED'

        df[new_column] = df[column] * df['MULTIPLIER']

    temp = df.groupby(
        'CODE'
    ).agg(
        {
            'PROFIT_BEFORE_TAX_UPGRADED': 'sum',
            'TAXES_PAID_UPGRADED': 'sum',
            'TAXES_ACCRUED_UPGRADED': 'sum'
        }
    ).reset_index()

    temp['AVERAGE_ETR_CASH'] = temp['TAXES_PAID_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100
    temp['AVERAGE_ETR_ACCRUED'] = temp['TAXES_ACCRUED_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100

    temp['AVERAGE_ETR_CASH'] = temp['AVERAGE_ETR_CASH'].map(lambda x: max(x, 0))
    temp['AVERAGE_ETR_ACCRUED'] = temp['AVERAGE_ETR_ACCRUED'].map(lambda x: max(x, 0))

    df = df.merge(
        temp[['CODE', 'AVERAGE_ETR_CASH', 'AVERAGE_ETR_ACCRUED']],
        on='CODE',
        how='left'
    )

    # Adding average Effective Tax Rates (ETRs) excluding the year being considered - Aggregate level
    temp_dataframes = {}

    for year in [2016, 2017, 2018, 2019, 2020]:
        temp = df[df['YEAR'] != year].copy()

        temp = temp.groupby(
            'CODE'
        ).agg(
            {
                'PROFIT_BEFORE_TAX_UPGRADED': 'sum',
                'TAXES_PAID_UPGRADED': 'sum',
                'TAXES_ACCRUED_UPGRADED': 'sum'
            }
        ).reset_index()

        temp['AVERAGE_ETR_CASH_EXCL'] = temp['TAXES_PAID_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100
        temp['AVERAGE_ETR_ACCRUED_EXCL'] = temp['TAXES_ACCRUED_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100

        temp['AVERAGE_ETR_CASH_EXCL'] = temp['AVERAGE_ETR_CASH_EXCL'].map(lambda x: max(x, 0))
        temp['AVERAGE_ETR_ACCRUED_EXCL'] = temp['AVERAGE_ETR_ACCRUED_EXCL'].map(lambda x: max(x, 0))

        temp['YEAR'] = year

        temp_dataframes[year] = temp

    temp = pd.concat(list(temp_dataframes.values()))

    df = df.merge(
        temp[['CODE', 'YEAR', 'AVERAGE_ETR_CASH_EXCL', 'AVERAGE_ETR_ACCRUED_EXCL']],
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding current year ETRs - Aggregate level
    temp = df[['CODE', 'YEAR', 'PROFIT_BEFORE_TAX_UPGRADED', 'TAXES_PAID_UPGRADED', 'TAXES_ACCRUED_UPGRADED']].copy()

    temp = temp.groupby(['CODE', 'YEAR']).sum().reset_index()

    temp['ETR_CASH'] = temp['TAXES_PAID_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100
    temp['ETR_ACCRUED'] = temp['TAXES_ACCRUED_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100

    temp['ETR_CASH'] = temp['ETR_CASH'].map(lambda x: max(x, 0))
    temp['ETR_ACCRUED'] = temp['ETR_ACCRUED'].map(lambda x: max(x, 0))

    df = df.merge(
        temp[['CODE', 'YEAR', 'ETR_CASH', 'ETR_ACCRUED']],
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding previous year ETRs - Aggregate level
    temp = df[['CODE', 'YEAR', 'INDUSTRY', 'ETR_CASH', 'ETR_ACCRUED']].copy()

    temp['YEAR'] += 1

    temp = temp.rename(
        columns={
            'ETR_CASH': 'ETR_CASH_PREVIOUS_YEAR',
            'ETR_ACCRUED': 'ETR_ACCRUED_PREVIOUS_YEAR'
        }
    )

    df = df.merge(
        temp,
        on=['CODE', 'YEAR', 'INDUSTRY'],
        how='left'
    )

    # Adding average Effective Tax Rates (ETRs) - Industry level
    temp = df.groupby(
        ['CODE', 'INDUSTRY']
    ).agg(
        {
            'PROFIT_BEFORE_TAX_UPGRADED': 'sum',
            'TAXES_PAID_UPGRADED': 'sum',
            'TAXES_ACCRUED_UPGRADED': 'sum'
        }
    ).reset_index()

    temp['AVERAGE_ETR_CASH_INDUS'] = temp['TAXES_PAID_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100
    temp['AVERAGE_ETR_ACCRUED_INDUS'] = temp['TAXES_ACCRUED_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100

    temp['AVERAGE_ETR_CASH_INDUS'] = temp['AVERAGE_ETR_CASH_INDUS'].map(lambda x: max(x, 0))
    temp['AVERAGE_ETR_ACCRUED_INDUS'] = temp['AVERAGE_ETR_ACCRUED_INDUS'].map(lambda x: max(x, 0))

    df = df.merge(
        temp[['CODE', 'INDUSTRY', 'AVERAGE_ETR_CASH_INDUS', 'AVERAGE_ETR_ACCRUED_INDUS']],
        on=['CODE', 'INDUSTRY'],
        how='left'
    )

    # Adding average Effective Tax Rates (ETRs) excluding the year being considered - Industry level
    temp_dataframes = {}

    for year in [2016, 2017, 2018, 2019, 2020]:
        temp = df[df['YEAR'] != year].copy()

        temp = temp.groupby(
            ['CODE', 'INDUSTRY']
        ).agg(
            {
                'PROFIT_BEFORE_TAX_UPGRADED': 'sum',
                'TAXES_PAID_UPGRADED': 'sum',
                'TAXES_ACCRUED_UPGRADED': 'sum'
            }
        ).reset_index()

        temp['AVERAGE_ETR_CASH_EXCL_INDUS'] = temp['TAXES_PAID_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED'] * 100
        temp['AVERAGE_ETR_ACCRUED_EXCL_INDUS'] = (
            temp['TAXES_ACCRUED_UPGRADED'] / temp['PROFIT_BEFORE_TAX_UPGRADED']
        ) * 100

        temp['AVERAGE_ETR_CASH_EXCL_INDUS'] = temp['AVERAGE_ETR_CASH_EXCL_INDUS'].map(lambda x: max(x, 0))
        temp['AVERAGE_ETR_ACCRUED_EXCL_INDUS'] = temp['AVERAGE_ETR_ACCRUED_EXCL_INDUS'].map(lambda x: max(x, 0))

        temp['YEAR'] = year

        temp_dataframes[year] = temp

    temp = pd.concat(list(temp_dataframes.values()))

    df = df.merge(
        temp[['CODE', 'YEAR', 'INDUSTRY', 'AVERAGE_ETR_CASH_EXCL_INDUS', 'AVERAGE_ETR_ACCRUED_EXCL_INDUS']],
        on=['CODE', 'YEAR', 'INDUSTRY'],
        how='left'
    )

    # Adding current year ETRs - Industry level
    df['ETR_CASH_INDUS'] = df.apply(
        lambda row: row['TAXES_PAID'] / row['PROFIT_BEFORE_TAX'] * 100 if row['PROFIT_BEFORE_TAX'] > 0 else np.nan,
        axis=1
    )
    df['ETR_ACCRUED_INDUS'] = df.apply(
        lambda row: row['TAXES_ACCRUED'] / row['PROFIT_BEFORE_TAX'] * 100 if row['PROFIT_BEFORE_TAX'] > 0 else np.nan,
        axis=1
    )

    df['ETR_CASH_INDUS'] = df['ETR_CASH_INDUS'].map(lambda x: max(x, 0))
    df['ETR_ACCRUED_INDUS'] = df['ETR_ACCRUED_INDUS'].map(lambda x: max(x, 0))

    # Adding previous year ETRs - Industry level
    temp = df[['CODE', 'YEAR', 'INDUSTRY', 'ETR_CASH_INDUS', 'ETR_ACCRUED_INDUS']].copy()

    temp['YEAR'] += 1

    temp = temp.rename(
        columns={
            'ETR_CASH_INDUS': 'ETR_CASH_PREVIOUS_YEAR_INDUS',
            'ETR_ACCRUED_INDUS': 'ETR_ACCRUED_PREVIOUS_YEAR_INDUS'
        }
    )

    df = df.merge(
        temp,
        on=['CODE', 'YEAR', 'INDUSTRY'],
        how='left'
    )

    df = df[
        [
            'CODE', 'YEAR', 'INDUSTRY',
            'NB_REPORTING_MNEs',
            'UNRELATED_PARTY_REVENUES', 'RELATED_PARTY_REVENUES', 'TOTAL_REVENUES', 'PROFIT_BEFORE_TAX',
            'STATED_CAPITAL', 'ACCUM_EARNINGS', 'NB_EMPLOYEES', 'TANGIBLE_ASSETS',
            'AVERAGE_ETR_ACCRUED', 'AVERAGE_ETR_CASH',
            'AVERAGE_ETR_CASH_EXCL', 'AVERAGE_ETR_ACCRUED_EXCL',
            'ETR_CASH', 'ETR_ACCRUED',
            'ETR_CASH_PREVIOUS_YEAR', 'ETR_ACCRUED_PREVIOUS_YEAR',
            'AVERAGE_ETR_ACCRUED_INDUS', 'AVERAGE_ETR_CASH_INDUS',
            'AVERAGE_ETR_CASH_EXCL_INDUS', 'AVERAGE_ETR_ACCRUED_EXCL_INDUS',
            'ETR_CASH_INDUS', 'ETR_ACCRUED_INDUS',
            'ETR_CASH_PREVIOUS_YEAR_INDUS', 'ETR_ACCRUED_PREVIOUS_YEAR_INDUS',
        ]
    ].copy()

    agg_irs = preprocess_aggregate_US_CbCR_data()

    agg_irs = agg_irs[
        [
            'CODE', 'YEAR',
            'AVERAGE_ETR_ACCRUED_POSPROFITS', 'AVERAGE_ETR_CASH_POSPROFITS',
            'AVERAGE_ETR_CASH_EXCL_POSPROFITS', 'AVERAGE_ETR_ACCRUED_EXCL_POSPROFITS',
            'ETR_CASH_POSPROFITS', 'ETR_ACCRUED_POSPROFITS',
            'ETR_CASH_PREVIOUS_YEAR_POSPROFITS', 'ETR_ACCRUED_PREVIOUS_YEAR_POSPROFITS',
        ]
    ].copy()

    df = df.merge(
        agg_irs,
        on=['CODE', 'YEAR'],
        how='left'
    )

    return df.copy()


def preprocess_bilateral_aggregate_CbCR_data():

    path_to_file = os.path.join(path_to_data, 'oecd_cbcr.csv')
    oecd = pd.read_csv(path_to_file)

    oecd = oecd[oecd['PAN'] == 'PANELA'].copy()

    oecd = oecd.drop(
        columns=[
            'PAN', 'Grouping',
            'Ultimate Parent Jurisdiction', 'Partner Jurisdiction',
            'Variable', 'Year',
            'Flag Codes', 'Flags'
        ]
    )

    oecd = oecd.pivot(
        index=['COU', 'JUR', 'YEA'],
        columns=['CBC'],
        values='Value'
    ).reset_index()

    oecd = oecd[
        [
            'COU', 'JUR', 'YEA',
            'UPR', 'RPR', 'TOT_REV',
            'PROFIT',
            'CBCR_COUNT',
            'STATED_CAPITAL', 'EARNINGS', 'EMPLOYEES', 'ASSETS'
        ]
    ].copy()

    ser = oecd.groupby('COU').nunique()['JUR']
    parents_with_sufficient_details = ser[ser >= 60 + 2].index

    oecd = oecd[oecd['COU'].isin(parents_with_sufficient_details)].copy()

    # Adding current ETRs computed based on the positive-profit sub-sample
    temp = pd.read_csv(path_to_file)

    temp = temp[temp['PAN'] == 'PANELAI'].copy()

    temp = temp.drop(
        columns=[
            'PAN', 'Grouping',
            'Ultimate Parent Jurisdiction', 'Partner Jurisdiction',
            'Variable', 'Year',
            'Flag Codes', 'Flags'
        ]
    )

    temp = temp.pivot(
        index=['COU', 'JUR', 'YEA'],
        columns=['CBC'],
        values='Value'
    ).reset_index()

    temp = temp[
        [
            'COU', 'JUR', 'YEA',
            'PROFIT', 'TAX_PAID', 'TAX_ACCRUED'
        ]
    ].copy()

    temp['ETR_CASH_POSPROFITS'] = temp['TAX_PAID'] / temp['PROFIT'] * 100
    temp['ETR_ACCRUED_POSPROFITS'] = temp['TAX_ACCRUED'] / temp['PROFIT'] * 100

    temp['ETR_CASH_POSPROFITS'] = temp['ETR_CASH_POSPROFITS'].map(lambda x: max(x, 0))
    temp['ETR_ACCRUED_POSPROFITS'] = temp['ETR_ACCRUED_POSPROFITS'].map(lambda x: max(x, 0))

    oecd = oecd.merge(
        temp,
        how='left',
        on=['COU', 'JUR', 'YEA']
    )

    # Adding previous year ETRs computed based on the positive-profit sub-sample
    temp['YEA'] += 1

    temp = temp.rename(
        columns={
            'ETR_CASH_POSPROFITS': 'ETR_CASH_PREVIOUS_YEAR_POSPROFITS',
            'ETR_ACCRUED_POSPROFITS': 'ETR_ACCRUED_PREVIOUS_YEAR_POSPROFITS',
        }
    )

    oecd = oecd.merge(
        temp,
        how='left',
        on=['COU', 'JUR', 'YEA']
    )

    # Last step - Renaming columns
    oecd = oecd.rename(
        columns={
            'COU': 'PARENT_COUNTRY_CODE',
            'JUR': 'PARTNER_COUNTRY_CODE',
            'YEA': 'YEAR',
            'UPR': 'UNRELATED_PARTY_REVENUES',
            'RPR': 'RELATED_PARTY_REVENUES',
            'TOT_REV': 'TOTAL_REVENUES',
            'PROFIT': 'PROFIT_BEFORE_TAX',
            'CBCR_COUNT': 'NB_REPORTING_MNEs',
            'EARNINGS': 'ACCUM_EARNINGS',
            'EMPLOYEES': 'NB_EMPLOYEES',
            'ASSETS': 'TANGIBLE_ASSETS'
        }
    )

    return oecd.copy()
