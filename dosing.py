# Define variables volumes
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

# Define variables for nutrient ratios
calcium_nitrate_Ca_NNo3 = 1.36
mkp_KPPO4 = 1.24
potassium_nitrate_KNNO3 = 2.78
mg_nitrate_NNO3Mg = 1.11
potassium_sulphate_KSSO4 = 2.26

# Define variables for measured PPM values Dummy Values
nitrogen_measured_ppm = 225 #203
potassium_measured_ppm = 310 #196
calcium_measured_ppm = 200
sulphur_measured_ppm = 50

# Define variables for source water PPM values
nitrogen_source_ppm = 10
potassium_source_ppm = 22
calcium_source_ppm = 90
sulphur_source_ppm = 15
phosphate_souce_ppm = 30
magni_souce_ppm = 95

# Total ppm for N,Ca,K

total_conce_NCaK = 645.9549893

# Define variable for total concentration
all_concen = 10000

# Define variables for pH adjustment
ph_measured = 9
ph_target = 7
ph_delta = ph_measured - ph_target
ph_after_adjustment = 7

# Initialize ph_error
ph_error = 0

# round to decimal places
TWO_DECIMAL = 2

# updated concentration values

updated_delta_potassium = 0
updated_delta_nitrogen = 0
updated_delta_calcium = 0
added_N_with_KNO3 = 0
added_N_with_CaNO3 = 0
added_K_with_MKP = 0
added_K_with_K2SO4 = 0

# Function to calculate percentage of NO3H3.8 in pH adjustment
def no3h38_perc():
    return ph_delta * 0.1 * vol_current

# Function to check adjusted pH and return ph_error
def check_adjusted_ph():
    global ph_error  # Use the global ph_error variable
    ph_error = ph_after_adjustment - ph_target

# Example usage of the functions
percentage_no3h38 = no3h38_perc()
adjusted_ph_error = check_adjusted_ph()


# Function to calculate Deltaion
def calculate_Deltaion(target_ion_con, deter_ion_con, vol_current, source_ion_con, vol_target):
    delta_ion = (target_ion_con - deter_ion_con) * vol_current + (target_ion_con - source_ion_con) * (vol_target - vol_current)
    return delta_ion

# calculate delta values for specific nutrients
updated_delta_nitrogen = initial_delta_nitrogen = round(calculate_Deltaion(nitrogen_ppm, nitrogen_measured_ppm, vol_current, nitrogen_source_ppm, vol_target), TWO_DECIMAL)
updated_delta_calcium = initial_delta_calcium = round(calculate_Deltaion(calcium_ppm, calcium_measured_ppm, vol_current, calcium_source_ppm, vol_target), TWO_DECIMAL)
updated_delta_potassium = initial_delta_potassium = round(calculate_Deltaion(potassium_ppm, potassium_measured_ppm, vol_current, potassium_source_ppm, vol_target), TWO_DECIMAL)
initial_delta_sulphur = round(calculate_Deltaion(sulphur_ppm, sulphur_measured_ppm, vol_current, sulphur_source_ppm, vol_target), TWO_DECIMAL)

#  values for specific nutrients in ml
mKP_ml =  0
caNO3_ml = 0
kNO3_ml = 0
mgNO3_ml = 0
k2SO4_ml = 0

print("Delta Nitrogen:", initial_delta_nitrogen, "mg")
print("Delta Calcium:", initial_delta_calcium, "mg")
print("Delta Potassium:", initial_delta_potassium, "mg")
print("Delta Sulphur:", initial_delta_sulphur, "mg\n")
# print("Nitrogen injection ml:", delta_nitrogen_ml, "ml")
# print("Calcium injection ml:", delta_calcium_ml, "ml")
# print("Potassium injection ml:", delta_potassium_ml, "ml")
# print("Sulphur injection ml:", delta_sulphur_ml, "ml\n")
print("NO3H38%:", percentage_no3h38, "ml")
print("N in NO3H38%:", percentage_no3h38 * 84, "mg")
updated_delta_nitrogen = round(initial_delta_nitrogen - percentage_no3h38 * 84, TWO_DECIMAL)
print("Delta N after substarcting NO3H38%:", updated_delta_nitrogen, "mg")

# Function to calculate milligrams per part dosing
def mg_p_dosing(ppm):
    dosing = (ppm / total_conce_NCaK) * (updated_delta_nitrogen + updated_delta_calcium + updated_delta_potassium)
    return dosing

# Function to calculate ratios of ions
def ratio_calculation(delta, ratio):
    specific_ion_part = delta/ratio
    return specific_ion_part

# Function to calculate micro nutrients
def micro_nuterients(ratio):
    micro_concentration = ratio/(initial_delta_nitrogen + initial_delta_calcium + initial_delta_potassium)

