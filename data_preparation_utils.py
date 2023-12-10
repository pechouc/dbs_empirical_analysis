import os

import numpy as np
import pandas as pd

path_to_dir = os.path.dirname(__file__)
path_to_data = os.path.join(path_to_dir, 'data')


def pick_relevant_ETR(row, ETR_type='A'):
    if not np.isnan(row[f'E{ETR_type}TR_x']):
        return row[f'E{ETR_type}TR_x']

    elif not np.isnan(row[f'E{ETR_type}TR_y']):
        return row[f'E{ETR_type}TR_x']

    else:
        return np.nan


def get_foreign_market_access():
    foreign_market_access = pd.read_csv(os.path.join(path_to_dir, 'foreign_market_access.csv'))

    foreign_market_access['YEAR'] = foreign_market_access['exp_x_y_FE'].map(
        lambda x: x.split('_')[0]
    ).astype(int)

    foreign_market_access['CODE'] = foreign_market_access['exp_x_y_FE'].map(
        lambda x: x.split('_')[2]
    ).astype(str)

    foreign_market_access = foreign_market_access.drop(columns=['exp_x_y_FE'])

    foreign_market_access = foreign_market_access.rename(columns={'variable_to_sum': 'FMA'})

    lagged_foreign_market_access = foreign_market_access.copy()
    lagged_foreign_market_access['YEAR'] += 1
    lagged_foreign_market_access = lagged_foreign_market_access.rename(
        columns={'FMA': 'LAGGED_FMA'}
    )

    foreign_market_access = foreign_market_access.merge(
        lagged_foreign_market_access,
        how='left',
        on=['CODE', 'YEAR']
    )

    return foreign_market_access.copy()


def get_WOE_GDP_data():
    path_to_file = os.path.join(path_to_data, 'WEOOct2021all.xlsx')

    woe = pd.read_excel(path_to_file, engine='openpyxl')

    woe = woe[woe['WEO Subject Code'] == 'NGDPD'].copy()

    woe = woe.drop(
        columns=[
            'WEO Country Code', 'WEO Subject Code', 'Country', 'Subject Notes',
            'Subject Descriptor', 'Units', 'Country/Series-specific Notes',
        ]
    )
    woe = woe.reset_index(drop=True)

    woe = woe[['ISO', 2016, 2017, 2018, 2019, 2020]].copy()

    for year in [2016, 2017, 2018, 2019, 2020]:
        woe[year] = woe[year].map(lambda x: x.replace(',', '') if isinstance(x, str) else x)
        woe[year] = woe[year].astype(float) * 10**9

    long_df = woe[['ISO', 2016]].rename(columns={2016: 'NGDPD'})
    long_df['YEAR'] = 2016

    for year in [2017, 2018, 2019, 2020]:
        df = woe[['ISO', year]].rename(columns={year: 'NGDPD'})
        df['YEAR'] = year
        long_df = pd.concat([long_df, df], axis=0)

    long_df = long_df.rename(columns={'ISO': 'CODE'})

    return long_df.copy()


