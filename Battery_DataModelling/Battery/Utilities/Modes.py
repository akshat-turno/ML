# Method defining the classification logic
def operation_modes(df):
    modes_df = df[['vehicleNo','Date_conv','Time_conv','eventAt','soc','battery_voltage','time','odometer','vehicle_speed','current','delta_t']].copy()
    modes_df['acceleration'] = (df['vehicle_speed'].diff()*5/18) / (df['delta_t']) # Units: m/s^2
    modes_df['mode'] = "undefined"

    # For Etrio("MD93******") sign convention for current is reversed
    if modes_df['vehicleNo'].str.contains('MD93').any(): 
      modes_df['current'] = modes_df['current']*(-1)

    modes_df.loc[(modes_df['vehicle_speed'].isnull().values.any()) & (modes_df['current'] > 0) ,'mode'] = "Charging"
    modes_df.loc[(modes_df['vehicle_speed'].isnull().values.any()) & (modes_df['current'] == 0),'mode'] = "Parking"    
    modes_df.loc[(modes_df['vehicle_speed'] > 0) & (modes_df['current'] <= 0) ,'mode'] = "Driving"
    modes_df.loc[(modes_df['vehicle_speed'] == 0) & (modes_df['current'] < 0) ,'mode'] = "Idle"
    modes_df.loc[(modes_df['vehicle_speed'].notnull()) & (modes_df['current'] > 0) ,'mode'] = "Regen"
    #Timing each mode
    modes_df["dummy"] = 1
    modes_df["Frequency_per_event"] = modes_df.dummy.groupby((modes_df['mode'] != modes_df['mode'].shift()).cumsum()) .cumsum()    
    modes_df = Regen_to_IgnOn_Charging(modes_df) # Handling Edge case    
    return modes_df

#Edge_Case: IgnOn_Charging if misclassified as Regen
def Regen_to_IgnOn_Charging(modes_df):
    mode_idx = modes_df.columns.get_loc("mode")
    delta_t_idx = modes_df.columns.get_loc("Frequency_per_event")
    for i in range(len(modes_df)):
      if modes_df.iloc[i,mode_idx] == "Regen":
        if modes_df.iloc[i,mode_idx] == modes_df.iloc[i+1,mode_idx]:
          if modes_df.iloc[i+1, delta_t_idx]>20:
            modes_df.iloc[i+1, mode_idx] = "ignON_charging"
            modes_df.iloc[i-19:i+1 , mode_idx] = "ignON_charging"
      i+=1
    return modes_df



