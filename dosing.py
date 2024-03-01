# Define variables volumes in Liters
vol_target = 10
vol_current = 8

# Define variables for PPM values
nitrogen_ppm = 203
potassium_ppm = 254.15
calcium_ppm = 180.351
sulphur_ppm = 48.09

# User defined values for PO4 & Mg
phosphor_ppm = 34.0714
magni_ppm = 38.88

# Define variables for nutrient ratios (the reverse ratios would be nice to hav eas well)
calcium_nitrate_Ca_NNo3 = 1.36
nitrate_calcium_Ca_NNo3 = 1/calcium_nitrate_Ca_NNo3
mkp_KPPO4 = 1.24
potassium_nitrate_KNNO3 = 2.78
mg_nitrate_NNO3Mg = 1.11
potassium_sulphate_KSSO4 = 2.26

# Define variables for measured PPM values Dummy Values
nitrogen_measured_ppm = 203 #203
potassium_measured_ppm = 196 #196
calcium_measured_ppm = 200
sulphur_measured_ppm = 40 # 50

# Define variables for source water PPM values
nitrogen_source_ppm = 10
potassium_source_ppm = 22
calcium_source_ppm = 90
sulphur_source_ppm = 15
phosphate_souce_ppm = 30
magni_souce_ppm = 95

# Total ppm for N,Ca,K

total_conce_NCaK = 645.9549893

# Define variable for total concentration in ppm (values for iron_concen and micro_Nutrient_concen were flipped)
all_concen = 10000
iron_concen = 22103.96
micro_Nutrient_concen = 331

# Define variables for pH adjustment
ph_measured = 9
ph_target = 6
ph_delta = ph_measured - ph_target
ph_after_adjustment = 7

# Initialize ph_adjustment_error
ph_adjustment_error = 0

# round to decimal places
TWO_DECIMAL = 2

"""""
TODO:
updated concentration values (at first glance,
it seems that creating for variables for every ion added with every salt at every step makes sense, 
to keep the structure open for the use of different salts)

"""""

updated_delta_potassium = 0
updated_delta_nitrogen = 0
updated_delta_calcium = 0
added_Ca_with_CaNO3 = 0 
added_N_with_KNO3 = 0
added_N_with_CaNO3 = 0
added_N_with_Mg2NO3 = 0
added_K_with_KNO3 = 0
added_K_with_MKP = 0
added_K_with_2KSO4 = 0
added_S_with_MgSO4 = 0
added_S_with_k2SO4 = 0
added_Mg_with_MgSO4 = 0
added_Mg_with_MgNO3 = 0

#  values for specific nutrients in ml
mKP_ml =  0
caNO3_ml = 0
kNO3_ml = 0
mgNO3_ml = 0
K2SO4_ml = 0
mgSO4_ml= 0
iron_ml = 0
micro_ml = 0

# Function to calculate volume of NO3H38% in pH adjustment
def no3h38_vol():
    return round(ph_delta * 0.1 * vol_current, TWO_DECIMAL)

# Function to check adjusted pH and return ph_adjustment_error
def check_adjusted_ph():
    global ph_adjustment_error  # Use the global ph_adjustment_error variable. This comes from Database.
    ph_adjustment_error = ph_after_adjustment - ph_target

# Execute pH functions
vol_no3h38 = no3h38_vol()
adjusted_ph_adjustment_error = check_adjusted_ph()


# Function to calculate Deltaion
def calculate_Deltaion(target_ion_con, deter_ion_con, vol_current, source_ion_con, vol_target):
    delta_ion = (target_ion_con - deter_ion_con) * vol_current + (target_ion_con - source_ion_con) * (vol_target - vol_current)
    return delta_ion

# calculate delta values for specific nutrients
updated_delta_nitrogen = initial_delta_nitrogen = round(calculate_Deltaion(nitrogen_ppm, nitrogen_measured_ppm, vol_current, nitrogen_source_ppm, vol_target), TWO_DECIMAL)
updated_delta_calcium = initial_delta_calcium = round(calculate_Deltaion(calcium_ppm, calcium_measured_ppm, vol_current, calcium_source_ppm, vol_target), TWO_DECIMAL)
updated_delta_potassium = initial_delta_potassium = round(calculate_Deltaion(potassium_ppm, potassium_measured_ppm, vol_current, potassium_source_ppm, vol_target), TWO_DECIMAL)
updated_delta_sulphur = initial_delta_sulphur = round(calculate_Deltaion(sulphur_ppm, sulphur_measured_ppm, vol_current, sulphur_source_ppm, vol_target), TWO_DECIMAL)



print("Delta Nitrogen:", initial_delta_nitrogen, "mg")
print("Delta Calcium:", initial_delta_calcium, "mg")
print("Delta Potassium:", initial_delta_potassium, "mg")
print("Delta Sulphur:", initial_delta_sulphur, "mg\n")

