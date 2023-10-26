from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'helloworld'  # Change this to a secure secret key.

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if pdf_file:
        # Save the uploaded PDF file to a temporary directory
        upload_folder = 'temp_uploads'  # Create a 'temp_uploads' directory
        os.makedirs(upload_folder, exist_ok=True)
        pdf_file_path = os.path.join(upload_folder, pdf_file.filename)
        pdf_file.save(pdf_file_path)

        # Execute your Python script on the uploaded PDF
        try:
            result = subprocess.run(['python', 'main.py', pdf_file_path], capture_output=True, text=True)
            output = result.stdout
            error = result.stderr
            # You can do something with the output or error if needed.
        except Exception as e:
            flash(f'Error: {str(e)}')
        finally:
            os.remove(pdf_file_path)  # Remove the uploaded PDF after processing

    return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
