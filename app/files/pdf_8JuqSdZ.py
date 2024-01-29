import os
import PyPDF2
import re 

def split_bill_pdf(fname,pattern,parse_method=1,pdf_name_apply = lambda x : x,filter_file=None):
    with open(fname, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        total_pages = pdf_reader.numPages     
        curr_page = 0   

        for page_num in range(total_pages):
            page = pdf_reader.getPage(page_num)            
            page_text = page.extractText()
            curr_page += 1 

            if parse_method == 1 :
               page_find = re.findall(r"Page : ([0-9]+) of ([0-9]+)",page_text)  
               _curr_page , tot_page = int(page_find[0]) , int(page_find[1])
               if curr_page != _curr_page : raise Exception("parse method 1 not applicable") 
            if parse_method == 2 :
               page_find = re.findall(r"([0-9]+) of Page:",page_text)
               l = len(str(curr_page))
               if str(curr_page) == page_find[0][-l:] : 
                   tot_page = int(page_find[0][ : -l ])
               else : 
                  print( pdf_file_path , page_num )
                  print( page_text )
                  raise Exception("parse method 2 not applicable") 

            if curr_page == 1 : 
               pdf_writer = PyPDF2.PdfFileWriter() 

            pdf_writer.addPage(page)

            if curr_page == tot_page : 
               f = re.findall( pattern , page_text )[0]
               fname =  pdf_name_apply(f) + ".pdf"
               curr_page = 0 
               if filter_file is not None and f not in filter_file : continue 
               os.makedirs( os.path.dirname(fname) , exist_ok = True )
               with open(fname, 'wb') as output_file:
                   pdf_writer.write(output_file)
