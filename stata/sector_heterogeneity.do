use "per_industry_regression_data.dta", clear

gen log_remoteness = log(remoteness)

regress log_unrelated_party_revenues c.is_tax_haven_twz#i.sector log_ngdpd log_fma log_dist log_remoteness is_domestic contig comlang_off comlang_ethno col45 is_eu rta i.interacted_control, robust

coefplot, vertical keep(*.sector#c.is_tax_haven_twz) yline(0) coeflabels(2.sector#c.is_tax_haven_twz = "Finance", truncate(12))
