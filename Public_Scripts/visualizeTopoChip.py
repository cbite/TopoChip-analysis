##############################################################################################################
#################   Python script with the functions to visualize TopoChip images     ########################
#################   Author: A.S. Vasilevich   , T.J.M Kuijpers                        ########################
##############################################################################################################

import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import PIL
import os

def showOnTopoChip(ScreenData, displayFeature, zoom=[[1,66],[1,66]]):

    ScreenData=ScreenData.loc[ScreenData["Metadata_row"].between(zoom[0][0], zoom[0][1])]#apply zoom for rows
    ScreenData=ScreenData.loc[ScreenData["Metadata_col"].between(zoom[1][0], zoom[1][1])]#apply zoom for columns
    #find median
    
    medianScreenData=ScreenData.groupby(["Metadata_row","Metadata_col"])[[displayFeature]].median()
    pivMedian = pd.pivot_table(medianScreenData, 
        values=displayFeature,index=["Metadata_row"], columns=["Metadata_col"], dropna = False)
    
    #find mean
        
    meanScreenData=ScreenData.groupby(["Metadata_row","Metadata_col"])[[displayFeature]].mean()
    pivMean = pd.pivot_table(meanScreenData, 
        values=displayFeature,index=["Metadata_row"], columns=["Metadata_col"], dropna = False)
    
    #find sd
        
    sdScreenData=ScreenData.groupby(["Metadata_row","Metadata_col"])[[displayFeature]].std()
    pivSd = pd.pivot_table(sdScreenData, 
        values=displayFeature,index=["Metadata_row"], columns=["Metadata_col"], dropna = False)
    
    nrows_f=math.ceil((ScreenData.Metadata_Chip.nunique()+3)/3)
    fig, axes = plt.subplots(ncols=3, 
        nrows=nrows_f,sharex=True, sharey=True)
    
    fig.subplots_adjust(hspace=0.1)
       
    fig.set_figwidth(20)
    fig.set_figheight(6*nrows_f)
    cbar_ax = fig.add_axes([.96, .3, .03, .4])
    cbar_ax.set(title="Distribution of \n %s \n on TopoChips"%(displayFeature))

    for ax, chip in zip(axes.flatten(), np.append(np.sort(ScreenData.Metadata_Chip.unique()),["Mean","Sd","Median"])):
        i=0
        if (chip=="Median"):
            sns.heatmap(pivMedian,
                    ax=ax, 
                    square=True,
                    cmap="tab20b",
                    vmin=min(ScreenData[displayFeature]),
                    vmax=max(ScreenData[displayFeature]),
                    #vmin=np.quantile(ScreenData[displayFeature],0.01), 
                    #vmax=np.quantile(ScreenData[displayFeature],0.99),
                   cbar_ax=None if i else cbar_ax)#'gist_ncar'
        
            ax.set(title="TopoChip %s"%(chip))
            
        elif (chip=="Mean"):
            sns.heatmap(pivMean,
                    ax=ax, 
                    square=True,
                    cmap="tab20b", 
                    vmin=min(ScreenData[displayFeature]),
                    vmax=max(ScreenData[displayFeature]),
                    #vmin=np.quantile(ScreenData[displayFeature],0.01), 
                    #vmax=np.quantile(ScreenData[displayFeature],0.99),
                   cbar_ax=None if i else cbar_ax)#'gist_ncar'
        
            ax.set(title="TopoChip %s"%(chip))
            
        elif (chip=="Sd"):
            sns.heatmap(pivSd,
                    ax=ax, 
                    square=True,
                    cmap="tab20b", 
                    vmin=min(ScreenData[displayFeature]),
                    vmax=max(ScreenData[displayFeature]),
                    #vmin=np.quantile(ScreenData[displayFeature],0.01), 
                    #vmax=np.quantile(ScreenData[displayFeature],0.99),
                   cbar_ax=None if i else cbar_ax)#'gist_ncar'
        
            ax.set(title="TopoChip %s"%(chip))
        
        else:
            
            piv = pd.pivot_table(ScreenData.loc[ScreenData.Metadata_Chip==np.int(chip)], 
            values=displayFeature,index=["Metadata_row"], columns=["Metadata_col"], dropna = False)

            sns.heatmap(piv,
                        ax=ax, 
                        square=True,
                        cmap="tab20b", 
                        vmin=min(ScreenData[displayFeature]),
                        vmax=max(ScreenData[displayFeature]),
                        #vmin=np.quantile(ScreenData[displayFeature],0.01), 
                        #vmax=np.quantile(ScreenData[displayFeature],0.99),
                       cbar_ax=None if i else cbar_ax)#'gist_ncar'

            ax.set(title="TopoChip %s"%(chip))
        i+=1
        
    #fig.tight_layout(rect=[0, 0, .95, 1])
        
    #fig.show()
    
