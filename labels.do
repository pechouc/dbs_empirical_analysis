clear

import delimited "US_CbCR_regression_data.csv"

gen log_unrelated_party_revenues = log(unrelated_party_revenues)
gen log_nb_reporting_mnes = log(nb_reporting_mnes)
gen log_related_party_revenues = log(related_party_revenues)
gen log_total_revenues = log(total_revenues)
gen log_profits = log(profit_before_tax)

gen log_dist = log(dist)
gen log_ngdpd = log(ngdpd)
gen log_gdp_d = log(gdp_d)
gen log_pop_pwt_d = log(pop_pwt_d)
gen log_fma = log(fma)

gen stat_rate_squared = stat_rate^2
gen stat_rate_cube = stat_rate^3
gen eatr_squared = eatr^2
gen eatr_cube = eatr^3
gen emtr_squared = emtr^2
gen emtr_cube = emtr^3

encode code, gen(partner)

gen is_domestic = (code == "USA")

label variable unrelated_party_revenues "UPR"
label variable nb_reporting_mnes "\# MNEs"
label variable related_party_revenues "RPR"
label variable total_revenues "TR"
label variable profit_before_tax "PBT"

label variable log_unrelated_party_revenues "ln(UPR)"
label variable log_nb_reporting_mnes "ln(\# MNEs)"
label variable log_related_party_revenues "ln(RPR)"
label variable log_total_revenues "ln(TR)"
label variable log_profits "ln(PBT)"

label variable log_dist "ln(Distance)"
label variable log_ngdpd "ln(GDP) - WOE"
label variable log_gdp_d "ln(GDP) - WDI"
label variable log_pop_pwt_d "ln(Population)"
label variable log_fma "ln(Foreign Market Access)"

label variable dist "Distance"
label variable distcap "Distance between capitals"
label variable ngdpd "GDP - WOE"
label variable gdp_d "GDP - WDI"
label variable pop_pwt_d "Population"
label variable is_domestic "Domestic"
label variable contig "Contiguity"
label variable comlang_off "Common language - Official"
label variable comlang_ethno "Common language - Spoken"
label variable rta "Regional trade agreement"
label variable comcol "Common colonizer after 1945"
label variable col45 "Colonial relationship after 1945"
label variable is_eu "EU membership"
label variable is_tax_haven_twz "TWZ tax haven classification"
label variable is_tax_haven_hr "H\&R tax haven classification"

label variable stat_rate "Statutory tax rate"
label variable stat_rate_squared "Squared statutory tax rate"
label variable stat_rate_cube "Cube statutory tax rate"
label variable eatr "EATR"
label variable eatr_squared "Squared EATR"
label variable eatr_cube "Cube EATR"
label variable emtr "EMTR"
label variable emtr_squared "Squared EMTR"
label variable emtr_cube "Cube EMTR"

label variable tiea_signed "TIEA signed"
label variable dtc_signed "DTC signed"
label variable tiea_enforced "TIEA enforced"
label variable dtc_enforced "DTC enforced"
label variable _dtc_signed "\# DTC signed / 100"
label variable _dtc_enforced "\# DTC enforced / 100"

save "US_CbCR_regression_data.dta", replace

clear

import delimited "per_industry_regression_data.csv"

gen log_unrelated_party_revenues = log(unrelated_party_revenues)
gen log_nb_reporting_mnes = log(nb_reporting_mnes)
gen log_related_party_revenues = log(related_party_revenues)
gen log_total_revenues = log(total_revenues)
gen log_profits = log(profit_before_tax)

gen log_dist = log(dist)
gen log_ngdpd = log(ngdpd)
gen log_gdp_d = log(gdp_d)
gen log_pop_pwt_d = log(pop_pwt_d)
gen log_fma = log(fma)

gen stat_rate_squared = stat_rate^2
gen stat_rate_cube = stat_rate^3
gen eatr_squared = eatr^2
gen eatr_cube = eatr^3
gen emtr_squared = emtr^2
gen emtr_cube = emtr^3

encode industry, gen(sector)
encode code, gen(partner)

gen interacted_control = sector * year

gen is_domestic = (code == "USA")

