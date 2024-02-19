YouTube Video Search Application
Overview
In the initial part of this project, I utilized the Trafilatura library to perform web scraping on YouTube. Trafilatura is a Python library for extracting content from web pages. The goal was to extract relevant information from a specific YouTube user's page.

Video Search Application
The subsequent part of the project involves the development of a Python application that allows users to search for videos on YouTube. The application prompts the user to input a YouTube username and the name of the video they are looking for. It then queries the YouTube Data API to find relevant videos either within the specified user's channel or among all users.

Functionality
User Input:

Users are prompted to provide a YouTube username (optional) and the name of the video they are searching for.
Search Options:

The application can perform searches within a specific user's videos or across all users on YouTube.
Results Display:

The application displays up to 5 videos with similar names to the user-provided video name.
Usage
API Key Setup:

Replace 'YOUR_API_KEY' in the code with your actual YouTube Data API key obtained from the Google Cloud Console.
User Input:

Run the application and input the YouTube username (optional) and the video name you are looking for.
Results Display:

The application will display up to 5 videos with similar names, either within the specified user's channel or among all users.
Dependencies
google-api-python-client: Used to interact with the YouTube Data API.
fuzzywuzzy: Used for fuzzy matching to find videos with similar names.
trafilatura: Used for web scraping YouTube pages.
Note: Please make sure to review and comply with YouTube's API terms of service and usage policies.


Ultimate and Final Code: The last presented code in this .py and .ipynb files is the ultimate and final version of the YouTube Video Search Application. Feel free to use and customize it according to your needs.



