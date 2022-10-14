#Method for plotting and comparing primary variables for each mode
import matplotlib.pyplot as plt
def plot_mode(df):
# from google.colab import output
#     output.enable_custom_widget_manager()
    get_ipython().run_line_magic('matplotlib', 'widget')

#     plt.rcParams["figure.figsize"] = [17.00, 5]
#     plt.rcParams["figure.autolayout"] = True

    #Plotting current and vehicle speed for Regen, driving and charging
    ax1 = df[df['mode'] == 'Driving'].plot.scatter(x='time', y='current',color="black",label ="Drive_current") 
    df[df['mode'] == 'Regen'].plot.scatter(ax=ax1, x='time', y='current',color="red",label ="Regen_current")
    df[df['mode'] == 'Charging'].plot.scatter(ax=ax1, x='time', y='current',color="blue",label ="Charging_current")
    df[df['mode'] == 'Driving'].plot.scatter(ax=ax1, x='time', y='vehicle_speed',color="green",label ="Drive_vehicle_speed")
    df[df['mode'] == 'Regen'].plot.scatter(ax=ax1, x='time', y='vehicle_speed',color="cyan",label ="Regen_vehicle_speed")
    df[df['mode'] == 'Charging'].plot.scatter(ax=ax1, x='time', y='vehicle_speed',color="orange",label ="Charging_vehicle_speed")

    #Plotting current for Regen, driving and idling
    ax2 = df[df['mode'] == 'Driving'].plot.scatter(x='time', y='current',color="black",label ="Drive_current") 
    df[df['mode'] == 'Regen'].plot.scatter(ax=ax2, x='time', y='current',color="red",label ="Regen_current")
    df[df['mode'] == 'Idle'].plot.scatter(ax=ax2, x='time', y='current',color="blue",label ="Idle_current")    

    #Plotting vehicle speed for Regen, driving and idling
    ax3 = df[df['mode'] == 'Driving'].plot.scatter(x='time', y='vehicle_speed',color="black",label ="Drive_vehicle_speed") 
    df[df['mode'] == 'Regen'].plot.scatter(ax=ax3, x='time', y='vehicle_speed',color="red",label ="Regen_vehicle_speed")
    df[df['mode'] == 'Idle'].plot.scatter(ax=ax3, x='time', y='vehicle_speed',color="blue",label ="Idle_vehicle_speed")

    #Plotting vehicle speed for Regen
    ax4 = df[df['mode'] == 'Regen'].plot.scatter(x='time', y='vehicle_speed',color="black",label ="Regen_vehicle_speed")

def savefig(filename, crop = True):
    if crop == True:
#        plt.savefig('{}.pgf'.format(filename), bbox_inches='tight', pad_inches=0)
        plt.savefig('{}.pdf'.format(filename), bbox_inches='tight', pad_inches=0)        
    else:
#        plt.savefig('{}.pgf'.format(filename))
        plt.savefig('{}.pdf'.format(filename))
        