clear

import delimited "foreign_market_access_data.csv"

generate log_trade = log(v)

egen exp_x_y_FE = concat(t iso_3digit_alpha_exporter), punct(_EXP_)
egen imp_x_y_FE = concat(t iso_3digit_alpha_importer), punct(_IMP_)

encode exp_x_y_FE, generate(exp_x_y_FE_encoded)
encode imp_x_y_FE, generate(imp_x_y_FE_encoded)

xtset imp_x_y_FE_encoded

xtreg log_trade log_dist contig comcol col45 comlang_off comlang_ethno rta i.exp_x_y_FE_encoded, fe

predict mu_j_t, u

replace dist = exp(log_dist)

generate temp = _b[contig] * contig + _b[comcol] * comcol + _b[col45] * col45 + _b[comlang_off] * comlang_off + _b[comlang_ethno] * comlang_ethno + _b[rta] * rta
replace temp = exp(temp)
gen phi_i_j_t = dist^(_b[log_dist]) * temp

gen variable_to_sum = exp(mu_j_t) * phi_i_j_t

collapse (sum) variable_to_sum, by(exp_x_y_FE)

export delimited foreign_market_access.csv, delimiter(",") replace
