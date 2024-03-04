import pandas as pd
import os
from datetime import datetime as dt
import numpy as np
import calendar
import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import webbrowser
# import warnings


# warnings.filterwarnings("ignore", category=DeprecationWarning) 


'''Note: Date not included in the digitalised file (.csv) is interpreted as dry day! 
        Missing day has a date but no data in the .csv file! 
        Snow days have -s after the date in the .csv file!
        -r after the date means points (without possibility of overlap) were manually added.'''


t_int = 20          # time interval in minutes used for correction of overlapping points on the upper and lower branches of the curve
skok_razpon = 5000  # razpon med tockami zgornje in spodnje krivulje pri praznenju posode
razpon_tocka = 7000 # razpon med tockami pri detekciji tocke izven krivulje

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action="store_true", help='Podrobnejsi izpis popravkov prekrivanja in kreiranih datotek')
args = parser.parse_args()
verbose = args.verbose

verboseprint = print if verbose else lambda *a, **k: None

now = dt.now()
current_time = now.strftime("%d-%m-%Y_%H-%M-%S")
plot_name = 'Slike_grafov_' + current_time + '.pdf'
pp = PdfPages(plot_name)



# create a list of all the .csv files in the working directory
listfiles = [fi for fi in os.listdir() if fi.endswith(".csv")]
listfiles.sort()

# split the date string into seperate numbers
def split(word):
    return [char for char in word]

# creates coordinates to add to the dataset
# x koordinata tece od 00001 namesto od 00000, ker pri programu za izracun kolicine padavin mora biti vrednost razlicna od 0 (!=0)
df_coord = pd.DataFrame([['01', '00001', '20000'],['01', '24000', '20000'],['01', '00001', '10000']],columns=['code', 'x', 'y'])

# code for a dry day
df_dry = pd.DataFrame([['02', '12345', '12345']],columns=['code', 'x', 'y'])

# code for a missing day
df_missing = pd.DataFrame([['03', '12345', '12345']],columns=['code', 'x', 'y'])

# code for a snow day
df_snow = pd.DataFrame([['04', '12345', '12345']],columns=['code', 'x', 'y'])

# code for the end of a sequence
df_end = pd.DataFrame([['0#', '12345', '12345']],columns=['code', 'x', 'y'])



