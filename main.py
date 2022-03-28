import os

import click
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter


class Range(click.ParamType):
    name = "range_input"
    def convert(self, value, param, ctx):
        try:
            r=list(map(int,value.split(',')))      
            r[0]-=1
            return tuple(r)
        except :
            self.fail("Wrong page range format", param, ctx)


                
@click.group()
def main():
    pass

@main.command()
@click.option("--base_pdf_path",prompt="Provide a path to the PDF file to use",type=click.Path(exists=True,dir_okay=False))
@click.option("--input_pdf_path",prompt="Provide a path to the PDF file to use",type=click.Path(exists=True,dir_okay=False))
@click.option("--page",prompt="Provide a page number in the base PDF file where to replace by the input pdf",type=int)
def replace_page(base_pdf_path,input_pdf_path,page):
    baseReader = PdfFileReader(base_pdf_path)
    inputReader = PdfFileReader(input_pdf_path)
    
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
    baseWriter.write(open(base_pdf_path,"wb"))
    print("Done, your base pdf file has been modified")

@main.command()
@click.option("--base_pdf_path",prompt="Provide a path to the PDF file to use",type=click.Path(exists=True,dir_okay=False))
@click.option("--page_to_move",prompt="Provide a page to move within the file (page number?)",type=int)
@click.option("--after_page",prompt="Provide a page number in the base PDF file where to insert the new pdf (insert after page # ?)",type=int)
def move_pdf_page(base_pdf_path,page_to_move,after_page):
    baseReader = PdfFileReader(base_pdf_path)
  
    if (page_to_move > baseReader.getNumPages() or page_to_move < 1 ) or (after_page > baseReader.getNumPages() or after_page < 1 ):
        print("invalid page number")
        return
    page_to_move-=1
    after_page-=1
    baseWriter = PdfFileWriter()
    for i in range(baseReader.getNumPages()):
        if i != page_to_move:
            baseWriter.addPage(baseReader.getPage(i))
    pageObj = baseReader.getPage(page_to_move)
    baseWriter.insertPage(pageObj,after_page)
    baseWriter.write(open(base_pdf_path,"wb"))
    print("Done, your base pdf file has been modified")


@main.command()
@click.option("--base_pdf_path",prompt="Provide a path to the PDF file to use",type=click.Path(exists=True,dir_okay=False))
@click.option("--input_pdf_path",prompt="Provide a path to the PDF file to use as input",type=click.Path(exists=True,dir_okay=False))
@click.option("--after_page",prompt="Provide a page number in the base PDF file where to insert the new pdf (insert after page # ?)",type=int)
@click.option("--range_input",prompt="Provide a range of pages from input file to insert with format: FromPage#,ToPage# [OPTIONAL]",type=Range(),required=False)
@click.option("--out_dir_path",prompt="Provide a directory path where to save the output pdf file",type=click.Path(exists=True,dir_okay=True,file_okay=False))
@click.option("--out_name",prompt="Provide a file name for the output pdf file",type=str)
def merge_pdf_after_page(base_pdf_path,input_pdf_path,after_page,range_input,out_dir_path,out_name):
    position=after_page
    
    if(len(out_name.split('.'))==1): out_name+='.pdf'
    merger = PdfFileMerger()
    merger.append(base_pdf_path)

    ip = PdfFileReader(input_pdf_path)

    if ip.isEncrypted:
        ip.decrypt('')

    merger.merge(position,ip,pages=range_input)

    out_path = os.path.join(out_dir_path,out_name)
    output = open(out_path,"wb")
    merger.write(output)
    merger.close()
    print(f'Done, your new pdf file should be at: {out_path}')

@main.command()
@click.option("--dir_path",prompt="Provide a full folder path where you want to merge all pdf files",type=click.Path(exists=True,dir_okay=True,file_okay=False))
@click.option("--out_name",prompt="Provide a file name for the output pdf file",type=str)
def merge_pdf_in_dir(dir_path,out_name):
    if(len(out_name.split('.'))==1): out_name+='.pdf'
    if os.path.isdir(dir_path):
        merger = PdfFileMerger()
        for filename in sorted(filter(lambda x: os.path.isfile(os.path.join(dir_path,x)),os.listdir(dir_path))):
            f = os.path.join(dir_path,filename)
            if os.path.splitext(f)[1] == ".pdf":
                print(filename)
                pdfFile = open(f,"rb")
                merger.append(pdfFile)

        out_path = os.path.join(dir_path,out_name)
        output = open(out_path,"wb")
        merger.write(output)
        merger.close()
        print(f'Done, your new pdf file should be at: {out_path}')
    else:
        print("This path isn't a directory")



if __name__=="__main__":
    main()

