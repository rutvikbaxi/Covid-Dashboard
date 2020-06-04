import os
with open(os.path.join('E:/analysis datasets/covid 19 india/multiple_func','Procfile'), "w") as file1:
    toFile = 'web: sh setup.sh && streamlit run main_app.py'
    file1.write(toFile)