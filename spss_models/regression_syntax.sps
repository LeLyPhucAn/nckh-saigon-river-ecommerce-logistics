* Cu phap SPSS hoi quy kinh te luong 28 phuong ven song Sai Gon.
GET DATA /TYPE=TXT
  /FILE="D:/NCKH/De tai dong song/Mo hinh nckh song/spss_models/spss_ward_data.csv"
  /ENCODING='UTF8'
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=
  ward_name A50
  district A30
  pop_density_k_per_km2 F8.2
  dist_to_hub_km F8.2
  land_rent_mil_vnd_m2 F8.2
  road_ris_score F8.2
  est_saving_pct F8.2
  demand_index_Y F8.2.
EXECUTE.

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA COLLIN TOL
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT demand_index_Y
  /METHOD=ENTER pop_density_k_per_km2 dist_to_hub_km land_rent_mil_vnd_m2 road_ris_score est_saving_pct.