# Finding P and Mg required here
required_P = round(mg_p_dosing(phosphor_ppm), TWO_DECIMAL)
added_K_with_MKP = round(required_P * mkp_KPPO4, TWO_DECIMAL) # TODO change the ratio as im Mg approach if correct.
updated_delta_potassium = round(initial_delta_potassium - added_K_with_MKP, TWO_DECIMAL)
required_Mg = round(mg_p_dosing(magni_ppm), TWO_DECIMAL)
# added_N_with_Mg2NO3 = round(required_Mg * mg_nitrate_NNO3Mg, TWO_DECIMAL)




# tree branch where Ca required > 0 is checked
if initial_delta_calcium > 0:
    caNO3_ml = round((initial_delta_calcium/10000) * 1000, TWO_DECIMAL)
    print("\nTo be added CaNO3:", initial_delta_calcium, "mg and solution to pump", caNO3_ml, "ml")
    added_N_with_CaNO3 = round(ratio_calculation(initial_delta_calcium, calcium_nitrate_Ca_NNo3), TWO_DECIMAL)
    # print("Add MKP/KH2PO4:", round(ratio_calculation(updated_delta_potassium, mkp_KPPO4), TWO_DECIMAL), "ml")
    mKP_ml = round((added_K_with_MKP/10000) * 1000, TWO_DECIMAL)
    print("\nP Dosing:", required_P, "mg")
    print("To be added MKP/KH2PO4:", added_K_with_MKP, "mg and solution to pump", mKP_ml, "ml")
    updated_delta_nitrogen = round(updated_delta_nitrogen - added_N_with_CaNO3, TWO_DECIMAL)
    print("Delta N after substracting CaNO3:", updated_delta_nitrogen, "mg")
else:
    print("Sufficient Ca levels")


# tree branch where K required > K injected is checked
if initial_delta_potassium > added_K_with_MKP:
    kNO3_ml = round((updated_delta_potassium/10000) * 1000, TWO_DECIMAL)
    print("\nTo be added KNO3:", updated_delta_potassium, "mg and solution to pump", kNO3_ml, "ml")
    # calculte added ratio of N
    added_N_with_KNO3 = round(ratio_calculation(updated_delta_potassium,potassium_nitrate_KNNO3), TWO_DECIMAL)
    print("N in KNO3:", added_N_with_KNO3, "mg")
    # updated_delta_nitrogen = updated_delta_nitrogen - added_N_with_KNO3
    # print("delta N with KNO3:", updated_delta_nitrogen)

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
    print("K required to be reduced:", reduced_K, "mg")
    updated_delta_potassium = round(updated_delta_potassium + reduced_K, TWO_DECIMAL)
    print("\nK2SO4 injection since N required = N injected:", updated_delta_potassium, "mg")
    k2SO4_ml = round((updated_delta_potassium/10000) * 1000, TWO_DECIMAL)
    print("K2SO4 injection:", k2SO4_ml, "ml")

    """""
    TODO: add how much S is added as well but need MgSO4 ratio
    """""

    # add K2SO4 to cover K Delta
    # added_K_with_K2SO4 = round(ratio_calculation(updated_delta_potassium,potassium_sulphate_KSSO4), TWO_DECIMAL)

else:   
    print("\nSufficient KNO3 levels. Now add mg2no3")
    print("Mg Dosing:", required_Mg, "mg")
    added_N_with_Mg2NO3 = round(required_Mg * 1.17, TWO_DECIMAL)
    updated_delta_nitrogen = round(updated_delta_nitrogen - added_N_with_Mg2NO3, TWO_DECIMAL)
    print("Mg required complete. Updated delta N =", updated_delta_nitrogen, "mg")
    mgNO3_ml = round((added_N_with_Mg2NO3/10000) * 1000, TWO_DECIMAL)
    print("To be added MG2NO3 =", added_N_with_Mg2NO3, "mg and solution to pump", mgNO3_ml, "ml")


# tree branch where N injected > NO3 required is checked
if  updated_delta_nitrogen < 0:
    # add MgSO4
    
    print("\nMgSO4 injection:", round(required_Mg * 2.11, TWO_DECIMAL), "mg") # fake to be corrected after getting orignal ratio

else:
    # split MgNO3%, CaNO3%, KNO3% for remaining N
    ten_percent = round(0.10 * updated_delta_nitrogen, TWO_DECIMAL)
    forty_percent = round(0.40 * updated_delta_nitrogen, TWO_DECIMAL)
    fifty_percent = round(0.50 * updated_delta_nitrogen, TWO_DECIMAL)
    print("\nMgNO3%, CaNO3%, KNO3% to be added to fulfill N req", ten_percent, "mg", forty_percent, "mg", fifty_percent, "mg\n") # to be checked