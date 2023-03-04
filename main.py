import datetime
from supabase import create_client, Client
from flask import Flask, render_template, request

app = Flask(__name__)

url, key = open("SECRET.txt", "r").read().split("\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("request received:", request.form)
        # Temporarily store header image in file
        with open("header.jpg", "wb") as f:
            f.write(request.files['header-img'].read())

        # Initialize Supabase client
        client = create_client(url, key)

        # Upload header image to Supabase storage
        client.storage().from_('images').upload(request.files['header-img'].filename, 'header.jpg')

        # Insert article into Supabase database
        client.table('article').insert([
            {
                'title': request.form['title'],
                'content': request.form['content'],
                'published': "true",
                'authors': [i.lstrip().rstrip() for i in request.form['authors'].split(",")],
                'category': request.form['category'],
                'subcategory': request.form['subcategory'],
                'img': url + "/storage/v1/object/public/images/" + request.files['header-img'].filename,
                'month': datetime.datetime.now().month,
                'year': datetime.datetime.now().year
            }
        ]).execute()
        return render_template('index.html', success=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)