python tax_treaties_compiler.py

python foreign_market_access.py

stata-mp -e do foreign_market_access.do

python regression_data.py

stata-mp -e do labels.do

stata-mp -e do benchmark_regressions.do
