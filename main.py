import os, sys, signal
from PyPDF2  import PdfFileMerger,PdfFileWriter, PdfFileReader




def replace_page():
    base = str(input("Provide a path to the PDF file to use as base: "))
    input1 = str(input("Provide a path to the PDF file to use as input: "))
    if not (os.path.isfile(base) and os.path.isfile(input1) and os.path.splitext(base)[1] == ".pdf" and os.path.splitext(input1)[1] == ".pdf"):
        print("these paths don't lead to existing pdf files")
        return
    page = int(input("Provide a page number in the base PDF file where to replace by the new pdf (page number ?): "))
    baseReader = PdfFileReader(base)
    inputReader = PdfFileReader(input1)
    if page > baseReader.getNumPages() or page < 1 :
        print("invalid page number")
        return
    page-=1
    baseWriter = PdfFileWriter()
    for i in range(baseReader.getNumPages()):
        if i != page:
            baseWriter.addPage(baseReader.getPage(i))
        else:
            baseWriter.appendPagesFromReader(inputReader)
    baseWriter.write(open(base,"wb"))
    print("Done, your base pdf file has been modified")


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
    print("Done, your base pdf file has been modified")



def merge_pdf_after_page():
    base = str(input("Provide a path to the PDF file to use as base: "))
    input1 = str(input("Provide a path to the PDF file to use as input: "))
    if not (os.path.isfile(base) and os.path.isfile(input1) and os.path.splitext(base)[1] == ".pdf" and os.path.splitext(input1)[1] == ".pdf"):
        print("these paths don't lead to existing pdf files")
        return
    position = int(input("Provide a page number in the base PDF file where to insert the new pdf (insert after page # ?): "))
    range_input=str(input("Provide a range of pages from input file to insert with format: page#,page#\nTo insert all pages press ENTER: "))
    position-=1
    r=None
    if range_input:
        r=list(map(int,range_input.split(',')))
        if len(r) != 2:
            print("Wrong page range format")
            return
        else:
            r[0]-=1
            r=tuple(r)
    
    out_path =  str(input("Provide a directory path where to save the output pdf file : "))
    if not os.path.isdir(out_path):
        print("this path doesn't lead to an existing directory")
        return
    out_name = str(input("Provide a file name for the output pdf file : "))+".pdf"
    merger = PdfFileMerger()
    merger.append(base)
    merger.merge(position,input1,pages=r)

    out_path = os.path.join(out_path,out_name)
    output = open(out_path,"wb")
    merger.write(output)
    merger.close()
    print(f'Done, your new pdf file should be at: {out_path}')


def merge_pdf_in_dir():
    path = str(input("Provide a folder path where you want to merge all pdf files: "))
    out_name = str(input("Provide a file name for the output pdf file : "))+".pdf"
    if os.path.isdir(path):
        merger = PdfFileMerger()
        for filename in sorted(filter(lambda x: os.path.isfile(os.path.join(path,x)),os.listdir(path))):
            f = os.path.join(path,filename)
            if os.path.splitext(f)[1] == ".pdf":
                print(filename)
                pdfFile = open(f,"rb")
                merger.append(pdfFile)

        out_path = os.path.join(path,out_name)
        output = open(out_path,"wb")
        merger.write(output)
        merger.close()
        print(f'Done, your new pdf file should be at: {out_path}')
    else:
        print("This path isn't a directory")

def done(sig, frame):
    print("\nBye")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, done)
    choice = int(input ("Enter 1 for merge all pdf in directory(ordered by filename).\nEnter 2 to move a page in PDF file to page x.\nEnter 3 to replace a page with a new pdf file.\nEnter 4 for insert pdf into another at page x.\nPress CTRL-C to exit\n "))
    if choice == 1:
        merge_pdf_in_dir()
    elif choice == 2:
        move_pdf_page()
    elif choice == 3:
        replace_page()
    elif choice == 4:
        merge_pdf_after_page()
    else:
        print("Invalid choice")

if __name__=="__main__":
    main()