for file_num in listfiles:
    
    df = pd.read_csv(file_num)
    
    # list of all the dates present in the dataframe
    date_table_list=[]
    i = 0
    while i < df.shape[1]:
        try:
            if '-s' in df.columns[i]:
                sneg = df.columns[i]
                sneg = dt.strptime(sneg.replace('-s',''), '%d-%m-%Y')
                date_table_list.append(sneg)
                i +=2
            elif '-r' in df.columns[i]:
                rocno = df.columns[i]
                rocno = dt.strptime(rocno.replace('-r',''), '%d-%m-%Y')
                date_table_list.append(rocno)
                i +=2
            else:
                dez = dt.strptime(df.columns[i], '%d-%m-%Y')
                date_table_list.append(dez)
                i +=2
        except ValueError:
            i +=2

    # populate a list of all dates in a month in the DataFrame
    # itermonthdates(year, month) This iterator will return all days (as datetime.date objects) for the month and all days before the start of the month or after the end of the month that are required to get a complete week.
    date_month_list=[]
    cal= calendar.Calendar() 
    # iterating with itermonthdates
    for day in cal.itermonthdates(date_table_list[0].year, date_table_list[0].month):  
        date_month_list.append(day) 
    # filter the dates for only the relevant month
    date_month_list_filtered = list(filter(lambda x: x.month == date_table_list[0].month, date_month_list))

    # create a dictionary table of all the dates present in the dataframe
    def dict_table_():
        df_date_table_list1 = pd.DataFrame(columns = ['Datum', 'Indeks', 'Padavina', 'Time_interval'])
        j = 0
        while j < df.shape[1]:
            try:
                if '-s' in df.columns[j]:
                    sneg = df.columns[j]
                    sneg = dt.strptime(sneg.replace('-s',''), '%d-%m-%Y')
                    df_sneg = pd.DataFrame({'Datum' : [sneg], 'Indeks' : [j], 'Padavina' : ['sneg'], 'Time_interval' : [15]})
                    df_date_table_list1 = pd.concat([df_date_table_list1,df_sneg], ignore_index = True)
                    # df_date_table_list1 = df_date_table_list1.append({'Datum' : sneg, 'Indeks' : j, 'Padavina' : 'sneg', 'Time_interval' : t_int}, 
                    #     ignore_index = True)
                    j +=2
                elif '-r' in df.columns[j]:
                    rocno = df.columns[j]
                    rocno = dt.strptime(rocno.replace('-r',''), '%d-%m-%Y')
                    df_rocno = pd.DataFrame({'Datum' : [rocno], 'Indeks' : [j], 'Padavina' : ['dez'], 'Time_interval' : [0]})
                    df_date_table_list1 = pd.concat([df_date_table_list1,df_rocno], ignore_index = True)
                    # df_date_table_list1 = df_date_table_list1.append({'Datum' : rocno, 'Indeks' : j, 'Padavina' : 'dez', 'Time_interval' : 0}, 
                    #     ignore_index = True)
                    j +=2
                elif (df.shape[0] == 1 and ('-s' and '-r' not in df.columns[j])) or (df.shape[0] > 1 and ('-s' and '-r' not in df.columns[j] and (pd.isna(df.iloc[1,j]) == True))):
                    manj = df.columns[j]
                    manj = dt.strptime(df.columns[j], '%d-%m-%Y')
                    df_manj = pd.DataFrame({'Datum' : [manj], 'Indeks' : [j], 'Padavina' : ['manjka'], 'Time_interval' : [15]})
                    df_date_table_list1 = pd.concat([df_date_table_list1,df_manj], ignore_index = True)
                    # df_date_table_list1 = df_date_table_list1.append({'Datum' : manj, 'Indeks' : j, 'Padavina' : 'manjka', 'Time_interval' : t_int}, 
                    #     ignore_index = True)
                    j +=2         
                else:
                    dez = dt.strptime(df.columns[j], '%d-%m-%Y')
                    df_dez = pd.DataFrame({'Datum' : [dez], 'Indeks' : [j], 'Padavina' : ['dez'], 'Time_interval' : [15]})
                    df_date_table_list1 = pd.concat([df_date_table_list1,df_dez], ignore_index = True)
                    # df_date_table_list1 = df_date_table_list1.append({'Datum' : dez, 'Indeks' : j, 'Padavina' : 'dez', 'Time_interval' : t_int}, 
                    #     ignore_index = True)
                    j +=2
            except ValueError:
                j +=2
        df_date_table_list1.sort_values(by=['Datum'], inplace=True)          # sorts the dates if the digitalizations are not in chronological order 
        df_date_table_list1 = df_date_table_list1.reset_index(drop=True)     # reset row index values
        return df_date_table_list1
    dict_table = dict_table_()

            
    # creating a header with station name and date
    def df_head(day):
        # read the date from column name and convert it to date string
        date_string = date_month_list_filtered[day].strftime('%y%m%d%H%M')
        # print the date in the form of izhodni format
        df_fraction1 = pd.DataFrame([['0*', '00000', '00000']],columns=['code', 'x', 'y'])
        for num in os.path.splitext(file_num)[0][0:3]:      # insert .csv filename of the second file in the working directory in the form of izhodni format
            df_postaja = pd.DataFrame({'code': ['0'+num], 'x': ['12345'], 'y': ['12345']})
            df_fraction1 = pd.concat([df_fraction1,df_postaja], ignore_index=True)
            # df_fraction1 = df_fraction1.append({'code': '0'+num, 'x': '12345', 'y': '12345'}, ignore_index=True)
        for value in range(10):
            df_dan = pd.DataFrame({'code': ['0'+split(date_string)[value]], 'x': ['12345'], 'y': ['12345']})
            df_fraction1 = pd.concat([df_fraction1,df_dan], ignore_index=True)
            # df_fraction1 = df_fraction1.append({'code': '0'+split(date_string)[value], 'x': '12345', 'y': '12345'}, ignore_index=True)
        return df_fraction1