print("NO3H38%:", vol_no3h38, "ml")
print("N in NO3H38%:", round(vol_no3h38 * 103.96, TWO_DECIMAL), "mg")        # 84 mg was the amount of N/(g NO3H), 103.96 is mg N in one ml of NO3H
updated_delta_nitrogen = round(initial_delta_nitrogen - vol_no3h38 * 103.96, TWO_DECIMAL)
print("Delta N after substarcting NO3H38%:", updated_delta_nitrogen, "mg")

# Function to calculate milligrams per part dosing
def mg_p_dosing(ppm):
    dosing = (ppm / total_conce_NCaK) * (updated_delta_nitrogen + updated_delta_calcium + updated_delta_potassium)
    return dosing

# Function to calculate ratios of ions
def ratio_calculation(delta, ratio):
    specific_ion_part = delta/ratio
    return specific_ion_part

# Function to calculate micro and iron nutrients implementation
def micro_nuterients(ratio):
    micro_concentration = ratio * (updated_delta_calcium + required_P + required_Mg + updated_delta_potassium + updated_delta_potassium + updated_delta_sulphur)
    return micro_concentration

# Function to calculate nuterient solution implementation
def volume_NS():
    water_volume = (vol_target * 1000) - ((vol_current * 1000) + (mKP_ml + caNO3_ml + kNO3_ml + mgNO3_ml + K2SO4_ml + mgSO4_ml + iron_ml + micro_ml) + vol_no3h38)
    return water_volume 


# Function to calculate Flow rate
def flow_Rate(amount_in_mg, ppm):
    flowRate = (amount_in_mg/ppm)/144
    return flowRate

# Finding P and Mg required here
required_P = round(mg_p_dosing(phosphor_ppm), TWO_DECIMAL)
added_K_with_MKP = round(required_P * mkp_KPPO4, TWO_DECIMAL) 
updated_delta_potassium = round(initial_delta_potassium - added_K_with_MKP, TWO_DECIMAL)
required_Mg = round(mg_p_dosing(magni_ppm), TWO_DECIMAL)
# added_N_with_Mg2NO3 = round(required_Mg * mg_nitrate_NNO3Mg, TWO_DECIMAL)




# tree branch where Ca required > 0 is checked
if initial_delta_calcium > 0:
    caNO3_ml = round((initial_delta_calcium/10000) * 1000, TWO_DECIMAL)
    print("\nTo be added CaNO3:", initial_delta_calcium, "mg and solution to pump", caNO3_ml, "ml")

    added_N_with_CaNO3 = round(ratio_calculation(initial_delta_calcium, calcium_nitrate_Ca_NNo3), TWO_DECIMAL)
    added_Ca_with_CaNO3 = round(ratio_calculation(initial_delta_calcium, nitrate_calcium_Ca_NNo3), TWO_DECIMAL)
    updated_delta_calcium = round(updated_delta_calcium - added_Ca_with_CaNO3, TWO_DECIMAL)
    updated_delta_nitrogen = round(updated_delta_nitrogen - added_N_with_CaNO3, TWO_DECIMAL)
    print("N in CaNO3:", added_N_with_CaNO3, "mg")

    print("\nP Dosing:", required_P, "mg")
    mKP_ml = round((added_K_with_MKP/10000) * 1000, TWO_DECIMAL)
    print("To be added MKP/KH2PO4:", added_K_with_MKP, "mg and solution to pump", mKP_ml, "ml")

    print("Delta N after substracting CaNO3:", updated_delta_nitrogen, "mg")


else:
    print("Sufficient Ca levels")


# tree branch where K required > K injected is checked
"""""
# (since "initial_delta_potassium" is only used for printing it doesn't matter which you use, but you want to use the 
  updated value at every step of the decision tree)
"""""
if updated_delta_potassium > added_K_with_MKP:        
    kNO3_ml = round((updated_delta_potassium/10000) * 1000, TWO_DECIMAL)
    print("\nTo be added KNO3:", updated_delta_potassium, "mg and solution to pump", kNO3_ml, "ml")

    # calculte added ratio of N
    added_N_with_KNO3 = round(ratio_calculation(updated_delta_potassium, potassium_nitrate_KNNO3), TWO_DECIMAL)
    print("N in KNO3:", added_N_with_KNO3, "mg")

else:
    added_N_with_Mg2NO3 = round(required_Mg * 1.17, TWO_DECIMAL)
    print("Mg Dosing:", required_Mg, "mg")
    mgNO3_ml = round((added_N_with_Mg2NO3/10000) * 1000, TWO_DECIMAL)
    print("To be added MG2NO3 =", added_N_with_Mg2NO3, "mg and solution to pump", mgNO3_ml, "ml")
    updated_delta_nitrogen = updated_delta_nitrogen - added_N_with_Mg2NO3
    print("Mg required complete. Updated delta N = ", updated_delta_nitrogen, "mg")



