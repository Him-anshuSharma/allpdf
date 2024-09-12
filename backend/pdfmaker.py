import os
import subprocess
from PyPDF2 import PdfMerger
from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__, template_folder = '../frontend')

def convert_to_pdf(file_path, output_folder):
    # Converts .docx, .doc, .pptx files to PDF using LibreOffice
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', output_folder, file_path])

def merge_pdfs(output_path, pdf_files):
    merger = PdfMerger()
    for pdf_file in sorted(pdf_files):
        merger.append(pdf_file)
    merger.write(output_path)
    merger.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert_and_merge', methods=['POST'])
def convert_and_merge():
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist('files')
    output_folder = '/tmp/converted_pdfs'
    os.makedirs(output_folder, exist_ok=True)

    pdf_files = []

    for file in files:
        file_path = os.path.join(output_folder, file.filename)
        file.save(file_path)
        
        base_name, extension = os.path.splitext(file.filename)
        
        # Convert if it's a docx, doc, pptx or process pdf directly
        if extension in ['.docx', '.doc', '.pptx']:
            convert_to_pdf(file_path, output_folder)
            pdf_file = os.path.join(output_folder, f"{base_name}.pdf")
            pdf_files.append(pdf_file)
        elif extension == '.pdf':
            pdf_files.append(file_path)
    
    output_path = os.path.join(output_folder, 'merged_output.pdf')
    merge_pdfs(output_path, pdf_files)

    # Send the merged PDF file back
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
