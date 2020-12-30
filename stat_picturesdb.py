import pandas as pd
import os

# main_folder = os.listdir()
# list_slides = []
# list_types = []
# for folder in main_folder:
#     if folder.find("TCGA") != -1 and folder.find("TCGA-AO") == -1:
#         current_type = folder
#         print(folder)
#         print(os.getcwd())
#         sub_folder = os.listdir(os.path.join(os.getcwd(), folder))
#         for sf in sub_folder:
#             if sf.find("Slides") != -1:
#                 files = os.listdir(os.path.join(os.getcwd(), folder, sf ))
#                 for f in files:
#                     if f.find("TCGA-") != -1:
#                         list_slides.append(f)
#                         list_types.append(current_type)
# df_slides_report = pd.DataFrame()
# df_slides_report["SlideName"] = list_slides
# df_slides_report["CancerType"] = list_types
# df_slides_report.to_csv("SlidesReport.csv", sep="\t", header=True, index=False)


list_slides = []
list_types = []
main_folder_path = "/data/gcs/tcgadata/files/DiagnosisSlides/DataExtraction_DataManagement"
main_folder_list = os.listdir(main_folder_path)
for subfolder in main_folder_list:
    if subfolder.find("TCGA") != -1:
        print(main_folder_path, subfolder)
        subfolder_slides_path = os.path(main_folder_path, subfolder, subfolder, "harmonized/Biospecimen/Slide_Image")
        current_type = subfolder
        subfolder_slides_list = os.listdir(subfolder_slides_path)
        for folder in subfolder_slides_list:
            slides_folder = os.listdir(subfolder_slides_path, folder)
            for f in slides_folder:
                list_slides.append(f)
                list_types.append(current_type)
df_slides_report = pd.DataFrame()
df_slides_report["SlideName"] = list_slides
df_slides_report["CancerType"] = list_types
df_slides_report.to_csv("/data/gcs/tcgadata/files/DiagnosisSlides/DataExtraction_DataManagement/SlidesReport.csv", sep="\t", header=True, index=False)


