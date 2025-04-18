import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import os
#import cv2

def read_text_file(file_name=None,seperator=None):
    filename=pd.read_csv(os.getcwd()+file_name,sep=seperator)
    #filename=pd.read("Z:/1 BIS/Shared folders/Nikita/Marta/SCREEN/analysis/chip10/DataAnalysis/imageWithFIdx.csv",sep=separator)
    return filename

def set_working_directory(location_screen):
    old_directory=os.getcwd()
    os.chdir(location_screen)
    # Check if folder contains the chip folder structure
    subfolders=os.listdir()
    if '02_CroppedImages' in subfolders:
        print('Path to folder is set')
    else:
        print('Please check if path is correct')
        os.chdir(old_directory)

def retrieve_name_images_selected_features(selected_features=None,data_images=None,image_column=None):
    image_file_names=data_images.loc[data_images['FeatureIdx'].isin(selected_features),:]
    image_file_names=data_images.loc[:,['FeatureIdx','Metadata_Quadrant','Metadata_Duplicate',image_column]]
    return image_file_names

def plot_the_images(image_data=None,features_to_plot=None,image_type=None,image_mode='png',visualizing=None,folder_to_select=None,number_of_rows=2,number_of_columns=10,save_figure='No'):
    chip_folders=os.listdir(os.getcwd()+folder_to_select)
    for feat in features_to_plot:
        image_data_feature=image_data.loc[image_data['FeatureIdx']==int(feat),:]
        figure,ax = plt.subplots(nrows=number_of_rows,ncols=number_of_columns,figsize=(25,7.5)) 
        images_top=image_data_feature.loc[image_data_feature['Metadata_Duplicate']==0,:]
        images_bottom=image_data_feature.loc[image_data_feature['Metadata_Duplicate']==1,:]
        indexTop=0
        indexBottom=10
        for chip in chip_folders:
            image_top_to_plot=images_top[image_type]
            image_top_to_plot=image_top_to_plot[image_top_to_plot.str.contains(chip)]
            image_top_to_plot=image_top_to_plot.astype(str)
            tmp_folder=os.getcwd()+folder_to_select+chip+'/'
            image_location_top=tmp_folder+image_top_to_plot
            if image_mode=='png':
                imgTop=mpimg.imread(image_location_top.item())
            if image_mode=='tif':
                # plot the TIF image with PIL
                imgTop=cv2.imread(image_location_top.item())
                imgTop = cv2.cvtColor(imgTop, cv2.COLOR_BGR2RGB)
            ax.ravel()[indexTop].imshow(imgTop,aspect='auto')
            ax.ravel()[indexTop].set_title(chip)
            ax.ravel()[indexTop].set_axis_off()
            
            image_bottom_to_plot=images_bottom[image_type]
            image_bottom_to_plot=image_bottom_to_plot[image_bottom_to_plot.str.contains(chip)]
            image_bottom_to_plot=image_bottom_to_plot.astype(str)
            tmp_folder=os.getcwd()+folder_to_select+chip+'/'
            image_location_bottom=tmp_folder+image_bottom_to_plot
            if image_mode=='png':
                imgBottom=mpimg.imread(image_location_bottom.item())

            if image_mode=='tif':
                # plot the tif image with PIL
                imgBottom=cv2.imread(image_location_bottom.item())
                imgBottom = cv2.cvtColor(imgBottom, cv2.COLOR_BGR2RGB)
            ax.ravel()[indexBottom].imshow(imgBottom,aspect='auto')
            ax.ravel()[indexBottom].set_title(chip)
            ax.ravel()[indexBottom].set_axis_off()
            
            figure.suptitle(feat,fontsize=24)
            indexTop=indexTop+1
            indexBottom=indexBottom+1

        # save the subplot per feature
        if save_figure=='Yes':
            file_name_to_save=os.getcwd()+"/04_DataAnalysis/"+visualizing+"_"+"Feature_"+feat+".png"
            figure.savefig(file_name_to_save)
            

def plot_feature_distribution(image_data=None,feature_of_interest=None,features_to_plot=None):
    # boxplots cannot handle a long list of features
    image_data_of_interest=image_data.loc[:,['FeatureIdx','Metadata_Chip',feature_of_interest]]
    if features_to_plot.__len__() < 8:
        features_to_plot=features_to_plot.append('2177')
        image_data_to_plot=image_data_of_interest.loc[image_data_of_interest['FeatureIdx'].isin(features_to_plot),:]
        plt.figure()
        ax = sns.boxplot(x="FeatureIdx", y=feature_of_interest, data=image_data_to_plot,color='white')
        ax = sns.stripplot(x="FeatureIdx", y=feature_of_interest, data=image_data_to_plot, hue='Metadata_Chip',size=4)
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,title='Chip Number')
    else:
        plotFeatures=True
        x_init=0
        x_end=8
        while plotFeatures:
            if x_end < features_to_plot.__len__():
                features_subselected=features_to_plot[x_init:x_end]
                features_subselected.append('2177')
                image_data_to_plot=image_data_of_interest.loc[image_data_of_interest['FeatureIdx'].isin(features_subselected),:]
                plt.figure()
                ax = sns.boxplot(x="FeatureIdx", y=feature_of_interest, data=image_data_to_plot,color='white')
                ax = sns.stripplot(x="FeatureIdx", y=feature_of_interest, data=image_data_to_plot, hue='Metadata_Chip',size=4)
                plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,title='Chip Number')
            else:
                x_end=features_to_plot.__len__()
                features_subselected=features_to_plot[x_init:x_end]
                features_subselected.append('2177')
                image_data_to_plot=image_data_of_interest.loc[image_data_of_interest['FeatureIdx'].isin(features_subselected),:]
                plt.figure()
                ax = sns.boxplot(x="FeatureIdx", y=feature_of_interest, data=image_data_to_plot,color='white')
                ax = sns.stripplot(x="FeatureIdx", y=feature_of_interest, data=image_data_to_plot, hue='Metadata_Chip',size=4)
                plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,title='Chip Number')
                plotFeatures=False
            x_init=x_end
            x_end=x_init+8