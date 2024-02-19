#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# load necessary components
from trafilatura import fetch_url, extract


# In[ ]:


url = 'https://www.youtube.com/@roxsauce'
downloaded = fetch_url(url)
downloaded is None  # assuming the download was successful


# In[ ]:


import trafilatura

def extract(html_content):
    try:
        extracted_text = trafilatura.extract(html_content)
        return extracted_text
    except Exception as e:
        print(f"An error occurred during extraction: {e}")
        return None

# Assuming you've already fetched the HTML content using fetch_url
url = 'https://www.youtube.com/@roxsauce'
downloaded = fetch_url(url)

if downloaded is not None:
    extracted_text = extract(downloaded)
    if extracted_text is not None:
        print(extracted_text)
    else:
        print("Extraction failed.")
else:
    print("Download failed.")


# In[8]:


from trafilatura import extract

# Assuming 'downloaded' and 'url' are defined somewhere
result = extract(downloaded)
result_without_newlines = result.replace('\n', ' ')
print(result_without_newlines)

# You can do the same for other cases
result_with_links = extract(downloaded, include_links=True)
result_with_links_without_newlines = result_with_links.replace('\n', ' ')
print(result_with_links_without_newlines)

result_xml = extract(downloaded, output_format='xml')
result_xml_without_newlines = result_xml.replace('\n', ' ')
print(result_xml_without_newlines)

result_xml_with_links = extract(downloaded, output_format='xml', include_links=True)
result_xml_with_links_without_newlines = result_xml_with_links.replace('\n', ' ')
print(result_xml_with_links_without_newlines)

# Make sure to provide the 'url' parameter if needed
result_links_without_newlines = extract(downloaded, include_links=True, url=url).replace('\n', ' ')
print(result_links_without_newlines)


# In[9]:


# no comments in output
result = extract(downloaded, include_comments=False)

# skip tables examination
result = extract(downloaded, include_tables=False)

# output with links
result = extract(downloaded, include_links=True)
# and so on...


# In[10]:


result = extract(downloaded, url, favor_precision=True)
result


# In[11]:


from trafilatura import html2txt
html2txt(downloaded)


# In[12]:


result = extract(downloaded, url, target_language="de")


# In[13]:


# skip algorithms used as fallb
result = extract(downloaded, no_fallback=True)


# In[14]:


# skip algorithms used as fallbac
result = extract(downloaded, no_fallback=True)


# In[15]:


result = extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)


# In[16]:


# create a filename-safe string by hashing the given content
from trafilatura.hashing import generate_hash_filename
generate_hash_filename("This is a text.")


# In[17]:


# create a Simhash for near-duplicate detectio
from trafilatura.hashing import Simhash
first = Simhash("This is a text.")
second = Simhash("This is a test.")
second.similarity(first)




# In[18]:


# use existing Simhash
first_copy = Simhash(existing_hash=first.hash)
first_copy.similarity(first)


# In[19]:


from trafilatura.settings import use_config
from trafilatura import extract

# Assuming 'downloaded' and 'url' are defined somewhere
newconfig = use_config()
newconfig.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
result = extract(downloaded, config=newconfig)

# Remove newline characters from the result
result_without_newlines = result.replace('\n', ' ')

print(result_without_newlines)



# In[20]:


# import the extract() function, use a previously downloaded document
# pass the new parameters as dict
extract(downloaded, output_format="xml", date_extraction_params={
        "extensive_search": True, "max_date": "2018-07-01"
    })


# In[21]:


from trafilatura import bare_extraction


# In[22]:


def bare_extraction(downloaded, with_metadata=True, url=None):
    # Your implementation goes here
    pass  # Replace this with your actual implementation

# Now you can use the function
bare_extraction(downloaded, with_metadata=True)
bare_extraction(downloaded, with_metadata=True, url=url)



# In[23]:


from trafilatura.meta import reset_caches

# at any given point
reset_caches()


# In[24]:


