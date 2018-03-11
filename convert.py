# -*- coding: utf-8 -*-
from pdf2txt import pdf2txt
from os import listdir
from os.path import isfile, join
from pdf2txt import pdf2txt

path = "./pdfs"
onlyfiles = [path+"/"+f.split(".")[0] for f in listdir(path) if isfile(join(path, f)) and f.endswith(".pdf")]
# print(onlyfiles[31:])
for f in onlyfiles:
    try:
        print("filename", f)
        output_fname = f+".txt"
        input_fname = f+".pdf"
        pdf2txt(input_fname,  output_fname)

    except EOFError:
        print('Why did you do an EOF on me?')

    except KeyboardInterrupt:
        print('You cancelled the operation.')
    except Exception as e:
        print(e)
        print('An error occurred.')
# clean_pdf("test")