label variable unrelated_party_revenues "UPR"
label variable nb_reporting_mnes "\# MNEs"
label variable related_party_revenues "RPR"
label variable total_revenues "TR"
label variable profit_before_tax "PBT"

label variable log_unrelated_party_revenues "ln(UPR)"
label variable log_nb_reporting_mnes "ln(\# MNEs)"
label variable log_related_party_revenues "ln(RPR)"
label variable log_total_revenues "ln(TR)"
label variable log_profits "ln(PBT)"

label variable log_dist "ln(Distance)"
label variable log_ngdpd "ln(GDP) - WOE"
label variable log_gdp_d "ln(GDP) - WDI"
label variable log_pop_pwt_d "ln(Population)"
label variable log_fma "ln(Foreign Market Access)"

label variable dist "Distance"
label variable distcap "Distance between capitals"
label variable ngdpd "GDP - WOE"
label variable gdp_d "GDP - WDI"
label variable pop_pwt_d "Population"
label variable is_domestic "Domestic"
label variable contig "Contiguity"
label variable comlang_off "Common language - Official"
label variable comlang_ethno "Common language - Spoken"
label variable rta "Regional trade agreement"
label variable comcol "Common colonizer after 1945"
label variable col45 "Colonial relationship after 1945"
label variable is_eu "EU membership"
label variable is_tax_haven_twz "TWZ tax haven classification"
label variable is_tax_haven_hr "H\&R tax haven classification"

label variable stat_rate "Statutory tax rate"
label variable stat_rate_squared "Squared statutory tax rate"
label variable stat_rate_cube "Cube statutory tax rate"
label variable eatr "EATR"
label variable eatr_squared "Squared EATR"
label variable eatr_cube "Cube EATR"
label variable emtr "EMTR"
label variable emtr_squared "Squared EMTR"
label variable emtr_cube "Cube EMTR"

label variable tiea_signed "TIEA signed"
label variable dtc_signed "DTC signed"
label variable tiea_enforced "TIEA enforced"
label variable dtc_enforced "DTC enforced"
label variable _dtc_signed "\# DTC signed / 100"
label variable _dtc_enforced "\# DTC enforced / 100"

save "per_industry_regression_data.dta", replace

clear

import delimited "bilateral_CbCR_regression_data.csv"

gen log_unrelated_party_revenues = log(unrelated_party_revenues)
gen log_nb_reporting_mnes = log(nb_reporting_mnes)
gen log_related_party_revenues = log(related_party_revenues)
gen log_total_revenues = log(total_revenues)
gen log_profits = log(profit_before_tax)

gen log_dist = log(dist)
gen log_ngdpd = log(ngdpd)
gen log_gdp_d = log(gdp_d)
gen log_pop_pwt_d = log(pop_pwt_d)
gen log_fma = log(fma)

gen stat_rate_squared = stat_rate^2
gen stat_rate_cube = stat_rate^3
gen eatr_squared = eatr^2
gen eatr_cube = eatr^3
gen emtr_squared = emtr^2
gen emtr_cube = emtr^3

encode parent_country_code, gen(parent)
encode partner_country_code, gen(partner)

gen interacted_control = parent * year

gen is_domestic = (parent_country_code == partner_country_code)

label variable unrelated_party_revenues "UPR"
label variable nb_reporting_mnes "\# MNEs"
label variable related_party_revenues "RPR"
label variable total_revenues "TR"
label variable profit_before_tax "PBT"

label variable log_unrelated_party_revenues "ln(UPR)"
label variable log_nb_reporting_mnes "ln(\# MNEs)"
label variable log_related_party_revenues "ln(RPR)"
label variable log_total_revenues "ln(TR)"
label variable log_profits "ln(PBT)"

label variable log_dist "ln(Distance)"
label variable log_ngdpd "ln(GDP) - WOE"
label variable log_gdp_d "ln(GDP) - WDI"
label variable log_pop_pwt_d "ln(Population)"
label variable log_fma "ln(Foreign Market Access)"

