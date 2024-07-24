import pyxdf
import pandas as pd
import PySimpleGUI as sg
import numpy as np
layout2 = [[sg.Text('без папки и имени файла не сохранит')],
            [sg.FileBrowse("загрузить XDF")],
            [sg.Text('выберите папку', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
            [sg.Text('введите имя файла', size=(15, 1)), sg.InputText()],
            [sg.Submit(), sg.Cancel()]]

window2 = sg.Window('Rename Files or Folders', layout2)
event2, values2 = window2.read()
window2.close()


def izvlechenie_data(data, structur):
    channel_data_DATA = data[structur]["time_series"] # 1 массив данных
    channel_label_DATA = []
    for channel in range(len(data[structur]['info']["desc"][0]["channels"][0]['channel'])): # 2 имена каналов 
        channel_label_DATA.append(data[structur]['info']["desc"][0]["channels"][0]['channel'][channel]['label'][0])

    data_DATA = pd.DataFrame()
    if len(channel_label_DATA)>1:
        for channels in range(len(channel_label_DATA)):
            data_DATA[channel_label_DATA[channels]] = channel_data_DATA[:,channels].reshape(-1)
    else:
        data_DATA[data[structur]['info']['name'][0]] = channel_data_DATA.reshape(-1)

    return data_DATA

file_xdf, folder_path_metki, file_path_metki = values2['загрузить XDF'], values2[0], values2[1]       # get the data from the values dictionary
file = file_xdf
data, header = pyxdf.load_xdf(file)
metki = "_metki.csv"
eeg = "_eeg.csv"
ecg = "_ecg.csv"
bioz = "_bioz.csv"

for structur in range(len(data)):
    if data[structur]['info']['name'][0]=="task":
        try:
            metki_xdf = pd.DataFrame()
            metki_xdf["time_stamps"] = np.intc(data[structur]['time_stamps']-data[structur]['time_stamps'][0])
            metki_xdf["time_series"] = data[structur]['time_series']
        except:
            print(data[structur]['info']['name'][0], "Меток нет")


    if data[structur]['info']['name'][0]=="EEG":
        data_EEG = izvlechenie_data(data, structur)

    if data[structur]['info']['name'][0]=="zadasac":
        data_EEG = izvlechenie_data(data, structur)
    
    if data[structur]['info']['name'][0]=="NBEEG16_Data":
        data_EEG = izvlechenie_data(data, structur)

    if data[structur]['info']['name'][0]=="ECG":
        data_ECG = izvlechenie_data(data, structur)
     
    if data[structur]['info']['name'][0]=="BIOZ":
        data_BIOZ = izvlechenie_data(data, structur)

if folder_path_metki is None or file_path_metki is None:
    print("нет имени файла и папки")
elif folder_path_metki=='':
    print("нет имени папки")
elif file_path_metki =='':
    print("нет имени файла")
else:
    pass

metki_xdf.to_csv(folder_path_metki+'/'+file_path_metki+metki, sep=",", index=False) 
data_EEG.to_csv(folder_path_metki+'/'+file_path_metki+eeg, sep=",", index=False)
data_ECG.to_csv(folder_path_metki+'/'+file_path_metki+ecg, sep=",", index=False)
data_BIOZ.to_csv(folder_path_metki+'/'+file_path_metki+bioz, sep=",", index=False)
