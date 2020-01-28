# Bruno Alves
# Claudia Coelho

from Tkinter import *
import tkFileDialog
import tkMessageBox
import dicom
import matplotlib.pyplot as plt
import os

def generate_dvh(RD_Path_file, RS_Path_file):
    #ROINames to not be considered
    EXCLUDE_ROIName = {"TARGET", "HT", "SHELL", "BODY"}
    
    #2. Read the files found
    plan = dicom.read_file(RD_Path_file)
    plan2 = dicom.read_file(RS_Path_file)

    RD_DVH = []
    RD_ROINumber = []
    DVH_size = len(plan[0x3004, 0x50].value)

    for i in range(DVH_size):
        RD_DVH.append(plan[0x3004, 0x50].value[i][0x3004,0x58].value)
        RD_ROINumber.append(str(plan[0x3004, 0x50].value[i][0x3004, 0x60][0][0x3006, 0x84])[54:-1])

    RD_DVH_even = []
    for i in range(DVH_size):
        RD_DVH_even.append(RD_DVH[i][1::2])

    RS_ROINumber = []
    RS_ROIName = []
    RS_ROINumber_size = len(plan2[0x3006, 0x20].value)

    for i in range(RS_ROINumber_size):
        RS_ROINumber.append(plan2[0x3006, 0x20].value[i][0x3006,0x22].value)
        RS_ROIName.append(plan2[0x3006, 0x20].value[i][0x3006,0x26].value)

    RD_ROIName = []
    for i in range(len(RD_ROINumber)):
        for j in range(len(RS_ROINumber)):
            if(str(RD_ROINumber[i]) == str(RS_ROINumber[j])):
                RD_ROIName.append(RS_ROIName[j])

    RD_DVH_ToShow = []
    RD_ROIName_ToShow = []
    for i in range(len(RD_ROINumber)):
        if (str(RD_ROIName[i]) not in EXCLUDE_ROIName):
            RD_DVH_ToShow.append(RD_DVH_even[i])
            RD_ROIName_ToShow.append(RD_ROIName[i])

    maximos = []
    for i in range(len(RD_DVH_ToShow)):
        maximos.append(max(RD_DVH_ToShow[i]))

    maximo = max(maximos)

    plt.clf()
    for j in range(len(RD_DVH_ToShow)):
        x_axis = []
        for i in range(len(RD_DVH_ToShow[j])):
            x_axis.append(i*0.01)

        RD_DVH_ToShow[j] = [(e*100)/maximo for e in RD_DVH_ToShow[j]]
        if(RD_DVH_ToShow[j] > 0 and len(RD_DVH_ToShow[j]) > 1): #excludes empty arrays
            plt.plot(x_axis,RD_DVH_ToShow[j], alpha = 0.5, label = RD_ROIName_ToShow[j])


    plt.legend(loc='upper right')
    plt.xlabel('Dose (Gy)')
    plt.ylabel('Volume (%)')
    plt.show()

def selectFolder():
    PathDicom = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    lstFilesNames = []
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                lstFilesNames.append(str(filename))

    RD_Path = []
    RS_Path = []
    for file in lstFilesNames:
        initials = file[:2]
        if (initials == "RD"):
            RD_Path.append(file)
        elif (initials == "RS"):
            RS_Path.append(file)

    if (len(RD_Path) != 1 and len(RS_Path) != 1):
        tkMessageBox.showerror("Error", "A problem ocurred when looking for RT-Dose and RT-Struct files")  
    elif (len(RD_Path) != 1):
        tkMessageBox.showerror("Error", "A problem ocurred when looking for RT-Dose file")  
    elif (len(RS_Path) != 1):
        tkMessageBox.showerror("Error", "A problem ocurred when looking for RT-Struct file") 
    else:
        RD_Path_file = PathDicom+"/"+RD_Path[0]
        RS_Path_file = PathDicom+"/"+RS_Path[0]
        generate_dvh(RD_Path_file, RS_Path_file)

#Simple GUI
root = Tk()
root.title("DICOM DVH Generator")
root.geometry("300x300")
b1=Button(root, text="Select Patient Folder",height=10,width=15,command=selectFolder)
b1.place(relx=0.5, rely=0.5, anchor=CENTER)
root.mainloop()