# data points for one day in a specified output format for plotting
    def df_graf_(col, cas_interval):
        df_temp_g = df[[df.columns[col],df.columns[col+1]]]   # display first and second columns (X and Y)
        df_temp_g = df_temp_g.dropna().drop(index=0) # drop rows with any column having NA/null data and first row
        df_temp_g = df_temp_g.apply(pd.to_numeric)  # convert values in table to float
        df_temp_g.iloc[:, 1] = df_temp_g.iloc[:, 1].transform(lambda x: x-x.min())  # shift y values to 0+
        df_temp_g = df_temp_g.sort_values(by=[df_temp_g.columns[0],df_temp_g.columns[1]], ascending = [True, False])    # sort by values in first (X) column and then if x are the same by y column descending
        df_temp_g = df_temp_g.reset_index(drop=True)     # reset row index values

    # Zamik x osi, da so vrednosti med 0 in 24h   
        if df_temp_g.shape[0] > 1:
            if (df_temp_g.iloc[-1, 0] - df_temp_g.iloc[0, 0]) <= 24 and df_temp_g.iloc[0, 0] < 0:
                df_temp_g.iloc[:, 0] = df_temp_g.iloc[:, 0].transform(lambda x: x-x.min())
            elif (df_temp_g.iloc[-1, 0] - df_temp_g.iloc[0, 0]) <= 24 and df_temp_g.iloc[-1, 0] > 24:
                df_temp_g.iloc[:, 0] = df_temp_g.iloc[:, 0].transform(lambda x: x-(x.max()-24))
            elif (df_temp_g.iloc[-1, 0] - df_temp_g.iloc[0, 0]) > 24:
                df_temp_g.iloc[:, 0] = df_temp_g.iloc[:, 0].transform(lambda x: x-x.min())
                df_temp_g.iloc[:, 0] = df_temp_g.iloc[:, 0].transform(lambda x: x*24/df_temp_g.iloc[-1, 0])
        
        df_temp_g.iloc[:, 0] = df_temp_g.iloc[:, 0].transform(lambda x: x+0.001)  # shift x values to 0+

        # Zamik v desno druge x vrednosti pri enakih x
        z=0
        while z < df_temp_g.shape[0]-1:
            if df_temp_g.iloc[z, 0] == df_temp_g.iloc[z+1, 0]:
                df_temp_g.iloc[z+1, 0] = df_temp_g.iloc[z+1, 0] + 0.001
                z +=1
            else:
                z +=1
        
        df_temp_g = df_temp_g * 1000
        df_temp_g = np.trunc(df_temp_g)   # cut off decimals
        df_temp_g = df_temp_g.apply(pd.to_numeric, downcast="integer")    # convert values to integer

        
        # popravljanje prekrivanja krivulj pri praznjenju pluviografa (correct overlap at the jumps)
        df_temp_g.columns = ['x', 'y']  # rename columns
        k = 0
        while k < df_temp_g.shape[0]-1:
            if (df_temp_g.loc[k,'y'] - df_temp_g.loc[k+1,'y']) > skok_razpon:   #zazna, da se posoda sprazne
                cas_z = df_temp_g.loc[k,'x']            # zadnja casovna tocka pred praznjenjem
                if cas_z + (cas_interval/60*1000) <= df_temp_g.iloc[-1,0]:
                    cas_k = cas_z + (cas_interval/60*1000)      # konec casovnega okna, ki ga gledamo; casovni interval 15 min (15/60*1000)
                else:
                    cas_k = df_temp_g.iloc[-1,0]               # konec casovnega okna sovpada s koncem meritev, v primeru, da je prelivanje konec dneva                
                l = k                                 # k - index na zacetku casovnega okna, l - index na koncu casovnega okna
                s = k                                 # s - index, ki tece znotraj 15 min casovnega okna
                if df_temp_g.loc[l,'x'] < cas_k:        # zanka postavi index l na konec casovnega okna
                    while df_temp_g.loc[l,'x'] < cas_k:
                        l += 1
                else:
                    l=k+1
                while s < l-1:
                    if (df_temp_g.loc[s,'y'] - df_temp_g.loc[s+1,'y']) < -skok_razpon:   # zazna, ce pride do prekrivanja zgornjega in spodnjega dela krivulje znotraj casovnega okna
                        #print(os.path.splitext(file_num)[0][0:3], dict_table.loc[m,'Datum'].strftime('%y%m%d'),'Popravljeno prekrivanje tock.', 'Cas:', cas_z, ',', 'St. tock:', l-k+1)
                        up = []                    # tocke znotraj intervala razdelimo na zgornjo (up) in spodnjo vejo (lo)
                        lo = []
                        for val in df_temp_g.loc[k:l, 'y']:
                            if val >= df_temp_g.loc[k,'y']:         # meja za razporeditev tock v zgornjo ali spodnjo vejo postavljena na y prve tocke na zgornji veji pri prekrivanju
                                up.append(val)
                                #up.sort() 
                            else:
                                lo.append(val)
                                #lo.sort()
                        jump = up + lo        # lista tock z up + lo vejama
                        q = k                 # index, ki tece po 15 min intervalu, po tockah, ki jih je potrebno zamenjati  
                        p = 0                 # index, ki tece po jump listi tock
                        while q <= l:
                            df_temp_g.at[q,'y'] = jump[p]  # zamenja tocke v tabeli z urejenimi
                            q += 1
                            p += 1
                        s = l
                    else:
                        s += 1
                k = l
            else:
                k += 1
        
    # Odpravljanje suma
        u = 0
        while u < df_temp_g.shape[0]-1:
            if ((df_temp_g.loc[u,'y'] - df_temp_g.loc[u+1,'y']) > 0) and ((df_temp_g.loc[u,'y'] - df_temp_g.loc[u+1,'y']) <= 200):   #zazna sum do 0.2 mm (naslednja tocka je nizja od prejsnje)
                df_temp_g.loc[u+1,'y'] = df_temp_g.loc[u,'y']            # nizjo tocko premaknemo gor, na vrednost predhodne tocke
                u += 1
            else:
                u += 1

        return df_temp_g    
    
    
    


