clear all

// ########################################################################
// Using the IRS' aggregated and anonymised country-by-country report statistics
// ########################################################################

// Basic results: effect of various tax variables on unrelated-party revenues
// ########################################################################

eststo clear

use "US_CbCR_regression_data.dta"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues eatr log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues emtr log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues lagged_stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues etr_cash_previous_year_posprofit log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues etr_accrued_previous_year_pospro log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate eatr emtr lagged_stat_rate etr_cash_previous_year_posprofit etr_accrued_previous_year_pospro) replace

esttab using "latex_outputs/table_initial_results.tex", drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate eatr emtr lagged_stat_rate etr_cash_previous_year_posprofit etr_accrued_previous_year_pospro) replace

// Basic results - SLIDE OUTPUT VERSION
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues lagged_stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues etr_cash_previous_year_posprofit log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(_cons log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate lagged_stat_rate etr_cash_previous_year_posprofit) replace

esttab using "latex_outputs/slide_output_table_initial_results.tex", drop(_cons log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate lagged_stat_rate etr_cash_previous_year_posprofit) replace

// Introducing the broader tax environment of the partner country
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate tiea_enforced dtc_enforced _dtc_enforced log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate is_tax_haven_twz tiea_enforced dtc_enforced _dtc_enforced log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate is_tax_haven_hr tiea_enforced dtc_enforced _dtc_enforced log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local exclude_US Yes

// esttab, drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate is_tax_haven_twz is_tax_haven_hr tiea_enforced dtc_enforced _dtc_enforced) replace

esttab using "latex_outputs/table_tax_environment.tex", drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate is_tax_haven_twz is_tax_haven_hr tiea_enforced dtc_enforced _dtc_enforced) replace

// Introducing the broader tax environment of the partner country - SLIDE OUTPUT VERSION
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate tiea_enforced dtc_enforced _dtc_enforced log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local tax_env Yes
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate vat_rate is_tax_haven_twz tiea_enforced dtc_enforced _dtc_enforced log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local tax_env Yes
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate vat_rate is_tax_haven_hr tiea_enforced dtc_enforced _dtc_enforced log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local tax_env Yes
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(_cons log_dist tiea_enforced dtc_enforced _dtc_enforced log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(tax_env gravity_controls fe N r2 r2_a, labels("Tax environment controls" "Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate vat_rate is_tax_haven_twz is_tax_haven_hr) replace

esttab using "latex_outputs/slide_output_table_tax_environment.tex", drop(_cons log_dist tiea_enforced dtc_enforced _dtc_enforced log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(tax_env gravity_controls fe N r2 r2_a, labels("Tax environment controls" "Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate vat_rate is_tax_haven_twz is_tax_haven_hr) replace


// Varying the dependent variable and introducing the VAT rate
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate vat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_related_party_revenues stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_related_party_revenues stat_rate vat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_nb_reporting_mnes stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_profits stat_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate vat_rate) replace

esttab using "latex_outputs/table_varying_dep_var.tex", drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate vat_rate) replace

// Running the regression with the log of the retention rate instead
// ########################################################################

eststo clear

generate log_retention_rate = log(1 - stat_rate / 100)
label variable log_retention_rate "ln(Retention rate) - Statutory"

generate log_retention_rate_eatr = log(1 - eatr / 100)
label variable log_retention_rate_eatr "ln(Retention rate) - EATR"

generate log_retention_rate_lagged = log(1 - lagged_stat_rate / 100)
label variable log_retention_rate_lagged "ln(Retention rate) - Statutory, lagged"

generate log_retention_rate_etr_cash = log(1 - etr_cash_previous_year_posprofit / 100)
label variable log_retention_rate_etr_cash "ln(Retention rate) - Lagged CbCR ETR, cash"

generate log_retention_rate_etr_accrued = log(1 - etr_accrued_previous_year_pospro / 100)
label variable log_retention_rate_etr_accrued "ln(Retention rate) - Lagged CbCR ETR, accrued"

eststo: quietly regress log_unrelated_party_revenues log_retention_rate log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_eatr log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_lagged log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_etr_cash log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_etr_accrued log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

esttab using "latex_outputs/table_retention_rates_results.tex", drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

// Changing the proxy for foreign market access (based on the Logistics Performance Index)
// ########################################################################

eststo clear

gen log_lpi = log(lpi_overall_score)
label variable log_lpi "ln(Logistics Performance Index)"

eststo: quietly regress log_unrelated_party_revenues log_retention_rate log_ngdpd log_lpi log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_eatr log_ngdpd log_lpi log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_lagged log_ngdpd log_lpi log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_etr_cash log_ngdpd log_lpi log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_etr_accrued log_ngdpd log_lpi log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

esttab using "latex_outputs/table_controlling_for_LPI.tex", drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

// Introducing the wage rate
// ########################################################################

eststo clear

gen daily_wage = monthly_wage_upgraded / 30
label variable daily_wage "Mean daily wage (current USD)"

gen log_wage = log(daily_wage)
label variable log_wage "ln(Mean daily wage)"

eststo: quietly regress log_unrelated_party_revenues log_retention_rate log_ngdpd log_fma log_dist log_wage log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_eatr log_ngdpd log_fma log_dist log_wage log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_lagged log_ngdpd log_fma log_dist log_wage log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_etr_cash log_ngdpd log_fma log_dist log_wage log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_retention_rate_etr_accrued log_ngdpd log_fma log_dist log_wage log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

esttab using "latex_outputs/table_controlling_for_wage.tex", drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

// Focusing on within-country variations
// ########################################################################

encode code, generate(country)

xtset country year

eststo clear

eststo: quietly xtreg log_unrelated_party_revenues stat_rate log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues eatr log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues emtr log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues lagged_stat_rate log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues etr_cash_previous_year_posprofit log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues etr_accrued_previous_year_pospro log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

// esttab, drop(*.year) p stats(country_fe year_fe N r2 r2_a, labels("Country fixed effects" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Standard errors clustered at the country level.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate eatr emtr lagged_stat_rate etr_cash_previous_year_posprofit etr_accrued_previous_year_pospro) replace

esttab using "latex_outputs/table_within_variations.tex", drop(*.year) p stats(country_fe year_fe N r2 r2_a, labels("Country fixed effects" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Standard errors clustered at the country level.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate eatr emtr lagged_stat_rate etr_cash_previous_year_posprofit etr_accrued_previous_year_pospro) replace

// Focusing on within-country variations with the retention rate specification
// ########################################################################

eststo clear

eststo: quietly xtreg log_unrelated_party_revenues log_retention_rate log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues log_retention_rate_eatr log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues log_retention_rate_lagged log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues log_retention_rate_etr_cash log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

eststo: quietly xtreg log_unrelated_party_revenues log_retention_rate_etr_accrued log_ngdpd log_fma i.year, fe vce(cluster country)
estadd local country_fe Yes
estadd local year_fe Yes

// esttab, drop(*.year) p stats(country_fe year_fe N r2 r2_a, labels("Country fixed effects" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Standard errors clustered at the country level.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

esttab using "latex_outputs/table_within_variations_retention_rates.tex", drop(*.year) p stats(country_fe year_fe N r2 r2_a, labels("Country fixed effects" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Standard errors clustered at the country level.") star(* 0.10 ** 0.05 *** 0.01) order(log_retention_rate log_retention_rate_eatr log_retention_rate_lagged log_retention_rate_etr_cash log_retention_rate_etr_accrued) replace

// Non-linear relationship between unrelated-party revenues and the tax rate
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues eatr eatr_squared log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA", robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues emtr emtr_squared log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA", robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate stat_rate_squared eatr eatr_squared emtr emtr_squared) replace

esttab using "latex_outputs/table_non_linear_relationship.tex", drop(log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate stat_rate_squared eatr eatr_squared emtr emtr_squared) replace

// ########################################################################
// Using the IRS' industry breakdown of country-by-country report statistics
// ########################################################################

eststo clear

clear

// General results based on US data broken down per industry
// ########################################################################

eststo clear

use "per_industry_regression_data.dta"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues eatr log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues lagged_stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.interacted_control) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Sector x Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_initial_results_by_indus.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.interacted_control) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Sector x Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate eatr lagged_stat_rate stat_rate_squared) replace

// Distinguishing each industry, using the linear specification
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Agriculture, extractives and construction", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Primary"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Manufacturing", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Manufacturing"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Wholesale and retail trade", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Trade"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Information", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Information"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Finance and insurance", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Finance"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Technical services", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Technical services"

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Management (except public administration)", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Management"

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_linear_relationship_indus_sub_samples.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

// Distinguishing each industry, using the quadratic specification
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Agriculture, extractives and construction", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Primary"

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Manufacturing", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Manufacturing"

scalar beta_1_manufacturing = _b[stat_rate]
scalar beta_2_manufacturing = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Wholesale and retail trade", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Trade"

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Information", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Information"

scalar beta_1_information = _b[stat_rate]
scalar beta_2_information = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Finance and insurance", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Finance"

scalar beta_1_finance = _b[stat_rate]
scalar beta_2_finance = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Technical services", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Technical services"

scalar beta_1_technical_services = _b[stat_rate]
scalar beta_2_technical_services = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Management (except public administration)", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Management"

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_non_linear_relationship_indus_sub_samples.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

// ########################################################################
// Using the OECD's aggregated and anonymised country-by-country report statistics
// ########################################################################

eststo clear

clear

use "bilateral_CbCR_regression_data.dta"

// General results based on the OECD's aggregated country-by-country statistics
// ########################################################################

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd_parent log_ngdpd_partner log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues eatr log_ngdpd_parent log_ngdpd_partner log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues lagged_stat_rate log_ngdpd_parent log_ngdpd_partner log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues stat_rate stat_rate_squared log_ngdpd_parent log_ngdpd_partner log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

esttab using "latex_outputs/table_initial_results_bilateral_CbCR.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.interacted_control) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Parent country x Year FE" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) order(stat_rate eatr stat_rate_squared) replace
