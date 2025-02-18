from Tools import *

pattern = r"_ER([\d\.]+)_T([\d\.]+).csv"
lenght = 100 


folder_Detailed = "/work/kotlarcm/WORK/Tools_Database/Comparision_0D/Mech_Input/Detailed"
folder_Reduced = "/work/kotlarcm/WORK/Tools_Database/Comparision_0D/Mech_OptiSmoke_2/Gen500"

Output_Folder = "/work/kotlarcm/WORK/Tools_Database/Comparision_0D/Mech_OptiSmoke_2/Change_Gen500"
Name_Output_Det ="Change_Detailed.csv"
Name_Output_Red = "Change_Gen500.csv"

all_csv_detailed = glob.glob(os.path.join(folder_Detailed,"*.csv"))
all_csv_reduced = glob.glob(os.path.join(folder_Reduced,"*.csv"))

scaler = MinMaxScaler()
all_data_ref = pd.DataFrame()
all_data_red = pd.DataFrame()
all_scaler =[] 
all_commun_grid = []
    
for csv_det in all_csv_detailed :
    New_data = pd.DataFrame() 
    data = pd.read_csv(csv_det)
    match = re.search(pattern,csv_det)
    ER = float(match.group(1)) 
    Tinit = float(match.group(2)) 
    
    #Shift 
    shift_grid = data["t"]-ai_delay(data)
    commun_grid = np.linspace(min(shift_grid),max(shift_grid),lenght)
    list_species = [col for col in data.columns if col.startswith("Y_")] # Only Species
    all_commun_grid.append(commun_grid)
    
    #Interpol
    for spec in list_species :
            New_data[spec] = interp(shift_grid,data[spec],commun_grid)
    
    #Scaler
    scaler.fit(New_data) 
    New_data = scaler.transform(New_data)  
    all_scaler.append(scaler) 
    
    #Add Info 
    New_data["Tinit"] = Tinit 
    New_data["ER"] = ER
    New_data["commun_grid"] = commun_grid
    New_data["T"] = data["T"]
    New_data["AI_delay"] = ai_delay(data)
    all_data_ref =pd.concat([all_data_ref,New_data],ignore_index=True)

all_data_ref.to_csv(os.path.join(Output_Folder,Name_Output_Det))

ind = 0 
for csv_red in all_csv_reduced : 
    New_data = pd.DataFrame() 
    data = pd.read_csv(csv_red)
    match = re.search(pattern,csv_red)
    ER = float(match.group(1)) 
    Tinit = float(match.group(2))  
    # print(ER)
    # print(Tinit)
    shift_grid = data["t"]-ai_delay(data)
    list_species = [col for col in data.columns if col.startswith("Y_")]
    loc_data_ref = all_data_ref[(all_data_ref["ER"]==ER)&(all_data_ref["Tinit"]==Tinit)]
    loc_commun_grid = loc_data_ref["commun_grid"]
    # print("Commun grid from dataref")
    # print(loc_commun_grid)
    for spec in list_species :
        New_data[spec] = interp(shift_grid,data[spec],loc_commun_grid)
    
    scaler = all_scaler[ind]   
    New_data = scaler.transform(New_data)  
      
    New_data["Tinit"] = Tinit 
    New_data["ER"] = ER
    New_data["commun_grid"] = loc_data_ref["commun_grid"]
    # print(New_data["commun_grid"])
    New_data["T"] = data["T"]
    New_data["AI_delay"] = ai_delay(data) 
    
    all_data_red =pd.concat([all_data_red,New_data],ignore_index=True)
             
all_data_red.to_csv(os.path.join(Output_Folder,Name_Output_Red))



#Compute Err : 
list_err = [col for col in all_data_red.columns if col.startswith("Y_")]
list_err.append("AI_delay")

# Compute the absolute difference for all selected columns in one operation
Err_Abs = (all_data_ref[list_err] - all_data_red[list_err]).abs()

Err_Abs["Tinit"] = all_data_ref["Tinit"] 
Err_Abs["ER"] = all_data_ref["ER"]
Err_Abs["commun_grid"] = all_data_ref["commun_grid"]

Err_Abs.to_csv(os.path.join(Output_Folder,"Err_Absolute.csv"))
