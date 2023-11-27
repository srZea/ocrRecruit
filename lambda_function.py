import json
import os
import subprocess
import tempfile
import pdfplumber

def lambda_handler(event, context):

    try:
      completeText = []
      file_content = event['body']

      with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
          temp_file.write(file_content.encode('utf-8'))
          temp_file_path = temp_file.name

      local_path = temp_file_path

      output_pdf_path = '/tmp/ocr_output.pdf'
      subprocess.run(['ocrmypdf','--force-ocr', local_path, output_pdf_path])

      with pdfplumber.open(output_pdf_path) as pdf:
        for i in range(0,len(pdf.pages)):
          page = pdf.pages[i]
          text = page.extract_text(x_tolerance=2, y_tolerance=2)
          completeText.append(text)
        
      completeText = "".join(completeText)

      response = {
          "statusCode": 200,
          "body": json.dumps({"text_response": completeText})
      }
      os.remove(output_pdf_path)
      return response
    except Exception as e:
      response = {
          'statusCode': 500,
          'body': json.dumps({'error': str(e)})
          }
      return response

    