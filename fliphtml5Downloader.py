"""

This Downloads the book from fliphtml5. The recently changed their file structures, so most of the codes on github will not work. This is the latest written in 2024 and is working in January 2024.

It will fetch the images of pages from fliphtml5, and then make pdf from them. Make sure that you have installed the dependencies, before executing this code.

It's a pretty simple and basic code with no complexities. For understanding, there will be more comment lines than the actual code :D

I was able to make this code in two days altogether which includes major time of research on fliphtml5.

"""

# One way is to import everything beforhand, but we will import the libraries, the moment we have to use them.
import requests
import json
import re
import os
from PIL import Image
import io

"""
First we need to see the url structure, the url structure is https://online.fliphtml5.com/*****/**** where the aestricks are different for every book, so we need to get this as input from you, so that you can download your favorite book.


Just punch in the format mentioned below.

*****/****

"""

#Taking Book reference/link from user
book_name = input("Enter the book link in the format *****/****:\n")

# We will fetch config file below

#url of config file
config_file_url = 'https://online.fliphtml5.com/{0}/javascript/config.js'.format(book_name)

#Request to get config file
config_file = requests.get(config_file_url)
config_dict = json.loads(config_file.text.split('= ')[1][:-1])      #changed from split(;) to slicing to remove last semicolon.
fliphtml5_pages = config_dict['fliphtml5_pages']

#Let's prepare where to save our images, creates folder as per title of book
folder_name = config_dict['meta']['title']
# Replace invalid characters
folder_name = re.sub(r'[<>:"/\\|?*]', '_', folder_name) #suggested by a person named astreopoli

os.makedirs(folder_name, exist_ok=True)

#Let's download our images now
"""
Below code is being added to see which url pattern is being followed.
"""
def url_patterns(book_name, page):
    #Fliphtml5 uses different options of url for different books. Feel free to add more options in the dictionary below.
    url_options = {
        0: f'https://online.fliphtml5.com/{book_name}/files/large/{fliphtml5_pages[page]['n'][0]}',
        1: f'https://online.fliphtml5.com/{book_name}/files/page/{page+1}.jpg',
        2: f'https://online.fliphtml5.com/{book_name}{fliphtml5_pages[page]['n'][0][1:]}',
        3: f'https://online.fliphtml5.com/{book_name}/#p{page + 1}',
    }
    for key in url_options.keys():
        page_image = requests.get(url_options[key])
        if page_image.status_code == 200:
            return url_options[key]
    return ''

page_images=[]
for page in range(len(fliphtml5_pages)):
    print(fliphtml5_pages[page]['n'][0][1:])
    page_url = url_patterns(book_name, page)
    if page_url != '':
        file_path = f"{folder_name}/{page + 1}.webp" # Replace .jpg"
        page_image = requests.get(page_url)
        page_images.append(page_image.content)
        print(f'Downloading Page {str(page + 1)} / {str(len(fliphtml5_pages))}')
        with open(file_path, "wb") as f:
            f.write(page_image.content)

        # Verification step
        try:
            with Image.open(file_path) as img:
                img.verify()
            print(f'Page {page + 1} saved and verified as a valid webp image.')
        except Exception as e:
            print(f'Warning: Page {page + 1} could not be verified as a valid webp image: {e}')
    else:
        print('Send an email to developer with your book name or comment on the youtube video with the book name.')
        break

if page_url != '' and page_images != []:
    print("Downloading Complete. Don't Close, hold-on. We are yet to make PDF.")

    # Process webp files
    image_objs = []
    for img_bytes in page_images:
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")  # Convert webp to RGB
        image_objs.append(image)

    #Let's make pdf now.
    pdf_path = f"{folder_name}.pdf"
    image_objs[0].save(pdf_path, save_all=True, append_images=image_objs[1:])

    print(f'The pdf named {folder_name}.pdf has been saved in your working directory.')
    print('Thank you for using this script originally written by Engr Moaz Dev.')
