clear

eststo clear

use "US_CbCR_regression_data.dta"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate, robust
estadd local fe No
estadd local exclude_US No

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta, robust
estadd local fe No

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local fe Yes

// esttab, drop(*.year) p stats(fe N r2 r2_a, labels("Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_initial_results.tex", drop(*.year) p stats(fe N r2 r2_a, labels("Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist eatr is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist emtr is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_robustness_to_ETRs.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_tax_haven_twz is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_tax_haven_hr is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_tax_haven_twz tiea_signed dtc_signed _dtc_signed is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_tax_haven_hr tiea_signed dtc_signed _dtc_signed is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local exclude_US Yes

// eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_tax_haven_twz tiea_enforced dtc_enforced _dtc_enforced is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
// estadd local gravity_controls Yes
// estadd local fe Yes
//
// eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_tax_haven_hr tiea_enforced dtc_enforced _dtc_enforced is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
// estadd local gravity_controls Yes
// estadd local fe Yes
// estadd local exclude_US Yes

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_tax_environment.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist eatr eatr_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA", robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_non_linear_relationship.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

eststo: quietly regress log_unrelated_party_revenues stat_rate log_ngdpd log_fma log_dist is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_nb_reporting_mnes stat_rate log_ngdpd log_fma log_dist contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_related_party_revenues stat_rate log_ngdpd log_fma log_dist contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_profits stat_rate log_ngdpd log_fma log_dist contig comlang_off comlang_ethno col45 is_eu rta i.year, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_varying_dep_var.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

clear

eststo clear

use "per_industry_regression_data.dta"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist eatr is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.interacted_control) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Sector x Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_initial_results_by_indus.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.interacted_control) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Sector x Year fixed effects" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Agriculture, extractives and construction", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Primary"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Manufacturing", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Manufacturing"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Wholesale and retail trade", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Trade"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Information", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Information"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Finance and insurance", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Finance"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Technical services", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Technical services"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if industry == "Management (except public administration)", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Management"

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_linear_relationship_indus_sub_samples.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Agriculture, extractives and construction", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Primary"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Manufacturing", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Manufacturing"

scalar beta_1_manufacturing = _b[stat_rate]
scalar beta_2_manufacturing = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Wholesale and retail trade", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Trade"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Information", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Information"

scalar beta_1_information = _b[stat_rate]
scalar beta_2_information = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Finance and insurance", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Finance"

scalar beta_1_finance = _b[stat_rate]
scalar beta_2_finance = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Technical services", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Technical services"

scalar beta_1_technical_services = _b[stat_rate]
scalar beta_2_technical_services = _b[stat_rate_squared]

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.year if code != "USA" & industry == "Management (except public administration)", robust
estadd local gravity_controls Yes
estadd local fe Yes
estadd local sub_sample "Management"

// esttab, drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

esttab using "latex_outputs/table_non_linear_relationship_indus_sub_samples.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.year) p stats(gravity_controls fe sub_sample N r2 r2_a, labels("Gravity control variables" "Year fixed effects" "Sector" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace

eststo clear

clear

use "bilateral_CbCR_regression_data.dta"

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist eatr is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

eststo: quietly regress log_unrelated_party_revenues log_ngdpd log_fma log_dist stat_rate stat_rate_squared is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust
estadd local gravity_controls Yes
estadd local fe Yes

esttab using "latex_outputs/table_initial_results_bilateral_CbCR.tex", drop(is_domestic contig comlang_off comlang_ethno col45 is_eu rta *.interacted_control) p stats(gravity_controls fe N r2 r2_a, labels("Gravity control variables" "Parent country x Year FE" "Observations" "R-squared" "Adj. R-squared")) label addnote("Using robust standard errors.") star(* 0.10 ** 0.05 *** 0.01) replace