def get_statutory_tax_rates():
    # Based on OECD data
    path_to_file = os.path.join(path_to_data, 'TABLE_II1_21022022181004367.csv')

    tax_rates = pd.read_csv(path_to_file)

    tax_rates = tax_rates[tax_rates['CORP_TAX'] == 'COMB_CIT_RATE'].copy()

    tax_rates = tax_rates[['COU', 'YEA', 'Value']].copy()

    tax_rates = tax_rates[tax_rates['YEA'].isin([2015, 2016, 2017, 2018, 2019, 2020])].copy()

    # Based on Tax Foundation data
    path_to_file = os.path.join(path_to_data, '1980-2021-Corporate-Tax-Rates-Around-the-World.xlsx')

    tax_foundation = pd.read_excel(path_to_file, engine='openpyxl')

    tax_foundation = tax_foundation[['iso_3', 'year', 'rate']].copy()

    tax_foundation = tax_foundation[tax_foundation['year'].isin([2015, 2016, 2017, 2018, 2019, 2020])].copy()

    # Merging the two sources
    merged_df = tax_rates.merge(
        tax_foundation,
        how='outer',
        left_on=['COU', 'YEA'], right_on=['iso_3', 'year']
    )

    merged_df['COU'] = merged_df.apply(
        lambda row: row['iso_3'] if isinstance(row['COU'], float) and np.isnan(row['COU']) else row['COU'],
        axis=1
    )
    merged_df['YEA'] = merged_df.apply(
        lambda row: row['year'] if isinstance(row['YEA'], float) and np.isnan(row['YEA']) else row['YEA'],
        axis=1
    )
    merged_df['Value'] = merged_df.apply(
        lambda row: row['rate'] if isinstance(row['Value'], float) and np.isnan(row['Value']) else row['Value'],
        axis=1
    )

    merged_df = merged_df.dropna().copy()

    merged_df = merged_df[['COU', 'YEA', 'Value']].copy()

    merged_df = merged_df.rename(
        columns={
            'COU': 'CODE',
            'YEA': 'YEAR',
            'Value': 'STAT_RATE'
        }
    )

    lagged_df = merged_df.copy()
    lagged_df['YEAR'] += 1
    lagged_df = lagged_df.rename(
        columns={
            'STAT_RATE': 'LAGGED_STAT_RATE'
        }
    )

    merged_df = merged_df.merge(
        lagged_df,
        how='left',
        on=['CODE', 'YEAR']
    )

    return merged_df.copy()


