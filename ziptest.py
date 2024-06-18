import shutil
import os
import zipfile

if __name__ == "__main__":  
    comcode = '0000001'
    dir_filepath = r'C:\Users\user\OneDrive\Workplace\emoney'
    dir_date = str(comcode) + '_'+ '202461'+'_'+'2024610'
    zip_name = str(comcode) + '_'+ '202461'+'_'+'2024610'+'.zip'

    #dir_out_filepath = os.path.join(dir_filepath, comcode, dir_date) 
    #dir_basepath = os.path.join(comcode, dir_date) 
    zipfile_name = os.path.join(dir_filepath, comcode, zip_name) 

    dir_files_file = os.path.join(dir_filepath, comcode, dir_date) 

    files_file = [
    f for f in os.listdir(dir_files_file) if os.path.isfile(os.path.join(dir_files_file, f))
    ]  

    files_no = len(files_file)

    with zipfile.ZipFile(zipfile_name, 'w',
                     compression=zipfile.ZIP_DEFLATED,
                     compresslevel=6) as zf:
        for i in range(0,files_no):
            add_file = os.path.join(dir_filepath, comcode, dir_date, str(files_file[i])) 
            zf.write(add_file, arcname=str(files_file[i]))
    