def showHistPerTopoChip(ScreenData, featureOfInterest):
    
    #find median
    
    medianScreenData=ScreenData.groupby(["Metadata_row","Metadata_col"])[[featureOfInterest]].median()
    #find mean
        
    meanScreenData=ScreenData.groupby(["Metadata_row","Metadata_col"])[[featureOfInterest]].mean()
    #find sd
        
    sdScreenData=ScreenData.groupby(["Metadata_row","Metadata_col"])[[featureOfInterest]].std()
       
    nrows_f=math.ceil((ScreenData.Metadata_Chip.nunique()+3)/3)
    
    fig, axes = plt.subplots(ncols=3, 
        nrows=nrows_f)
    
    fig.subplots_adjust(hspace=0.1)
       
    fig.set_figwidth(10)
    fig.set_figheight(3*nrows_f)
    
    for ax, chip in zip(axes.flatten(), np.append(ScreenData.Metadata_Chip.unique(),["Mean","Sd","Median"])):
        i=0
                    
        if (chip=="Median"):
            sns.histplot( medianScreenData[featureOfInterest], color="gold",ax=ax)
        
            ax.set(title="TopoChip %s"%(chip))
            
        elif (chip=="Mean"):
            sns.histplot( meanScreenData[featureOfInterest], color="gold",ax=ax)
        
            ax.set(title="TopoChip %s"%(chip))
            
        elif (chip=="Sd"):
            
            sns.histplot( sdScreenData[featureOfInterest], color="gold",ax=ax)
        
            ax.set(title="TopoChip %s"%(chip))
        
        else:        
            sns.histplot( ScreenData.loc[ScreenData.Metadata_Chip==np.int(chip)][featureOfInterest] ,
                         color="teal",ax=ax)
            
            ax.set(title="TopoChip %s"%(chip))
            
        i+=1
        
    fig.tight_layout(rect=[0, 0, 1, 1])
        
    #fig.show()    
    
def showImages(ScreenData, featureOfInterest, stainingFile, valuesRange, mode="raw",folderNameRaw=None,folderNameOverlay=None ):
    left=valuesRange[0]
    right=valuesRange[1]
    listOfFiles=ScreenData.loc[ScreenData[featureOfInterest].between(left, right)]
      
    if(len(listOfFiles.index)>100):
        rows=listOfFiles.sample(n=100).reset_index()
    else:
        rows=listOfFiles.reset_index()
    
    #FeatImg = PIL.Image.open('Surface_Images/Pattern_FeatureIdx_{}.bmp'.format(i)).convert("L")
    
   
    plt.figure(figsize=(20,80))
    
        
    
    for i, row in rows.iterrows():
        
        if(mode=="overlay"):
            
            folderName=folderNameOverlay            
                      
            fileName=row[stainingFile]#.replace(".tif","actinOverlay.png")
            
            #fileName="Row1_Col1_c1_actinOverlay.png"
            
            cmap="cividis"
            
        else:
            
            folderName=folderNameRaw
            fileName=row[stainingFile]
            
            #fileName="Row1_Col1_c1.tiff"
            
            cmap='gray'
        
        featureValue=row[featureOfInterest]
        chip=row["Metadata_Chip"]
        chipRow=row["Metadata_row"]
        chipCol=row["Metadata_col"]

        imageFolder=folderName%chip
        print('debug:', imageFolder, chip)
        print(fileName)
        print(imageFolder)

        try:
            s_image=PIL.Image.open(os.path.join(imageFolder, fileName))#.convert("L")
        except:
            s_image = PIL.Image.open(os.path.join(imageFolder, fileName+'f'))  # if its called tiff instead of tif
        
           
        plt.subplot(25,4,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(s_image,cmap=cmap)
        plt.xlabel("Chip-%d Row-%d Col-%d \n %s = %d"%(chip, chipRow, chipCol, featureOfInterest, featureValue))
        break

    
    plt.tight_layout()
    plt.show()