#the function that estimates Metadata_Row and Metadata_Col, if they are absent from the column "Metadata_Well"
# it also print out statements to help understand what function actually did after exectuting

import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def createRowCol(Imagedata):
    Imagedata=Imagedata[Imagedata["Metadata_Well"].notna()]#remove files that does not have coordinates data
    if "Metadata_Well" in Imagedata.columns: 
        print("Metadata_Well exists")
        if (not "Metadata_row" in Imagedata.columns)|(not "Metadata_col" in Imagedata.columns):
            Imagedata["Metadata_row"]=Imagedata.Metadata_Well.astype(int).astype(str).str.slice(stop=-2).astype(int)
            #print(Imagedata.shape)
            Imagedata["Metadata_col"]=Imagedata.Metadata_Well.astype(int).astype(str).str.slice(start=-2).astype(int)
            print("Metadata_row created")
            print("Metadata_col created")           
        else:
            print("Metadata_row exists")
            print("Metadata_col exists")
    elif "Metadata_col" in Imagedata.columns:
        print("Metadata_col exists")
    elif "Metadata_row" in Imagedata.columns:
        print("Metadata_row exists")        
    else:
        print("Metadata_Well does not exists") 
        print("nothing was changed")
    return Imagedata

#Defining a function that performs the merge
def mergeByRowCol(topochipMap, Imagedata):
    #first flatten FeatureIdx map to 1 column
    data = {'FeatureIdx': topochipMap.to_numpy().ravel('F'),
            'Metadata_col': np.asarray(topochipMap.columns+1).repeat(66),
            'Metadata_row': np.tile(np.asarray(topochipMap.index+1), 66)}#add 1 as index start from 0
    topochipMapFlat=pd.DataFrame(data, columns=['FeatureIdx', 'Metadata_row', 'Metadata_col'])
    topochipMapFlat["Metadata_Quadrant"]="B"#add quadrant A and B to metadata
    topochipMapFlat.loc[(topochipMapFlat.FeatureIdx<1088)|(topochipMapFlat.FeatureIdx==2177),"Metadata_Quadrant"]="A"
    
    topochipMapFlat["Metadata_Duplicate"]=topochipMapFlat.duplicated("FeatureIdx").astype(int)
    
    rawImagedataWithFeatureIdx=pd.merge(left=Imagedata, right=topochipMapFlat,
                      how='left', left_on=["Metadata_row", "Metadata_col"], 
                      right_on=["Metadata_row", "Metadata_col"])
    return rawImagedataWithFeatureIdx

#Define a fucntion that rotates TopoMap
def rotTopoMap(topochipMap, rotation_coefficient):
    topochipMap_rot=pd.DataFrame(np.rot90(topochipMap, k=rotation_coefficient, axes=(0, 1)))
    return topochipMap_rot

#Function to compare the location of FeatureIdx on the original, rotated and replicas of the chip
def vizFeatureIdxOnChip(originalMap, rotatedMap, screenData, cmap="tab20b"):
    
    nrows_f=math.ceil((screenData.Metadata_Chip.nunique()+2)/3)
    
    fig, axes = plt.subplots(ncols=3, 
        nrows=nrows_f,sharex=True, sharey=True)

    fig.subplots_adjust(hspace=0.1)

    fig.set_figwidth(20)
    fig.set_figheight(6*nrows_f)
    cbar_ax = fig.add_axes([.96, .3, .03, .4])
    cbar_ax.set(title="FeatureIdx number")

    for ax, chip in zip(axes.flatten(), np.append(screenData.Metadata_Chip.unique(),["Original","Rotated"])):
        i=0
        if (chip=="Original"):
            sns.heatmap(originalMap,
                    ax=ax, 
                    square=True,
                    cmap=cmap,
                    vmin=1,
                    vmax=2177,
                    cbar_ax=None if i else cbar_ax)#'gist_ncar'
        
            ax.set(title="%s"%(chip))
            
        elif (chip=="Rotated"):
            if(rotatedMap.empty):
                print('no rotation')
            else:
                sns.heatmap(rotatedMap,
                        ax=ax, 
                        square=True,
                        cmap=cmap, 
                        vmin=1,
                        vmax=2177,
                        cbar_ax=None if i else cbar_ax)#'gist_ncar'

                ax.set(title="%s"%(chip))

        else:
            piv = pd.pivot_table(screenData.loc[screenData.Metadata_Chip==np.int(chip)], 
                values="FeatureIdx",index=["Metadata_row"], columns=["Metadata_col"], 
                                 dropna = False)

            #plot pivot table as heatmap using seaborn
            sns.heatmap(piv, 
                    ax=ax, 
                    square=True,
                    cmap=cmap, 
                    vmin=1,
                    vmax=2177,
                    cbar_ax=None if i else cbar_ax)
            ax.set(title="TopoChip %s"%(chip))
        i+=1
    
    plt.show()
    
def getFilenames(Imagedata, FeatureIdx, filePathColumn):
    for f in np.unique((Imagedata.loc[Imagedata.FeatureIdx==FeatureIdx,
        [filePathColumn]])):
        print (f)