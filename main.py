import os
from PyPDF2  import PdfFileMerger,PdfFileWriter, PdfFileReader


def move_pdf_page():
    base = str(input("Provide a path to the PDF file: "))
    if not (os.path.isfile(base) and os.path.splitext(base)[1] == ".pdf"):
        print("this path doesn't lead to an existing pdf file")
        return
    page = int(input("Provide a page to move within the file (page number?): "))
    
    baseReader = PdfFileReader(base)
    position = int(input("Provide a page number in the base PDF file where to insert the new pdf (insert after page # ?): "))
    if (page > baseReader.getNumPages() or page < 1 ) or (position > baseReader.getNumPages() or position < 1 ):
        print("invalid page number")
        return
    page-=1
    position-=1
    baseWriter = PdfFileWriter()
    for i in range(baseReader.getNumPages()):
        if i != page:
            baseWriter.addPage(baseReader.getPage(i))
    pageObj = baseReader.getPage(page)
    baseWriter.insertPage(pageObj,position)

    baseWriter.write(open(base,"wb"))



def merge_pdf_after_page():
    base = str(input("Provide a path to the PDF file to use as base: "))
    input1 = str(input("Provide a path to the PDF file to use as input: "))
    if not (os.path.isfile(base) and os.path.isfile(input1) and os.path.splitext(base)[1] == ".pdf" and os.path.splitext(input1)[1] == ".pdf"):
        print("these paths don't lead to existing pdf files")
        return
    position = int(input("Provide a page number in the base PDF file where to insert the new pdf (insert after page # ?): "))
    out_path =  str(input("Provide a directory path where to save the output pdf file : "))
    if not os.path.isdir(out_path):
        print("this path doesn't lead to an existing directory")
        return
    out_name = str(input("Provide a file name for the output pdf file : "))+".pdf"
    try:
        merger = PdfFileMerger()
        merger.append(base)
        merger.merge(position,input1)

        out_path = os.path.join(out_path,out_name)
        output = open(out_path,"wb")
        merger.write(output)
        merger.close()
    except:
        print("Exception error occured")

def merge_pdf_in_dir():
    path = str(input("Provide a directory path where you want to merge all pdf files: "))
    out_name = str(input("Provide a file name for the output pdf file : "))+".pdf"
    if os.path.isdir(path):
        merger = PdfFileMerger()
        for filename in os.listdir(path):
            f = os.path.join(path,filename)
            if os.path.isfile(f) and os.path.splitext(f)[1] == ".pdf":
                # print(filename)
                pdfFile = open(f,"rb")

                merger.append(pdfFile)

        out_path = os.path.join(path,out_name)
        output = open(out_path,"wb")
        merger.write(output)
        merger.close()
    else:
        print("This path isn't a directory")


def main():
    choice = int(input ("Enter 1 for merge all pdf in directory.\nEnter 2 to move a page in PDF file to position x.\nEnter 3 for merge two pdfs after page x.\n"))
    if choice == 1:
        merge_pdf_in_dir()
    elif choice == 2:
        move_pdf_page()
    elif choice == 3:
        merge_pdf_after_page()
    else:
        print("Invalid choice")

if __name__=="__main__":
    main()
