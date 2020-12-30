import os
main_folder = os.listdir('/data/gcs/lungNENomics/work/TestSetImgCarcinoids')
list_empty_folder = []
for f in main_folder:
	if len(os.listdir(os.path.join( '/data/gcs/lungNENomics/work/TestSetImgCarcinoids' ,f))) == 0:
		list_empty_folder.append(f)

with open('empty_files_list.txt','w') as f:
	for ele in list_empty_folder:
		f.write('%s \n' %ele)
