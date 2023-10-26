from flask import Flask, render_template, request, redirect, url_for, flash
from github import Github
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'helloworld'  # Change this to a secure secret key.

# Replace with your GitHub personal access token
GITHUB_ACCESS_TOKEN = 'YOUR_GITHUB_ACCESS_TOKEN'

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
        # Authenticate with GitHub using your access token
        g = Github(GITHUB_ACCESS_TOKEN)

        # Specify the GitHub repository and branch you want to work with
        repo = g.get_repo('username/repo-name')
        branch = repo.get_branch('main')

        # Specify the folder where you want to upload the PDF
        upload_folder = 'temp_uploads'

        # Create a 'temp_uploads' directory on GitHub if it doesn't exist
        try:
            content = repo.get_contents(upload_folder, ref=branch.commit.sha)
        except:
            repo.create_file(
                path=upload_folder,
                message='Create temp_uploads directory',
                content='Creating temp_uploads directory',
                branch='main',
            )

        # Save the uploaded PDF file to the 'temp_uploads' directory on GitHub
        pdf_file_path = os.path.join(upload_folder, pdf_file.filename)
        pdf_file_contents = pdf_file.read()
        pdf_file_contents_base64 = base64.b64encode(pdf_file_contents).decode('utf-8')

        try:
            repo.create_file(
                path=pdf_file_path,
                message='Upload PDF file',
                content=pdf_file_contents_base64,
                branch='main',
            )

            # Execute your Python script on the uploaded PDF
            try:
                result = subprocess.run(['python', 'main.py', pdf_file_path], capture_output=True, text=True)
                output = result.stdout
                error = result.stderr
                # You can do something with the output or error if needed.
            except Exception as e:
                flash(f'Error: {str(e)}')
        except Exception as e:
            flash(f'Error uploading the file to GitHub: {str(e)}')

    return redirect(url_for('index'))