# data points for one day in a specified output format - dodatno obdelano po funkciji df_graf_
    def df_meritve(col, cas_interval):
        df_temp = df_graf_(col, cas_interval)  # display first and second columns (X and Y) as df_temp

    # Opozorilo za dodatno tocko izven krivulje     
        h = 0
        while h < df_temp.shape[0]-2:
            if (abs(df_temp.loc[h,'y'] - df_temp.loc[h+1,'y']) >= razpon_tocka) and (abs(df_temp.loc[h+1,'y'] - df_temp.loc[h+2,'y']) >= razpon_tocka) and cas_interval != 0:   #zazna tocko >= 3 mm izven krivulje
                print(os.path.splitext(file_num)[0][0:3], dict_table.loc[m,'Datum'].strftime('%d.%m.%Y'), 'Tocka', (df_temp.loc[h+1,'x'], df_temp.loc[h+1,'y']), 'izven krivulje.')
                df_graf = df_graf_(dict_table.loc[m,'Indeks'],dict_table.loc[m,'Time_interval'])
                df_graf.plot(x='x',y='y', linestyle='-', marker='o')
                plt.gcf().suptitle(os.path.splitext(file_num)[0][0:3]+' '+dict_table.loc[m,'Datum'].strftime('%d.%m.%Y')+' '+'Tocka izven krivulje.', fontsize=18, fontweight='bold', y=0.92)
                plt.gcf().text(0.95, 0.01, '1.) Preveri potencialno sumljive skoke. \n 2.) Preveri potencialno prekrivanje tock (premik casa nazaj).', verticalalignment='bottom', horizontalalignment='right',color='green', fontsize=15)
                plt.gcf().set_size_inches((15, 10))
                pp.savefig(plt.gcf())
                h += 1
            else:
                h += 1

        df_temp.iloc[:, 1] = df_temp.iloc[:, 1].transform(lambda x: 20000-x)  # convert y values to descending
        df_temp = df_temp.applymap(str)    # convert values back to string for zero padding
        df_temp = df_temp.applymap(lambda x: x.zfill(5))   # zero padd both columns
        df_temp.insert(0, "code", '02', allow_duplicates=True)   # insert an id column (alters column indexes!!)
        df_temp.columns = ['code', 'x', 'y']  # rename columns
        return df_temp    


    # creating the final dataset in the specified output format for a measuring station for one month
    n = 0
    m = 0
    df_inter = []
    while n < len(date_month_list_filtered):
        if pd.to_datetime(date_month_list_filtered[n]) in dict_table['Datum'].tolist():
            if dict_table.loc[m,'Padavina'] == 'sneg':
                re = pd.concat([df_head(n), df_snow, df_end], ignore_index=True)
                df_inter.append(re)
                n += 1
                m += 1
            elif dict_table.loc[m,'Padavina'] == 'manjka':
                re = pd.concat([df_head(n), df_missing, df_end], ignore_index=True)
                df_inter.append(re)
                n += 1
                m += 1
            elif dict_table.loc[m,'Padavina'] == 'dez':
                re = pd.concat([df_head(n), df_coord, df_meritve(dict_table.loc[m,'Indeks'], dict_table.loc[m,'Time_interval']), df_end], ignore_index=True)
                df_inter.append(re)
                #print(os.path.splitext(file_num)[0][0:3], dict_table.loc[m,'Datum'].strftime('%y%m%d'))
                n += 1
                m += 1
        else:  # for a dry day
            re = pd.concat([df_head(n), df_dry, df_end], ignore_index=True)
            df_inter.append(re)
            n += 1  
    df_final = pd.concat(df_inter, ignore_index=True)   

    
    # creating new directory for the relevant month
    folder_name = 'Output_files' + date_month_list_filtered[0].strftime('%y%m')
    os.makedirs(folder_name, exist_ok=True)  
    
    # writing and saving the file and adding file extension with repetition (version) number
    f_num = 1   # number of the file extension
    file_name = 'o' + os.path.splitext(file_num)[0][0:3] + date_month_list_filtered[0].strftime('%y%m') + '.' + str(f_num).zfill(3)
    while (os.path.exists(os.path.abspath(os.path.join(folder_name, file_name)))):
        f_num+=1
        file_name = 'o' + os.path.splitext(file_num)[0][0:3] + date_month_list_filtered[0].strftime('%y%m') + '.' + str(f_num).zfill(3)

    df_final.to_csv(os.path.join(folder_name, file_name), sep=' ', index=False, header=False)
    
    
    verboseprint('Narejena datoteka:', file_name)


pp.close()         
print(os.path.abspath(plot_name))
#print('file://wsl%24/Ubuntu-20.04'+os.path.abspath(plot_name))

#webbrowser.open('file://wsl%24/Ubuntu-20.04'+os.path.abspath(plot_name), new=2)

naslov_wsl = os.popen('wslpath -m '+os.path.abspath(plot_name))
naslov_win = naslov_wsl.read()
naslov_win = 'file:'+naslov_win.rstrip()
verboseprint(naslov_win)
webbrowser.open(naslov_win, new=2)