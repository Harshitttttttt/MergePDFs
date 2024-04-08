import fitz
import os

def merge_pdfs(pdf_dir, output_filename, number_of_pdfs, format_of_file_name):
    merged_doc = fitz.open()
    page_count_list = []
    for idx in range(1, number_of_pdfs+1):
        filename = format_of_file_name.replace('i', str(idx)) + ".pdf"
        filepath = os.path.join(pdf_dir, filename)
        if os.path.isfile(filepath):
            src_doc = fitz.open(filepath)
            merged_doc.insert_pdf(src_doc)
            page_count_list.append(src_doc.page_count)
            src_doc.close()
        else:
            print(f"File {filename} not found.")
            
    merged_doc.save(output_filename)
    
    print_output(page_count_list, merged_doc, output_filename)
    
def print_output(page_count_list, merged_doc, output_filename):
    print(f"Page count of the all PDFs: {page_count_list}")
    print(f"Total page count of the all PDFs: {sum(page_count_list)}")
    print(f"Page count of the merged PDF: {merged_doc.page_count}")
    print(f"Files merged into {output_filename}")
    
def get_input():
    number_of_pdfs = int(input("Enter the number of PDFs to merge: "))
    pdf_dir = input("Enter the directory containing the PDFs: ")
    output_filename = input("Enter the output filename: ")
    output_filename = pdf_dir + "/" + output_filename + ".pdf"
    format_of_file_name = input("Enter the format of the file name with an 'i' at the place of the file number e.g: T23-999 CC EXPi or T24-22 AOA EXi: ")
    print("\n")
    return pdf_dir, output_filename, number_of_pdfs, format_of_file_name

def ask_for_header_or_footer():
    header_or_footer = input("Do you want to add a header or footer to the merged PDF? (y/n): ")
    if header_or_footer == 'y':
        return True
    else:
        return False
    
def add_header_or_footer(output_filename):
    temp_output_filename = output_filename.replace(".pdf", "_h&f.pdf")
    doc = fitz.open(output_filename)
    header = input("Enter the text for the header: ")
    footer = input("Enter the text for the footer: ")
    for page in doc:
        page.clean_contents()
        page.insert_text((page.rect.width/2, 50), header)  # insert header
        page.insert_text((page.rect.width-75-len(footer), page.rect.height - 50), footer) # insert footer
        
    doc.save(temp_output_filename)
    print(f"Header and footer added to {output_filename}")
    
if __name__ == "__main__":
    pdf_dir, output_filename, number_of_pdfs, format_of_file_name = get_input()
    merge_pdfs(pdf_dir, output_filename, number_of_pdfs, format_of_file_name)
    if ask_for_header_or_footer():
        add_header_or_footer(output_filename)