# tree branch where NO3 injected > NO3 required is checked
if  added_N_with_KNO3 > updated_delta_nitrogen:
        
    updated_delta_nitrogen = round(updated_delta_nitrogen - added_N_with_KNO3, TWO_DECIMAL) # N required - NNO3
    print("Delta N after substracting KNO3:", updated_delta_nitrogen, "mg")
    reduced_K = round(updated_delta_nitrogen * potassium_nitrate_KNNO3, TWO_DECIMAL) # to know how much K is added with N from previous step
    print("K required to be reduced from Delta K:", reduced_K, "mg")
    updated_delta_potassium = round(updated_delta_potassium + reduced_K, TWO_DECIMAL)

    print("\nK2SO4 injection choosen to cover K since N required = N injected:", updated_delta_potassium, "mg")
    K2SO4_ml = round((updated_delta_potassium/10000) * 1000, TWO_DECIMAL)
    print("K2SO4 injection:", K2SO4_ml, "ml")
    added_S_with_k2SO4 = round(ratio_calculation(updated_delta_potassium, potassium_sulphate_KSSO4), TWO_DECIMAL)
    updated_delta_sulphur = round(updated_delta_sulphur - added_S_with_MgSO4, TWO_DECIMAL)
    print("S in K2SO4:", added_S_with_k2SO4, "mg")

else:   
    print("\nSufficient KNO3 levels. Now add MgNO3")
    print("Mg Dosing:", required_Mg, "mg")
    added_N_with_Mg2NO3 = round(required_Mg * 1.17, TWO_DECIMAL) # 1.17 is the ratio of N-NO3/Mg
    updated_delta_nitrogen = round(updated_delta_nitrogen - added_N_with_Mg2NO3, TWO_DECIMAL)
    mgNO3_ml = round((added_N_with_Mg2NO3/10000) * 1000, TWO_DECIMAL)
    print("Mg required complete with MG2NO3. Updated delta N =", updated_delta_nitrogen, "mg and solution to pump", mgNO3_ml, "ml")
    print("N in MG2NO3 =", added_N_with_Mg2NO3, "mg")



# tree branch where N injected > NO3 required is checked
if  updated_delta_nitrogen < 0:

    # add MgSO4
    print("\nMg Dosing:", required_Mg, "mg")
    added_S_with_MgSO4 = round(required_Mg * 1.32, TWO_DECIMAL) # 1.32 is the ratio of S-SO4/Mg
    updated_delta_sulphur = round(updated_delta_sulphur - added_S_with_MgSO4, TWO_DECIMAL)
    mgSO4_ml = round((added_S_with_MgSO4/10000) * 1000, TWO_DECIMAL)
    print("Mg required complete with MgSO4. Updated delta S =", updated_delta_sulphur, "mg and solution to pump", mgSO4_ml, "ml")
    print("S in MgSO4:", added_S_with_MgSO4, "mg")


else:
    # split MgNO3%, CaNO3%, KNO3% for remaining N
    ten_percent = round(0.10 * updated_delta_nitrogen, TWO_DECIMAL)
    forty_percent = round(0.40 * updated_delta_nitrogen, TWO_DECIMAL)
    fifty_percent = round(0.50 * updated_delta_nitrogen, TWO_DECIMAL)
    mgNO3_ml = round(mgNO3_ml + ((ten_percent/10000) * 1000), TWO_DECIMAL)
    caNO3_ml = round(caNO3_ml + ((forty_percent/10000) * 1000), TWO_DECIMAL)
    kNO3_ml = round(kNO3_ml + ((fifty_percent/10000) * 1000), TWO_DECIMAL)
    print("\nMgNO3%, CaNO3%, KNO3% to be added to fulfill N req", ten_percent + forty_percent + fifty_percent, "mg\n") # to be checked


# Display the final amount of solution's injection
print("\n*************************** FINAL INJECTION ***************************")
print("CaNO3 injection:", caNO3_ml, "ml")
print("MKP injection:", mKP_ml, "ml")
print("KNO3 injection:", kNO3_ml, "ml")
print("MgNO3 injection:", mgNO3_ml, "ml")
print("K2SO4 injection:", K2SO4_ml, "ml")
print("MgSO4 injection:", mgSO4_ml, "ml")
print("NO3H38% for pH injection:", vol_no3h38, "ml\n")
iron_mg = micro_nuterients(0.0011)
micro_mg = micro_nuterients(0.0032)
iron_ml = round((iron_mg/10000) * 1000, TWO_DECIMAL)
micro_ml = round((micro_mg/10000) * 1000, TWO_DECIMAL)

print("Micro nutrient injection:", micro_ml, "ml")
print("Iron nutrient injection:", iron_ml, "ml\n")
print("On time iron pump:", round(flow_Rate(iron_mg, iron_concen), 4), "minutes")
print("On time micro nutrients pump:", round(flow_Rate(micro_mg, micro_Nutrient_concen), 4), "minutes")
print("Iron nutrient injection:", iron_ml, "ml\n")

print("Top up volume water:", round(volume_NS()/1000, TWO_DECIMAL), "liters\n")