def get_effective_tax_rates():

    # Loading OECD Corporate Tax Statistics data
    path_to_file = os.path.join(path_to_data, 'CTS_ETR_23052022173235752.csv')
    oecd_tax_rates = pd.read_csv(path_to_file)

    if oecd_tax_rates['SCE'].nunique() == 1:
        oecd_tax_rates = oecd_tax_rates[['COU', 'YEA', 'INDIC', 'Value']].copy()

    else:
        raise Exception('Several "scenarios" in the dataset.')

    oecd_tax_rates = oecd_tax_rates.pivot(
        index=['COU', 'YEA'],
        columns='INDIC',
        values='Value'
    ).reset_index()

    oecd_tax_rates = oecd_tax_rates.rename(
        columns={
            'COU': 'CODE',
            'YEA': 'YEAR',
            'COMPOSITE_EATR': 'EATR',
            'COMPOSITE_EMTR': 'EMTR'
        }
    )

    # Loading data from the Oxford Center for Business Taxation
    path_to_file = os.path.join(path_to_data, 'cbt-tax-database-2017xls.xls')
    cbt_tax_rates = pd.read_excel(path_to_file, sheet_name='EATR and EMTR')

    cbt_tax_rates = cbt_tax_rates[cbt_tax_rates['year'] >= 2015].copy()

    cbt_tax_rates = cbt_tax_rates.rename(
        columns={
            'country': 'CODE',
            'year': 'YEAR'
        }
    )

    # We start from the table of statutory tax rates to which we add effective tax rates
    stat_rates = get_statutory_tax_rates()

    stat_rates = stat_rates.merge(
        oecd_tax_rates,
        on=['CODE', 'YEAR'],
        how='left'
    )

    stat_rates = stat_rates.merge(
        cbt_tax_rates,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Combining the two data sources
    stat_rates['EATR'] = stat_rates.apply(
        lambda row: pick_relevant_ETR(row, ETR_type='A'),
        axis=1
    )
    stat_rates['EMTR'] = stat_rates.apply(
        lambda row: pick_relevant_ETR(row, ETR_type='M'),
        axis=1
    )

    stat_rates = stat_rates.drop(columns=['EATR_x', 'EATR_y', 'EMTR_x', 'EMTR_y'])

    # Focusing on the observed ETRs to deduce median differences with statutory CIT rates
    stat_rates['ETRs_OBSERVED'] = np.logical_and(
        ~stat_rates['EATR'].isnull(),
        ~stat_rates['EMTR'].isnull()
    ) * 1

    etrs_observed = stat_rates[
        stat_rates['ETRs_OBSERVED'] == 1
    ].copy()

    etrs_observed['EATR_DIFF'] = etrs_observed['STAT_RATE'] - etrs_observed['EATR']
    etrs_observed['EMTR_DIFF'] = etrs_observed['STAT_RATE'] - etrs_observed['EMTR']

    median_diffs = etrs_observed.groupby(
        'CODE'
    ).median(
    )[
        ['EATR_DIFF', 'EMTR_DIFF']
    ].to_dict()

    eatr_median_diff = (etrs_observed['EATR_DIFF']).median()
    emtr_median_diff = (etrs_observed['EMTR_DIFF']).median()

    # Putting ETRs to 0 when we know that the statutory CIT rate is 0
    stat_rates['EATR'] = stat_rates.apply(
        lambda row: 0 if np.isnan(row['EATR']) and row['STAT_RATE'] == 0 else row['EATR'],
        axis=1
    )
    stat_rates['EMTR'] = stat_rates.apply(
        lambda row: 0 if np.isnan(row['EMTR']) and row['STAT_RATE'] == 0 else row['EMTR'],
        axis=1
    )

    # Imputing missing values based on the difference with statutory rates (inspired from Bratta et al.)
    stat_rates['EATR'] = stat_rates.apply(
        (
            lambda row: row['STAT_RATE']
            - median_diffs['EATR_DIFF'].get(row['CODE'], eatr_median_diff)
            if np.isnan(row['EATR']) else row['EATR']
        ),
        axis=1
    )
    stat_rates['EMTR'] = stat_rates.apply(
        (
            lambda row: row['STAT_RATE']
            - median_diffs['EMTR_DIFF'].get(row['CODE'], emtr_median_diff)
            if np.isnan(row['EMTR']) else row['EMTR']
        ),
        axis=1
    )

    etrs = stat_rates[['CODE', 'YEAR', 'EATR', 'EMTR', 'ETRs_OBSERVED']].copy()

    lagged_etrs = etrs.copy()
    lagged_etrs['YEAR'] += 1
    lagged_etrs = lagged_etrs.drop(columns=['ETRs_OBSERVED'])
    lagged_etrs = lagged_etrs.rename(
        columns={
            'EATR': 'LAGGED_EATR',
            'EMTR': 'LAGGED_EMTR',
        }
    )

    etrs = etrs.merge(
        lagged_etrs,
        how='left',
        on=['CODE', 'YEAR']
    )

    return etrs.copy()


def get_preprocessed_gravity_data():

    path_to_file = os.path.join(path_to_data, 'Gravity_csv_V202202', 'Gravity_V202202.csv')

    if 'gravity_dtypes.csv' not in os.listdir(path_to_data):
        gravity = pd.read_csv(path_to_file)

        gravity.dtypes.to_csv(os.path.join(path_to_data, 'gravity_dtypes.csv'))

    else:
        dtypes = pd.read_csv(
            os.path.join(path_to_data, 'gravity_dtypes.csv')
        ).set_index(
            'Unnamed: 0'
        ).to_dict()['0']

        gravity = pd.read_csv(path_to_file, dtype=dtypes)

    gravity = gravity[gravity['year'].isin([2016, 2017, 2018, 2019, 2020])].copy()

    gravity = gravity[
        [
            # Year identifier
            'year',
            # Country identifiers
            'iso3_o', 'iso3_d', 'country_exists_o', 'country_exists_d',
            # Distance variables
            'dist', 'distcap', 'contig',
            # Language variables
            'comlang_off', 'comlang_ethno',
            # Colonial history
            'comcol', 'col45',
            # Regional trade agreement dummy
            'rta',
            # Macroeconomic indicators,
            'gdp_d', 'pop_pwt_d'
        ]
    ].copy()

    gravity = gravity[
        np.logical_and(
            gravity['country_exists_d'] == 1,
            gravity['country_exists_o'] == 1
        )
    ].copy()
    gravity = gravity.drop(columns=['country_exists_o', 'country_exists_d'])

    gravity = gravity.rename(
        columns={
            'year': 'YEAR',
            'iso3_o': 'ORIGIN_COUNTRY_CODE',
            'iso3_d' : 'PARTNER_COUNTRY_CODE'
        }
    )

    return gravity.copy()


def get_EU_Member_States():

    path_to_file = os.path.join(path_to_data, 'listofeucountries_csv.csv')

    eu_countries = pd.read_csv(path_to_file, delimiter=';')

    eu_countries['IS_EU'] = 1

    eu_countries = eu_countries.rename(columns={'Alpha-3 code': 'CODE'})

    return eu_countries[['CODE', 'IS_EU']].copy()


def get_TWZ_tax_havens():

    path_to_file = os.path.join(path_to_data, 'tax_haven_list_TWZ.csv')

    TWZ_tax_havens = pd.read_csv(path_to_file, delimiter=';')

    TWZ_tax_havens = TWZ_tax_havens.rename(
        columns={
            'Alpha-3 code': 'CODE',
            'is_tax_haven?': 'IS_TAX_HAVEN_TWZ'
        }
    )

    TWZ_tax_havens = TWZ_tax_havens[['CODE', 'IS_TAX_HAVEN_TWZ']].copy()

    return TWZ_tax_havens.copy()


def get_HR_tax_havens():

    path_to_file = os.path.join(path_to_data, 'tax_haven_list_HR.csv')

    HR_tax_havens = pd.read_csv(path_to_file)

    HR_tax_havens = HR_tax_havens.rename(
        columns={
            'IS_TAX_HAVEN': 'IS_TAX_HAVEN_HR'
        }
    )

    HR_tax_havens = HR_tax_havens[['CODE', 'IS_TAX_HAVEN_HR']].copy()

    return HR_tax_havens.copy()


def get_tax_environment_variables(include_FATCA):

    path_to_file = os.path.join(path_to_data, 'tax_treaties.csv')
    tax_treaties = pd.read_csv(path_to_file)

    tax_treaties['signed'] = pd.to_datetime(tax_treaties['signed'])
    tax_treaties['entered_into_force'] = pd.to_datetime(tax_treaties['entered_into_force'])

    gravity = get_preprocessed_gravity_data()

    base_df = gravity[['YEAR', 'ORIGIN_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE']].copy()

    base_dfs = []

    for year in base_df['YEAR'].unique():

        base_df_temp = base_df[base_df['YEAR'] == year].copy()

        tax_treaties_signed = tax_treaties[
            tax_treaties['signed'] <= pd.Timestamp(year=year, month=12, day=31)
        ].copy()

        if not include_FATCA:
            tieas_signed = tax_treaties_signed[
                tax_treaties_signed['agreement_type'] == 'TIEA'
            ].copy()

        else:
            tieas_signed = tax_treaties_signed[
                tax_treaties_signed['agreement_type'].isin(['TIEA', 'FATCA'])
            ].copy()

        dtcs_signed = tax_treaties_signed[
            tax_treaties_signed['agreement_type'] == 'DTC'
        ].copy()

        tieas_signed['TIEA_SIGNED'] = 1
        dtcs_signed['DTC_SIGNED'] = 1

        tieas_signed = tieas_signed[
            ['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE', 'TIEA_SIGNED']
        ].copy()

        if include_FATCA:
            tieas_signed = tieas_signed.drop_duplicates().copy()

        dtcs_signed = dtcs_signed[
            ['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE', 'DTC_SIGNED']
        ].copy()

        base_df_temp = base_df_temp.merge(
            tieas_signed,
            how='left',
            left_on=['ORIGIN_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE'],
            right_on=['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE']
        ).drop(
            columns=['PARENT_COUNTRY_CODE']
        )
        base_df_temp = base_df_temp.merge(
            dtcs_signed,
            how='left',
            left_on=['ORIGIN_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE'],
            right_on=['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE']
        ).drop(
            columns=['PARENT_COUNTRY_CODE']
        )

        tax_treaties_enforced = tax_treaties[
            tax_treaties['entered_into_force'] <= pd.Timestamp(year=year, month=12, day=31)
        ].copy()

        if not include_FATCA:
            tieas_enforced = tax_treaties_enforced[
                tax_treaties_enforced['agreement_type'] == 'TIEA'
            ].copy()

        else:
            tieas_enforced = tax_treaties_enforced[
                tax_treaties_enforced['agreement_type'].isin(['TIEA', 'FATCA'])
            ].copy()


        dtcs_enforced = tax_treaties_enforced[
            tax_treaties_enforced['agreement_type'] == 'DTC'
        ].copy()

        tieas_enforced['TIEA_ENFORCED'] = 1
        dtcs_enforced['DTC_ENFORCED'] = 1

        tieas_enforced = tieas_enforced[
            ['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE', 'TIEA_ENFORCED']
        ].copy()

        if include_FATCA:
            tieas_enforced = tieas_enforced.drop_duplicates().copy()

        dtcs_enforced = dtcs_enforced[
            ['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE', 'DTC_ENFORCED']
        ].copy()

        base_df_temp = base_df_temp.merge(
            tieas_enforced,
            how='left',
            left_on=['ORIGIN_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE'],
            right_on=['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE']
        ).drop(
            columns=['PARENT_COUNTRY_CODE']
        )
        base_df_temp = base_df_temp.merge(
            dtcs_enforced,
            how='left',
            left_on=['ORIGIN_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE'],
            right_on=['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE']
        ).drop(
            columns=['PARENT_COUNTRY_CODE']
        )

        base_df_temp['TIEA_SIGNED'] = base_df_temp['TIEA_SIGNED'].fillna(0)
        base_df_temp['DTC_SIGNED'] = base_df_temp['DTC_SIGNED'].fillna(0)
        base_df_temp['TIEA_ENFORCED'] = base_df_temp['TIEA_ENFORCED'].fillna(0)
        base_df_temp['DTC_ENFORCED'] = base_df_temp['DTC_ENFORCED'].fillna(0)

        base_dfs.append(base_df_temp)

    df = pd.concat(base_dfs)

    temp = df.groupby(
        ['ORIGIN_COUNTRY_CODE', 'YEAR']
    ).sum(
    )[
        ['DTC_SIGNED', 'DTC_ENFORCED']
    ].reset_index(
    ).rename(
        columns={
            'DTC_SIGNED': '#_DTC_SIGNED',
            'DTC_ENFORCED': '#_DTC_ENFORCED',
        }
    )

    temp['#_DTC_ENFORCED'] /= 100
    temp['#_DTC_SIGNED'] /= 100

    df = df.merge(
        temp,
        how='left',
        left_on=['PARTNER_COUNTRY_CODE', 'YEAR'],
        right_on=['ORIGIN_COUNTRY_CODE', 'YEAR']
    ).drop(
        columns=['ORIGIN_COUNTRY_CODE_y']
    ).rename(
        columns={
            'ORIGIN_COUNTRY_CODE_x': 'PARENT_COUNTRY_CODE'
        }
    )

    return df.copy()


def get_LPI_scores():
    data = pd.read_excel(os.path.join('data', 'lpi_aggregated_ranks.xlsx'), engine='openpyxl')

    relevant_columns = ['Country', 'LPI Score'] + list(
        data.columns[data.columns.map(lambda col: col.endswith('.1'))]
    )

    data = data[relevant_columns].copy()

    new_col_names = {
        col: 'lpi_' + col.replace(
            '.1', ''
        ).replace(
            ' ', '_'
        ).replace(
            'LPI', 'overall'
        ).lower() for col in relevant_columns if col != 'Country'
    }

    data = data.rename(columns=new_col_names)

    geographies = pd.read_csv(os.path.join(path_to_data, 'geographies.csv'))

    data['Country'] = data['Country'].map(
        lambda country: country[:country.find(',')]
        if not country.startswith('Congo') and country.find(',') >=0
        else country
    )

    data = data.merge(
        geographies[['NAME', 'CODE']],
        how='left',
        left_on='Country', right_on='NAME'
    ).drop(columns='NAME')

    country_code_imputations = {
        "Cote d'Ivoire": 'CIV',
        'São Tomé and Príncipe': 'STP',
        'Lao PDR': 'LAO',
        'Kyrgyz Republic': 'KGZ',
        'Congo, Rep.': 'COG',
        'Congo, Dem. Rep.': 'COD',
        'C.A.R.': 'CAF'
    }

    data['CODE'] = data.apply(
        lambda row: country_code_imputations.get(row['Country'], row['CODE']),
        axis=1
    )

    return data.drop(columns='Country')


def get_mean_monthly_earnings():
    data = pd.read_csv(os.path.join(path_to_data, 'EAR_4MTH_SEX_ECO_CUR_NB_A-filtered-2022-09-27.csv'))

    unique_countries = list(data['ref_area.label'].unique())

    countries = {
        'COUNTRY': unique_countries,
        'KEY': [1] * len(unique_countries)
    }
    countries = pd.DataFrame(countries)

    years = {
        'YEAR': [2016, 2017, 2018, 2019],
        'KEY': [1] * 4
    }
    years = pd.DataFrame(years)

    base_df = countries.merge(years, how='outer', on='KEY').drop(columns='KEY')

    data = data[['ref_area.label', 'time', 'obs_value']].copy()
    data = data.rename(
        columns={
            'ref_area.label': 'COUNTRY',
            'time': 'YEAR',
            'obs_value': 'VALUE'
        }
    )

    df = base_df.merge(data, how='left', on=['COUNTRY', 'YEAR'])

    imputations = data.groupby('COUNTRY').mean().to_dict()['VALUE']
    df['VALUE'] = df.apply(
        lambda row: imputations[row['COUNTRY']] if np.isnan(row['VALUE']) else row['VALUE'],
        axis=1
    )

    geographies = pd.read_csv(os.path.join(path_to_data, 'geographies.csv'))

    df = df.merge(
        geographies[['NAME', 'CODE']],
        how='left',
        left_on='COUNTRY', right_on='NAME'
    ).drop(columns=['NAME'])

    country_code_imputations = {
        'Réunion': 'REU',
        'Türkiye': 'TUR'
    }

    df['CODE'] = df.apply(
        lambda row: country_code_imputations.get(row['COUNTRY'], row['CODE']),
        axis=1
    )

    return df.drop(columns=['COUNTRY']).rename(columns={'VALUE': 'MONTHLY_WAGE'})


def get_mean_monthly_earnings_upgraded():
    data = pd.read_csv(os.path.join(path_to_data, 'EAR_4MTH_SEX_ECO_CUR_NB_A-filtered-2022-09-27.csv'))

    data = data[['ref_area.label', 'time', 'obs_value']].copy()
    data = data.rename(
        columns={
            'ref_area.label': 'COUNTRY',
            'time': 'YEAR',
            'obs_value': 'VALUE'
        }
    )

    data['COUNTRY'] = data['COUNTRY'].map(
        lambda country: {'Türkiye': 'Turkey', 'Réunion': 'R√©union'}.get(country, country)
    )

    geographies = pd.read_csv(os.path.join(path_to_data, 'geographies.csv'))
    data = data.merge(
        geographies[['NAME', 'CODE', 'CONTINENT_CODE']],
        how='left',
        left_on='COUNTRY', right_on='NAME'
    ).drop(columns=['NAME'])

    data = data.drop(columns=['COUNTRY'])

    temp = data.copy()
    temp['YEAR'] += 1
    temp = temp.rename(columns={'VALUE': 'LAGGED_VALUE'})
    growth_rates = data.merge(temp, how='left', on=['CODE', 'CONTINENT_CODE', 'YEAR'])
    growth_rates['GROSS_GROWTH_RATE'] = growth_rates['VALUE'] / growth_rates['LAGGED_VALUE']

    continent_growth_rates = growth_rates.groupby(
        ['YEAR', 'CONTINENT_CODE']
    ).median()['GROSS_GROWTH_RATE'].reset_index()

    temp = data[data['YEAR'].isin([2016, 2017, 2018, 2019, 2020])].groupby('CODE').count()['VALUE']
    valid_countries = temp[temp == 4].index

    print('We already have all required observations for', len(valid_countries), 'countries.')

    data_valid = data[data['CODE'].isin(valid_countries)].copy()
    data_invalid = data[~data['CODE'].isin(valid_countries)].copy()

    countries = data_invalid[['CODE', 'CONTINENT_CODE']].drop_duplicates()
    countries['KEY'] = 1

    years = {
        'YEAR': [2010 + i for i in range(11)],
        'KEY': [1] * 11
    }
    years = pd.DataFrame(years)

    base_df = countries.merge(years, how='outer', on='KEY').drop(columns='KEY')

    df_invalid = base_df.merge(data_invalid, how='left', on=['CODE', 'CONTINENT_CODE', 'YEAR'])

    df_invalid = df_invalid.merge(continent_growth_rates, on=['CONTINENT_CODE', 'YEAR'], how='left')
    for i in range(11):
        print(df_invalid['VALUE'].isnull().sum(), 'missing values')
        df_invalid['VALUE'] = df_invalid.apply(
            lambda row: apply_growth_rates(row, df_invalid),
            axis=1
        )

    df_invalid = df_invalid[df_invalid['YEAR'].isin([2016, 2017, 2018, 2019, 2020])].copy()
    data_valid = data_valid[data_valid['YEAR'].isin([2016, 2017, 2018, 2019, 2020])].copy()

    df = pd.concat([data_valid, df_invalid], axis=0).drop(
        columns=['GROSS_GROWTH_RATE', 'CONTINENT_CODE']
    ).reset_index(drop=True)

    return df.rename(columns={'VALUE': 'MONTHLY_WAGE_UPGRADED'})


def apply_growth_rates(row, df_invalid):
    if not np.isnan(row['VALUE']):
        return row['VALUE']

    else:
        year = row['YEAR']
        country = row['CODE']

        try:
            previous_value = df_invalid[
                np.logical_and(
                    df_invalid['YEAR'] == year - 1,
                    df_invalid['CODE'] == country
                )
            ]['VALUE'].iloc[0]
        except:
            previous_value = np.nan

        try:
            temp = df_invalid[
                np.logical_and(
                    df_invalid['YEAR'] == year + 1,
                    df_invalid['CODE'] == country
                )
            ].copy()
            next_value = temp['VALUE'].iloc[0]
            next_growth_rate = temp['GROSS_GROWTH_RATE'].iloc[0]
        except:
            next_value = np.nan
            next_growth_rate = np.nan

        if not np.isnan(previous_value * row['GROSS_GROWTH_RATE']):
            return previous_value * row['GROSS_GROWTH_RATE']

        else:
            return next_value / next_growth_rate


def get_remoteness():

    path_to_file = os.path.join(path_to_data, 'Gravity_csv_V202202', 'Gravity_V202202.csv')

    if 'gravity_dtypes.csv' not in os.listdir(path_to_data):
        gravity = pd.read_csv(path_to_file)

        gravity.dtypes.to_csv(os.path.join(path_to_data, 'gravity_dtypes.csv'))

    else:
        dtypes = pd.read_csv(
            os.path.join(path_to_data, 'gravity_dtypes.csv')
        ).set_index(
            'Unnamed: 0'
        ).to_dict()['0']

        gravity = pd.read_csv(path_to_file, dtype=dtypes)

    gravity = gravity[gravity['year'].isin([2016, 2017, 2018, 2019, 2020])].copy()

    gravity = gravity[
        [
            # Year identifier
            'year',
            # Country identifiers
            'iso3_o', 'iso3_d', 'country_exists_o', 'country_exists_d',
            # Relevant variables for remoteness computation
            'dist', 'gdp_o'
        ]
    ].copy()

    gravity = gravity[
        np.logical_and(
            gravity['country_exists_d'] == 1,
            gravity['country_exists_o'] == 1
        )
    ].copy()
    gravity = gravity.drop(columns=['country_exists_o', 'country_exists_d'])

    gravity['ratio'] = gravity['gdp_o'] / gravity['dist']

    gravity = gravity.groupby(
        ['iso3_d', 'year']
    ).agg(
        {
            'ratio': 'sum',
        }
    ).reset_index()

    gravity['ratio'] = 1 / gravity['ratio']

    gravity = gravity.rename(
        columns={
            'ratio': 'REMOTENESS',
            'iso3_d': 'CODE',
            'year': 'YEAR'
        }
    )

    return gravity.copy()
