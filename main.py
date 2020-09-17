####################################################################
# Import
####################################################################
import os
import glob
import shutil

import helper_of_pdf
import writer_of_excel
####################################################################

# Prepare questions for extracting sentences from pdf files.
Q1 = 'Where is root directory including pdf files? (default : ./dataset/)'
Q1 += '\nex) ./dataset/\n=> '

Q2 = 'Where is result directory ? (default : ./results/)'
Q2 += '\nex) ./results/\n=>'

root_dir = input(Q1)
save_dir = input(Q2)

# If you don't answer question, I set up default arguments.
if root_dir == '': root_dir = './dataset/'
if save_dir == '': save_dir = './results/'

# If you already create directory, I remove directory and create new directory.
if os.path.isdir(save_dir):
    shutil.rmtree(save_dir)

os.makedirs(save_dir)

# Initialize Helper and Writer
# * Helper : Extract patterns and scripts from single pdf file.
# * Writer : Save patterns and scripts as single excel file.
helper = helper_of_pdf.Helper()
writer = writer_of_excel.Writer()

# Get folder name from os.listdir function. At this moment, folder name is similar to person name.
for name in os.listdir(root_dir):

    # each dictionary will get extraced sentences per pdf. 
    # At this moment, data type of extracted sentences is tuple. each of extraced sentences composes english and korean sentences.
    scripts_dic = {}
    patterns_dic = {}

    error_pdf_files = []

    writer.initialize()

    # ex)
    pdf_dir = root_dir + name + '/'
    log_path = save_dir + name + '.txt'
    excel_path = save_dir + name + '.xlsx'

    # Get pdf paths from glob.glob function. 
    for pdf_path in sorted(glob.glob(pdf_dir + '*.pdf')):

        # Get pdf name after parsing pdf path.
        # ex)
        pdf_name = os.path.basename(pdf_path).replace('.pdf', '')

        # Extract sentences from pdf file.
        patterns, scripts = helper.extract(pdf_path)

        # If pdf file dosen't have matched sentences, this case is error. So, the code appends pdf name.
        if len(scripts) == 0:
            error_pdf_files.append(pdf_name)
            continue
        
        # Update extracted patterns and scripts
        patterns_dic[pdf_name] = patterns
        scripts_dic[pdf_name] = scripts
    
    # If helper successfully extracts sentences from pdf files, the code saves patterns dic and scripts dic.
    if len(scripts_dic.keys()) > 0:
        writer.append(patterns_dic, scripts_dic)
        writer.save(excel_path)

    # 
    if len(error_pdf_files) > 0:
        with open(log_path, 'w') as f:
            for pdf_name in error_pdf_files:
                f.write(pdf_name + '\n')