label variable dist "Distance"
label variable distcap "Distance between capitals"
label variable ngdpd "GDP - WOE"
label variable gdp_d "GDP - WDI"
label variable pop_pwt_d "Population"
label variable is_domestic "Domestic"
label variable contig "Contiguity"
label variable comlang_off "Common language - Official"
label variable comlang_ethno "Common language - Spoken"
label variable rta "Regional trade agreement"
label variable comcol "Common colonizer after 1945"
label variable col45 "Colonial relationship after 1945"
label variable is_eu "EU membership"
label variable is_tax_haven_twz "TWZ tax haven classification"
label variable is_tax_haven_hr "H\&R tax haven classification"

label variable stat_rate "Statutory tax rate"
label variable stat_rate_squared "Squared statutory tax rate"
label variable stat_rate_cube "Cube statutory tax rate"
label variable eatr "EATR"
label variable eatr_squared "Squared EATR"
label variable eatr_cube "Cube EATR"
label variable emtr "EMTR"
label variable emtr_squared "Squared EMTR"
label variable emtr_cube "Cube EMTR"

label variable tiea_signed "TIEA signed"
label variable dtc_signed "DTC signed"
label variable tiea_enforced "TIEA enforced"
label variable dtc_enforced "DTC enforced"
label variable _dtc_signed "\# DTC signed / 100"
label variable _dtc_enforced "\# DTC enforced / 100"

save "bilateral_CbCR_regression_data.dta", replace

clear

import delimited "heckman_selection_model_data.csv"

gen log_unrelated_party_revenues = log(unrelated_party_revenues)
gen log_nb_reporting_mnes = log(nb_reporting_mnes)
gen log_related_party_revenues = log(related_party_revenues)
gen log_total_revenues = log(total_revenues)
gen log_profits = log(profit_before_tax)

gen log_dist = log(dist)
gen log_ngdpd = log(ngdpd)
gen log_gdp_d = log(gdp_d)
gen log_pop_pwt_d = log(pop_pwt_d)
gen log_fma = log(fma)

gen stat_rate_squared = stat_rate^2
gen stat_rate_cube = stat_rate^3
gen eatr_squared = eatr^2
gen eatr_cube = eatr^3
gen emtr_squared = emtr^2
gen emtr_cube = emtr^3

encode code, gen(partner)

gen is_domestic = (code == "USA")

label variable unrelated_party_revenues "UPR"
label variable nb_reporting_mnes "\# MNEs"
label variable related_party_revenues "RPR"
label variable total_revenues "TR"
label variable profit_before_tax "PBT"

label variable log_unrelated_party_revenues "ln(UPR)"
label variable log_nb_reporting_mnes "ln(\# MNEs)"
label variable log_related_party_revenues "ln(RPR)"
label variable log_total_revenues "ln(TR)"
label variable log_profits "ln(PBT)"

label variable log_dist "ln(Distance)"
label variable log_ngdpd "ln(GDP) - WOE"
label variable log_gdp_d "ln(GDP) - WDI"
label variable log_pop_pwt_d "ln(Population)"
label variable log_fma "ln(Foreign Market Access)"

label variable dist "Distance"
label variable distcap "Distance between capitals"
label variable ngdpd "GDP - WOE"
label variable gdp_d "GDP - WDI"
label variable pop_pwt_d "Population"
label variable is_domestic "Domestic"
label variable contig "Contiguity"
label variable comlang_off "Common language - Official"
label variable comlang_ethno "Common language - Spoken"
label variable rta "Regional trade agreement"
label variable comcol "Common colonizer after 1945"
label variable col45 "Colonial relationship after 1945"
label variable is_eu "EU membership"
label variable is_tax_haven_twz "TWZ tax haven classification"
label variable is_tax_haven_hr "H\&R tax haven classification"

label variable stat_rate "Statutory tax rate"
label variable stat_rate_squared "Squared statutory tax rate"
label variable stat_rate_cube "Cube statutory tax rate"
label variable eatr "EATR"
label variable eatr_squared "Squared EATR"
label variable eatr_cube "Cube EATR"
label variable emtr "EMTR"
label variable emtr_squared "Squared EMTR"
label variable emtr_cube "Cube EMTR"

label variable tiea_signed "TIEA signed"
label variable dtc_signed "DTC signed"
label variable tiea_enforced "TIEA enforced"
label variable dtc_enforced "DTC enforced"
label variable _dtc_signed "\# DTC signed / 100"
label variable _dtc_enforced "\# DTC enforced / 100"

save "heckman_selection_model_data.dta", replace