from trafilatura import bare_extraction
bare_extraction(downloaded)


# In[25]:


# necessary components
from trafilatura import fetch_response, bare_extraction

# load an example
response = fetch_response("https://www.youtube.com")

# perform extract() or bare_extraction() on Trafilatura's response object
# your additional code here...


# In[26]:


bare_extraction(response.data, url=response.url)  # here is the redirectio


# In[27]:


# define document and load it with LXML
from lxml import html
my_doc = """<html><body><article><p>
                Here is the main text.
                </p></article></body></html>"""
mytree = html.fromstring(my_doc)
# extract from the already loaded LXML tree
extract(mytree)


# In[32]:


from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with the API key you obtained
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def search_video(api_key, video_name):
    # Search for videos by title
    search_response = youtube.search().list(
        q=video_name,
        part='id',
        type='video',
    ).execute()

    if 'items' in search_response:
        video_id = search_response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        print(f'Found video: {video_url}')
    else:
        print('Video not found.')

# Ask the user for the video name
video_name = input("Enter the video name you are looking for: ")

# Search for the video using the API
search_video(api_key, video_name)


# In[33]:


from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with the API key you obtained
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def search_video(api_key, username=None, video_name=None):
    if username:
        # If a specific username is provided, search within that user's videos
        search_response = youtube.channels().list(
            forUsername=username,
            part='id'
        ).execute()

        if 'items' in search_response:
            channel_id = search_response['items'][0]['id']
            videos_response = youtube.search().list(
                channelId=channel_id,
                q=video_name,
                part='id',
                type='video',
            ).execute()

            if 'items' in videos_response:
                video_id = videos_response['items'][0]['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                print(f'Found video: {video_url}')
            else:
                print('Video not found in the specified user\'s videos.')

        else:
            print(f'User with username "{username}" not found.')

    else:
        # If no specific username is provided, search among all videos
        search_response = youtube.search().list(
            q=video_name,
            part='id',
            type='video',
        ).execute()

        if 'items' in search_response:
            video_id = search_response['items'][0]['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            print(f'Found video: {video_url}')
        else:
            print('Video not found among all users and videos.')

# Ask the user for the username
username = input("Enter the YouTube username (leave blank for all users): ")

# Ask the user for the video name
video_name = input("Enter the video name you are looking for: ")

# Search for the video using the API
search_video(api_key, username, video_name)


# In[34]:


from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with the API key you obtained
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def search_videos(api_key, username=None, video_name=None, max_results=5):
    if username:
        # If a specific username is provided, search within that user's videos
        search_response = youtube.channels().list(
            forUsername=username,
            part='id'
        ).execute()

        if 'items' in search_response:
            channel_id = search_response['items'][0]['id']
            videos_response = youtube.search().list(
                channelId=channel_id,
                q=video_name,
                part='snippet',
                type='video',
                maxResults=max_results,
            ).execute()

            if 'items' in videos_response:
                print(f"Found videos in the specified user's channel:")
                for item in videos_response['items']:
                    video_id = item['id']['videoId']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    print(f'{item["snippet"]["title"]}: {video_url}')

            else:
                print(f'No videos found in the specified user\'s channel with a similar name.')

        else:
            print(f'User with username "{username}" not found.')

    else:
        # If no specific username is provided, search among all videos
        search_response = youtube.search().list(
            q=video_name,
            part='snippet',
            type='video',
            maxResults=max_results,
        ).execute()

        if 'items' in search_response:
            print("Found videos among all users and videos:")
            for item in search_response['items']:
                video_id = item['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                print(f'{item["snippet"]["title"]}: {video_url}')

        else:
            print('No videos found among all users and videos with a similar name.')

# Ask the user for the username
username = input("Enter the YouTube username (leave blank for all users): ")

# Ask the user for the video name
video_name = input("Enter the video name you are looking for: ")

# Search for the videos using the API
search_videos(api_key, username, video_name, max_results=5)



# In[ ]:




