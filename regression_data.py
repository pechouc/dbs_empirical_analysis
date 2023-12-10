import numpy as np
import pandas as pd

from cbcr_data_preparation import *

from data_preparation_utils import *

from VAT_rates_collection import get_VAT_rates

include_FATCA = False


def get_aggregate_US_CbCR_regression_data():
    irs = preprocess_aggregate_US_CbCR_data()

    # Adding statutory tax rates
    stat_rates = get_statutory_tax_rates()

    irs = irs.merge(
        stat_rates,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding EATRs and EMTRs
    etrs = get_effective_tax_rates()

    irs = irs.merge(
        etrs,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding foreign market access
    fma = get_foreign_market_access()

    irs = irs.merge(
        fma,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding GDP
    woe = get_WOE_GDP_data()

    irs = irs.merge(
        woe,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding US GDP
    woe_restricted = woe[woe['CODE'] == 'USA'].drop(columns='CODE').rename(columns={'NGDPD': 'US_NGDPD'})

    irs = irs.merge(
        woe_restricted,
        how='left',
        on=['YEAR']
    )

    # Adding gravity control variables
    gravity = get_preprocessed_gravity_data()

    gravity = gravity[gravity['ORIGIN_COUNTRY_CODE'] == 'USA'].copy()
    gravity = gravity.drop(columns=['ORIGIN_COUNTRY_CODE'])
    gravity = gravity.rename(columns={'PARTNER_COUNTRY_CODE': 'CODE'})

    irs = irs.merge(
        gravity,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding tax environment variables
    agreements = get_tax_environment_variables(include_FATCA=include_FATCA)

    agreements = agreements[agreements['PARENT_COUNTRY_CODE'] == 'USA'].copy()
    agreements = agreements.drop(columns=['PARENT_COUNTRY_CODE'])
    agreements = agreements.rename(columns={'PARTNER_COUNTRY_CODE': 'CODE'})

    irs = irs.merge(
        agreements,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding the EU membership dummy
    eu_members = get_EU_Member_States()

    irs = irs.merge(
        eu_members,
        on='CODE',
        how='left'
    )

    irs['IS_EU'] = irs['IS_EU'].fillna(0)

    # Adding the TWZ tax haven dummy
    TWZ_tax_havens = get_TWZ_tax_havens()

    irs = irs.merge(
        TWZ_tax_havens,
        on='CODE',
        how='left'
    )

    irs['IS_TAX_HAVEN_TWZ'] = irs['IS_TAX_HAVEN_TWZ'].fillna(0)

    # Adding the Hines & Rice tax haven dummy
    HR_tax_havens = get_HR_tax_havens()

    irs = irs.merge(
        HR_tax_havens,
        on='CODE',
        how='left'
    )

    irs['IS_TAX_HAVEN_HR'] = irs['IS_TAX_HAVEN_HR'].fillna(0)

    # Adding VAT rates
    VAT_rates = get_VAT_rates()

    irs = irs.merge(
        VAT_rates,
        how='left',
        left_on='CODE', right_on='COUNTRY_CODE'
    ).drop(columns='COUNTRY_CODE')

    # Adding LPI scores
    LPI_scores = get_LPI_scores()

    irs = irs.merge(
        LPI_scores,
        how='left',
        on='CODE'
    )

    # Adding mean monthly earnings
    monthly_earnings = get_mean_monthly_earnings()

    irs = irs.merge(
        monthly_earnings,
        how='left',
        on=['CODE', 'YEAR']
    )

    # Adding upgraded mean monthly earnings
    monthly_earnings = get_mean_monthly_earnings_upgraded()

    irs = irs.merge(
        monthly_earnings,
        how='left',
        on=['CODE', 'YEAR']
    )

    # Adding remoteness
    remoteness = get_remoteness()

    irs = irs.merge(
        remoteness,
        how='left',
        on=['CODE', 'YEAR']
    )

    return irs.copy()

def get_heckman_selection_model_data():

    # Starting from the foreign market access dataset
    fma = get_foreign_market_access()

    # Adding IRS data
    irs = preprocess_aggregate_US_CbCR_data()
    irs['SELECTED'] = 1

    fma = fma.merge(
        irs,
        on=['CODE', 'YEAR'],
        how='left'
    )

    fma['SELECTED'] = fma['SELECTED'].fillna(0)

    # Adding statutory tax rates
    stat_rates = get_statutory_tax_rates()

    fma = fma.merge(
        stat_rates,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding EATRs and EMTRs
    etrs = get_effective_tax_rates()

    fma = fma.merge(
        etrs,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding GDP
    woe = get_WOE_GDP_data()

    fma = fma.merge(
        woe,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding gravity control variables
    gravity = get_preprocessed_gravity_data()

    gravity = gravity[gravity['ORIGIN_COUNTRY_CODE'] == 'USA'].copy()
    gravity = gravity.drop(columns=['ORIGIN_COUNTRY_CODE'])
    gravity = gravity.rename(columns={'PARTNER_COUNTRY_CODE': 'CODE'})

    fma = fma.merge(
        gravity,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding tax environment variables
    agreements = get_tax_environment_variables(include_FATCA=include_FATCA)

    agreements = agreements[agreements['PARENT_COUNTRY_CODE'] == 'USA'].copy()
    agreements = agreements.drop(columns=['PARENT_COUNTRY_CODE'])
    agreements = agreements.rename(columns={'PARTNER_COUNTRY_CODE': 'CODE'})

    fma = fma.merge(
        agreements,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding the EU membership dummy
    eu_members = get_EU_Member_States()

    fma = fma.merge(
        eu_members,
        on='CODE',
        how='left'
    )

    fma['IS_EU'] = fma['IS_EU'].fillna(0)

    # Adding the TWZ tax haven dummy
    TWZ_tax_havens = get_TWZ_tax_havens()

    fma = fma.merge(
        TWZ_tax_havens,
        on='CODE',
        how='left'
    )

    fma['IS_TAX_HAVEN_TWZ'] = fma['IS_TAX_HAVEN_TWZ'].fillna(0)

    # Adding the Hines & Rice tax haven dummy
    HR_tax_havens = get_HR_tax_havens()

    fma = fma.merge(
        HR_tax_havens,
        on='CODE',
        how='left'
    )

    fma['IS_TAX_HAVEN_HR'] = fma['IS_TAX_HAVEN_HR'].fillna(0)

    return fma.copy()


def get_per_industry_regression_data():
    irs = preprocess_per_industry_US_CbCR_data()

    irs['NB_REPORTING_MNEs'] = irs['NB_REPORTING_MNEs'].map(lambda x: np.nan if x == 'd' else x)

    # Adding statutory tax rates
    stat_rates = get_statutory_tax_rates()

    irs = irs.merge(
        stat_rates,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding EATRs and EMTRs
    etrs = get_effective_tax_rates()

    irs = irs.merge(
        etrs,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding foreign market access
    fma = get_foreign_market_access()

    irs = irs.merge(
        fma,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding GDP
    woe = get_WOE_GDP_data()

    irs = irs.merge(
        woe,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding gravity control variables
    gravity = get_preprocessed_gravity_data()

    gravity = gravity[gravity['ORIGIN_COUNTRY_CODE'] == 'USA'].copy()
    gravity = gravity.drop(columns=['ORIGIN_COUNTRY_CODE'])
    gravity = gravity.rename(columns={'PARTNER_COUNTRY_CODE': 'CODE'})

    irs = irs.merge(
        gravity,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding tax environment variables
    agreements = get_tax_environment_variables(include_FATCA=include_FATCA)

    agreements = agreements[agreements['PARENT_COUNTRY_CODE'] == 'USA'].copy()
    agreements = agreements.drop(columns=['PARENT_COUNTRY_CODE'])
    agreements = agreements.rename(columns={'PARTNER_COUNTRY_CODE': 'CODE'})

    irs = irs.merge(
        agreements,
        on=['CODE', 'YEAR'],
        how='left'
    )

    # Adding the EU membership dummy
    eu_members = get_EU_Member_States()

    irs = irs.merge(
        eu_members,
        on='CODE',
        how='left'
    )

    irs['IS_EU'] = irs['IS_EU'].fillna(0)

    # Adding the TWZ tax haven dummy
    TWZ_tax_havens = get_TWZ_tax_havens()

    irs = irs.merge(
        TWZ_tax_havens,
        on='CODE',
        how='left'
    )

    irs['IS_TAX_HAVEN_TWZ'] = irs['IS_TAX_HAVEN_TWZ'].fillna(0)

    # Adding the Hines & Rice tax haven dummy
    HR_tax_havens = get_HR_tax_havens()

    irs = irs.merge(
        HR_tax_havens,
        on='CODE',
        how='left'
    )

    irs['IS_TAX_HAVEN_HR'] = irs['IS_TAX_HAVEN_HR'].fillna(0)

    # Adding VAT rates
    VAT_rates = get_VAT_rates()

    irs = irs.merge(
        VAT_rates,
        how='left',
        left_on='CODE', right_on='COUNTRY_CODE'
    ).drop(columns='COUNTRY_CODE')

    # Adding LPI scores
    LPI_scores = get_LPI_scores()

    irs = irs.merge(
        LPI_scores,
        how='left',
        on='CODE'
    )

    # Adding mean monthly earnings
    monthly_earnings = get_mean_monthly_earnings()

    irs = irs.merge(
        monthly_earnings,
        how='left',
        on=['CODE', 'YEAR']
    )

    # Adding upgraded mean monthly earnings
    monthly_earnings = get_mean_monthly_earnings_upgraded()

    irs = irs.merge(
        monthly_earnings,
        how='left',
        on=['CODE', 'YEAR']
    )

    # Adding remoteness
    remoteness = get_remoteness()

    irs = irs.merge(
        remoteness,
        how='left',
        on=['CODE', 'YEAR']
    )

    return irs.copy()


def get_bilateral_CbCR_regression_data():

    oecd = preprocess_bilateral_aggregate_CbCR_data()

    # Adding statutory tax rates
    stat_rates = get_statutory_tax_rates()
    stat_rates = stat_rates.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE'
        }
    )

    oecd = oecd.merge(
        stat_rates,
        on=['PARTNER_COUNTRY_CODE', 'YEAR'],
        how='left'
    )

    # Adding EATRs and EMTRs
    etrs = get_effective_tax_rates()
    etrs = etrs.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE'
        }
    )

    oecd = oecd.merge(
        etrs,
        on=['PARTNER_COUNTRY_CODE', 'YEAR'],
        how='left'
    )

    # Adding foreign market access
    fma = get_foreign_market_access()
    fma = fma.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE'
        }
    )

    oecd = oecd.merge(
        fma,
        on=['PARTNER_COUNTRY_CODE', 'YEAR'],
        how='left'
    )

    # Adding GDP of the partner country
    woe = get_WOE_GDP_data()
    woe = woe.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE',
            'NGDPD': 'NGDPD_PARTNER'
        }
    )

    oecd = oecd.merge(
        woe,
        on=['PARTNER_COUNTRY_CODE', 'YEAR'],
        how='left'
    )

    # Adding GDP of the headquarter country
    woe = woe.rename(
        columns={
            'PARTNER_COUNTRY_CODE': 'PARENT_COUNTRY_CODE',
            'NGDPD_PARTNER': 'NGDPD_PARENT'
        }
    )

    oecd = oecd.merge(
        woe,
        on=['PARENT_COUNTRY_CODE', 'YEAR'],
        how='left'
    )

    # Adding gravity control variables
    gravity = get_preprocessed_gravity_data()
    gravity = gravity.rename(columns={'ORIGIN_COUNTRY_CODE': 'PARENT_COUNTRY_CODE'})

    oecd = oecd.merge(
        gravity,
        on=['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE', 'YEAR'],
        how='left'
    )

    # Adding tax environment variables
    agreements = get_tax_environment_variables(include_FATCA=include_FATCA)

    oecd = oecd.merge(
        agreements,
        on=['PARENT_COUNTRY_CODE', 'PARTNER_COUNTRY_CODE', 'YEAR'],
        how='left'
    )

    # Adding the EU membership dummy
    eu_members = get_EU_Member_States()
    eu_members = eu_members.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE'
        }
    )

    oecd = oecd.merge(
        eu_members,
        on='PARTNER_COUNTRY_CODE',
        how='left'
    )

    oecd['IS_EU'] = oecd['IS_EU'].fillna(0)

    # Adding the TWZ tax haven dummy
    TWZ_tax_havens = get_TWZ_tax_havens()
    TWZ_tax_havens = TWZ_tax_havens.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE'
        }
    )

    oecd = oecd.merge(
        TWZ_tax_havens,
        on='PARTNER_COUNTRY_CODE',
        how='left'
    )

    oecd['IS_TAX_HAVEN_TWZ'] = oecd['IS_TAX_HAVEN_TWZ'].fillna(0)

    # Adding the Hines & Rice tax haven dummy
    HR_tax_havens = get_HR_tax_havens()
    HR_tax_havens = HR_tax_havens.rename(
        columns={
            'CODE': 'PARTNER_COUNTRY_CODE'
        }
    )

    oecd = oecd.merge(
        HR_tax_havens,
        on='PARTNER_COUNTRY_CODE',
        how='left'
    )

    oecd['IS_TAX_HAVEN_HR'] = oecd['IS_TAX_HAVEN_HR'].fillna(0)

    return oecd.copy()


if __name__ == '__main__':
    US_CbCR_regression_data = get_aggregate_US_CbCR_regression_data()
    heckman_selection_model_data = get_heckman_selection_model_data()
    per_industry_regression_data = get_per_industry_regression_data()
    bilateral_CbCR_regression_data = get_bilateral_CbCR_regression_data()


    US_CbCR_regression_data.to_csv('US_CbCR_regression_data.csv', index=False)
    heckman_selection_model_data.to_csv('heckman_selection_model_data.csv', index=False)
    per_industry_regression_data.to_csv('per_industry_regression_data.csv', index=False)
    bilateral_CbCR_regression_data.to_csv('bilateral_CbCR_regression_data.csv', index=False)
