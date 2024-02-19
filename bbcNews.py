#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import spacy

def get_available_topics():
    url = 'https://www.bbc.com/news'
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        topics_list = soup.select('.sc-44f1f005-0 .hCrDEz')

        if topics_list:
            topics = {i + 1: topic.text.strip() for i, topic in enumerate(topics_list)}
            return topics
        else:
            print("No topics found on the page.")
            return {}
    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return {}

def get_articles(topic):
    url = f'https://www.bbc.com/news/{topic}'
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles_list = soup.select('.sc-44f1f005-0 .hCrDEz')

        if articles_list:
            return [article.text.strip() for article in articles_list]
        else:
            print("No articles found on the page.")
            return []
    else:
        print(f"Error: Unable to fetch articles. Status code: {response.status_code}")
        return []

def compare_statements(input_statement, documents):
    if not documents:
        print(f"No documents found for comparison.")
        return False

    nlp = spacy.load('en_core_web_sm')
    input_doc = nlp(input_statement)

    for document in documents:
        document_doc = nlp(document)
        similarity = input_doc.similarity(document_doc)

        # Adjust the similarity threshold as needed
        if similarity > 0.8:
            return True

    return False

def main():
    data_source = input("Enter the data source ('twitter' or 'bbc_news'): ")
    
    if data_source.lower() == 'bbc_news':
        available_topics = get_available_topics()

        if not available_topics:
            print("No topics available. Exiting.")
            return

        print("Available topics:")
        for number, topic in available_topics.items():
            print(f"{number}. {topic}")

        topic_number = int(input("Enter the number corresponding to the desired topic: "))
        topic_identifier = available_topics.get(topic_number)

        if not topic_identifier:
            print("Invalid topic number. Exiting.")
            return

        input_statement = input("Enter the statement to verify: ")
        documents = get_articles(topic_identifier)
    else:
        print("Invalid data source. Supported sources: 'bbc_news'")
        return

    if documents:
        is_legitimate = compare_statements(input_statement, documents)

        if is_legitimate:
            print("The statement is legitimate based on the data source.")
        else:
            print("The statement is not found among documents.")
    else:
        print("No documents found for the topic.")

if __name__ == "__main__":
    main()


# In[2]:


import requests
from bs4 import BeautifulSoup

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def choose_topic(topics):
    print("Available BBC News Topics:")
    for topic in topics:
        print(f"{topic[0]}. {topic[1]}")

    user_choice = input("Enter the number corresponding to the desired topic: ")
    return user_choice

def scrape_topic_page(topic_url):
    response = requests.get(topic_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add your scraping logic here
        print(f"Scraping data from {topic_url}")
        print("Scraped data:")
        #print(soup.prettify())
    else:
        print(f"Error: Unable to fetch topic page. Status code: {response.status_code}")

# Example usage:
bbc_topics = get_bbc_news_topics()

if bbc_topics:
    user_choice = choose_topic(bbc_topics)
    selected_topic = bbc_topics[int(user_choice) - 1]
    
    print(f"You selected: {selected_topic[1]}")
    scrape_topic_page(f'https://www.bbc.com{selected_topic[2]}')
else:
    print("No topics found.")

    
    
    


# In[3]:


import requests
from bs4 import BeautifulSoup

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def choose_topic(topics):
    print("Available BBC News Topics:")
    for topic in topics:
        print(f"{topic[0]}. {topic[1]}")

    user_choice = input("Enter the number corresponding to the desired topic: ")
    return user_choice

def get_user_statement():
    return input("Enter the statement you are looking for on the selected topic page: ")

def scrape_topic_page(topic_url, statement):
    response = requests.get(topic_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Add your specific scraping logic here
        # For example, checking if the statement is present in the page
        statement_found = statement.lower() in soup.get_text().lower()
        
        print(f"Scraping data from {topic_url}")
        print(f"Statement '{statement}' {'found' if statement_found else 'not found'} on the page.")
    else:
        print(f"Error: Unable to fetch topic page. Status code: {response.status_code}")

# Example usage:
bbc_topics = get_bbc_news_topics()

if bbc_topics:
    user_choice = choose_topic(bbc_topics)
    selected_topic = bbc_topics[int(user_choice) - 1]
    
    print(f"You selected: {selected_topic[1]}")
    user_statement = get_user_statement()
    scrape_topic_page(f'https://www.bbc.com{selected_topic[2]}', user_statement)
else:
    print("No topics found.")


# In[4]:


import requests
from bs4 import BeautifulSoup

def choose_data(data_list):
    print("Available Options:")
    for data in data_list:
        print(f"{data[0]}. {data[1]}")

    while True:
        user_choice = input("Enter the number corresponding to the desired option: ")
        if user_choice.isdigit() and 1 <= int(user_choice) <= len(data_list):
            return user_choice
        else:
            print("Invalid input. Please enter a valid number.")
def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # List of classes and IDs to check
        classes_and_ids_to_check = ['iframe', '.czRLo', '.jqwZKz', '.kTrQIN', '.kbvxap', '.crzIlm', '.dJMMNx', '.hPAmAW', '.huflns']

        for class_or_id in classes_and_ids_to_check:
            target_elements = soup.select(class_or_id)

            if target_elements:
                for index, element in enumerate(target_elements):
                    print(f"Content inside element with class or ID '{class_or_id}' {index + 1}:")
                    print(element.get_text(strip=True))
            else:
                print(f"No elements with class or ID '{class_or_id}' found.")
    else:
        print(f"Error: Unable to fetch data page. Status code: {response.status_code}")

# Example usage:
bbc_topics = get_bbc_news_topics()

if bbc_topics:
    user_choice = choose_topic(bbc_topics)
    selected_topic = bbc_topics[int(user_choice) - 1]

    print(f"You selected: {selected_topic[1]}")
    data_list = scrape_topic_page(f'https://www.bbc.com{selected_topic[2]}')

    if data_list:
        user_data_choice = choose_data(data_list)
        selected_data = data_list[int(user_data_choice) - 1]

        print(f"You selected: {selected_data[1]}")
        scrape_data_page(f'https://www.bbc.com{selected_data[2]}')

else:
    print("No topics found.")

def choose_topic(topics):
    print("Available BBC News Topics:")
    for topic in topics:
        print(f"{topic[0]}. {topic[1]}")

    user_choice = input("Enter the number corresponding to the desired topic: ")
    return user_choice

def get_user_statement():
    return input("Enter the statement you are looking for on the selected topic page: ")

def scrape_topic_page(topic_url, statement):
    response = requests.get(topic_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        layers = topic_url.split('/')[4:]  # Extract layers from the URL

        # Navigate through the layers
        current_layer = soup
        for layer in layers:
            current_layer = current_layer.find('a', {'href': f'/{layer}'})
            if not current_layer:
                print(f"Error: Unable to navigate to layer '{layer}' in the topic page.")
                return

        # Add your specific scraping logic here
        # For example, checking if the statement is present in the page
        statement_found = statement.lower() in current_layer.get_text().lower()

        print(f"Scraping data from {topic_url}")
        print(f"Statement '{statement}' {'found' if statement_found else 'not found'} on the page.")
    else:
        print(f"Error: Unable to fetch topic page. Status code: {response.status_code}")

# Example usage:
bbc_topics = get_bbc_news_topics()

if bbc_topics:
    user_choice = choose_topic(bbc_topics)
    selected_topic = bbc_topics[int(user_choice) - 1]
    
    print(f"You selected: {selected_topic[1]}")
    user_statement = get_user_statement()
    scrape_topic_page(f'https://www.bbc.com{selected_topic[2]}', user_statement)
else:
    print("No topics found.")


# In[5]:


import requests
from bs4 import BeautifulSoup

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            print(f"Elements with class '{class_name}':")
            for element in elements:
                print(element.get_text(strip=True))
            print("\n")
        else:
            print(f"No elements with class '{class_name}' found.")

if __name__ == "__main__":
    # Get available topics
    topics = get_bbc_news_topics()

    if not topics:
        print("No topics found. Exiting.")
    else:
        # Display available topics to the user
        print("Available topics:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a topic
        try:
            user_choice = input("Enter the number corresponding to the desired topic: ")
            selected_topic = topics[int(user_choice) - 1]

            print(f"You selected: {selected_topic[1]} - URL: https://www.bbc.com{selected_topic[2]}")
            topic_url = f'https://www.bbc.com{selected_topic[2]}'

            # Make a request for the topic page
            topic_response = requests.get(topic_url)

            if topic_response.status_code == 200:
                soup = BeautifulSoup(topic_response.text, 'html.parser')
                
                # Classes to check
                classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

                # Scrape elements with specified classes
                scrape_with_classes(soup, classes_to_check)

            else:
                print(f"Error: Unable to fetch topic page. Status code: {topic_response.status_code}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid topic number.")


# In[6]:


import requests
from bs4 import BeautifulSoup

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = []
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            for element in elements:
                scraped_data.append(element.get_text(strip=True))
    
    return scraped_data

def compare_statement(statement, scraped_data):
    for data in scraped_data:
        if statement.lower() in data.lower():
            return True
    return False

if __name__ == "__main__":
    # Get available topics
    topics = get_bbc_news_topics()

    if not topics:
        print("No topics found. Exiting.")
    else:
        # Display available topics to the user
        print("Available topics:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a topic
        try:
            user_choice = input("Enter the number corresponding to the desired topic: ")
            selected_topic = topics[int(user_choice) - 1]

            print(f"You selected: {selected_topic[1]} - URL: https://www.bbc.com{selected_topic[2]}")
            topic_url = f'https://www.bbc.com{selected_topic[2]}'

            # Make a request for the topic page
            topic_response = requests.get(topic_url)

            if topic_response.status_code == 200:
                soup = BeautifulSoup(topic_response.text, 'html.parser')
                
                # Classes to check
                classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

                # Scrape elements with specified classes
                scraped_data = scrape_with_classes(soup, classes_to_check)

                # Ask the user to enter a statement for comparison
                user_statement = input("Enter the statement to verify: ")

                # Compare the user's statement with the scraped data
                if compare_statement(user_statement, scraped_data):
                    print(f"The statement '{user_statement}' is found on the page. It might be legitimate.")
                else:
                    print(f"The statement '{user_statement}' is not found on the page. It might not be legitimate.")

            else:
                print(f"Error: Unable to fetch topic page. Status code: {topic_response.status_code}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid topic number.")


# In[9]:


import requests
from bs4 import BeautifulSoup

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = {}
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            scraped_data[class_name] = [element.get_text(strip=True) for element in elements]
    
    return scraped_data

def compare_statement(statement, scraped_data):
    for class_name, data_list in scraped_data.items():
        for data in data_list:
            if statement.lower() in data.lower():
                return class_name, data
    return None, None

if __name__ == "__main__":
    # Get available topics
    topics = get_bbc_news_topics()

    if not topics:
        print("No topics found. Exiting.")
    else:
        # Display available topics to the user
        print("Available topics:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a topic
        try:
            user_choice = input("Enter the number corresponding to the desired topic: ")
            selected_topic = topics[int(user_choice) - 1]

            print(f"You selected: {selected_topic[1]} - URL: https://www.bbc.com{selected_topic[2]}")
            topic_url = f'https://www.bbc.com{selected_topic[2]}'

            # Make a request for the topic page
            topic_response = requests.get(topic_url)

            if topic_response.status_code == 200:
                soup = BeautifulSoup(topic_response.text, 'html.parser')
                
                # Classes to check
                classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

                # Scrape elements with specified classes
                scraped_data = scrape_with_classes(soup, classes_to_check)

                # Ask the user to enter a statement for comparison
                user_statement = input("Enter the statement to verify: ")

                # Compare the user's statement with the scraped data
                matched_class, matched_data = compare_statement(user_statement, scraped_data)

                if matched_class is not None and matched_data is not None:
                    print(f"The statement '{user_statement}' is found in the context of class '{matched_class}':")
                    print(matched_data)
                    print("Statement verified and legitimate!")
                else:
                    print(f"The statement '{user_statement}' is not found on the page. It might not be legitimate.")

            else:
                print(f"Error: Unable to fetch topic page. Status code: {topic_response.status_code}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid topic number.")


# In[21]:


import requests
from bs4 import BeautifulSoup
from difflib import get_close_matches

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = {}
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            scraped_data[class_name] = [element.get_text(strip=True) for element in elements]
    
    return scraped_data

def compare_statement(statement, scraped_data):
    matches = get_close_matches(statement.lower(), [data.lower() for data_list in scraped_data.values() for data in data_list], n=1, cutoff=0.8)
    
    if matches:
        for class_name, data_list in scraped_data.items():
            for data in data_list:
                if matches[0] in data.lower():
                    return class_name, data
    return None, None

def scrape_and_verify(user_statement, url, classes_to_check):
    try:
        # Make a request for the selected news page
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Scrape elements with specified classes
            scraped_data = scrape_with_classes(soup, classes_to_check)

            # Compare the user's statement with the scraped data
            matched_class, matched_data = compare_statement(user_statement, scraped_data)

            if matched_class is not None and matched_data is not None:
                print(f"The statement '{user_statement}' is found in the context of class '{matched_class}':")
                print(matched_data)
                print("Statement verified and legitimate!")
            else:
                if scraped_data:
                    print(f"The statement '{user_statement}' is not found. Similar data includes:")
                    for class_name, data_list in scraped_data.items():
                        print(f"Class '{class_name}': {data_list}")
                else:
                    print("No data found on the page.")

        else:
            print(f"Error: Unable to fetch news page. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get available news categories
    topics = get_bbc_news_topics()

    if not topics:
        print("No news categories found. Exiting.")
    else:
        # Display available news categories to the user
        print("Available news categories:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a news category
        try:
            user_choice = input("Enter the number corresponding to the desired news category: ")
            selected_topic = topics[int(user_choice) - 1]
            news_category_url = f'https://www.bbc.com{selected_topic[2]}'

            # Replace 'your_link_class' with the actual class name for the links to other pages
            classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

            # Ask the user to input the statement for verification
            user_statement = input("Enter the statement to verify: ")

            # Scrape content and verify statement
            scrape_and_verify(user_statement, news_category_url, classes_to_check)

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid news category number.")


# In[20]:


import requests
from bs4 import BeautifulSoup
from difflib import get_close_matches

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = {}
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            scraped_data[class_name] = elements
    
    return scraped_data

def find_links_in_context(user_statement, soup, classes_to_check):
    links = []

    for class_name in classes_to_check:
        elements = soup.find_all(class_=class_name)
        for element in elements:
            if user_statement.lower() in element.get_text(strip=True).lower():
                link = element.find('a')
                if link:
                    links.append(link.get('href'))

    return links

def compare_statement(statement, scraped_data):
    matches = get_close_matches(statement.lower(), [data.get_text(strip=True).lower() for data_list in scraped_data.values() for data in data_list], n=1, cutoff=0.8)
    
    if matches:
        for class_name, data_list in scraped_data.items():
            for data in data_list:
                if matches[0] in data.get_text(strip=True).lower():
                    return class_name, data
    return None, None

def scrape_and_verify(user_statement, url, classes_to_check):
    try:
        # Make a request for the selected news page
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Scrape elements with specified classes
            scraped_data = scrape_with_classes(soup, classes_to_check)

            # Find links in the context of the user's statement
            links = find_links_in_context(user_statement, soup, classes_to_check)

            # Compare the user's statement with the scraped data
            matched_class, matched_data = compare_statement(user_statement, scraped_data)

            if matched_class is not None and matched_data is not None:
                print(f"The statement '{user_statement}' is found in the context of:")
                print(matched_data.get_text(strip=True))
                print("Statement verified and legitimate!")
                if links:
                    print(f"Links related to the statement:")
                    for link in links:
                        print(link)
            else:
                if scraped_data:
                    print(f"The statement '{user_statement}' is not found. Similar data includes:")
                    for class_name, data_list in scraped_data.items():
                        for data in data_list:
                            print(f"Context: {data.get_text(strip=True)}")
                            link = data.find('a')
                            if link:
                                print(f"Link: {link.get('href')}")
                    if links:
                        print(f"Links related to the statement:")
                        for link in links:
                            print(link)
                else:
                    print("No data found on the page.")

        else:
            print(f"Error: Unable to fetch news page. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get available news categories
    topics = get_bbc_news_topics()

    if not topics:
        print("No news categories found. Exiting.")
    else:
        # Display available news categories to the user
        print("Available news categories:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a news category
        try:
            user_choice = input("Enter the number corresponding to the desired news category: ")
            selected_topic = topics[int(user_choice) - 1]
            news_category_url = f'https://www.bbc.com{selected_topic[2]}'

            # Replace 'your_link_class' with the actual class name for the links to other pages
            classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

            # Ask the user to input the statement for verification
            user_statement = input("Enter the statement to verify: ")

            # Scrape content and verify statement
            scrape_and_verify(user_statement, news_category_url, classes_to_check)

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid news category number.")


# In[15]:


import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = {}
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            scraped_data[class_name] = [element.get_text(strip=True) for element in elements]

    return scraped_data

def find_parent_link(element):
    # Traverse the ancestors to find an href
    current_element = element
    while current_element:
        if 'href' in current_element.attrs:
            return current_element['href']
        current_element = current_element.find_parent()

    return 'Link not found'

def compare_statement(user_statement, scraped_data, soup):
    matches = {}
    for class_name, data_list in scraped_data.items():
        for data in data_list:
            # Use fuzzy matching to handle typos or errors
            similarity_ratio = fuzz.token_set_ratio(user_statement.lower(), data.lower())
            if similarity_ratio > 90:  # Adjust the threshold as needed
                matches[class_name] = {
                    'context': data,
                    'similarity_ratio': similarity_ratio,
                    'parent_link': find_parent_link(soup.find(class_=class_name)),
                }

    return matches

def print_matched_results(matches):
    for class_name, match_info in matches.items():
        context = match_info['context']
        similarity_ratio = match_info['similarity_ratio']
        parent_link = match_info['parent_link']
        print(f"Context: {context} - Similarity: {similarity_ratio}% - Parent Link: {parent_link}")

def scrape_and_verify(user_statement, news_category_url, classes_to_check):
    # Make a request for the news category page
    news_category_response = requests.get(news_category_url)

    if news_category_response.status_code == 200:
        soup = BeautifulSoup(news_category_response.text, 'html.parser')

        # Scrape elements with specified classes
        scraped_data = scrape_with_classes(soup, classes_to_check)

        # Compare the user's statement with the scraped data
        matches = compare_statement(user_statement, scraped_data, soup)

        if matches:
            print("The following contexts were found:")
            print_matched_results(matches)
            print("Statement verified and legitimate!")
        else:
            print("No matching context found. The statement might not be legitimate.")

    else:
        print(f"Error: Unable to fetch news category page. Status code: {news_category_response.status_code}")

if __name__ == "__main__":
    # Get available news categories
    topics = get_bbc_news_topics()

    if not topics:
        print("No news categories found. Exiting.")
    else:
        # Display available news categories to the user
        print("Available news categories:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a news category
        try:
            user_choice = input("Enter the number corresponding to the desired news category: ")
            selected_topic = topics[int(user_choice) - 1]

            print(f"You selected: {selected_topic[1]} - URL: https://www.bbc.com{selected_topic[2]}")
            news_category_url = f'https://www.bbc.com{selected_topic[2]}'

            # Ask the user to enter a statement for verification
            user_statement = input("Enter the statement to verify: ")

            # Specify classes to check on the news pages
            classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

            # Scrape and verify the user's statement
            scrape_and_verify(user_statement, news_category_url, classes_to_check)

        except (ValueError, IndexError):
            print("Invalid choice.")


# In[14]:


import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = {}
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            scraped_data[class_name] = [element.get_text(strip=True) for element in elements]
    
    return scraped_data

def compare_statement(statement, scraped_data):
    matched_data = []
    for class_name, data_list in scraped_data.items():
        for data in data_list:
            ratio = fuzz.partial_ratio(statement.lower(), data.lower())
            if ratio >= 80:
                matched_data.append((class_name, data))
    
    return matched_data

if __name__ == "__main__":
    # Get available topics
    topics = get_bbc_news_topics()

    if not topics:
        print("No topics found. Exiting.")
    else:
        # Display available topics to the user
        print("Available topics:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a topic
        try:
            user_choice = input("Enter the number corresponding to the desired topic: ")
            selected_topic = topics[int(user_choice) - 1]

            print(f"You selected: {selected_topic[1]} - URL: https://www.bbc.com{selected_topic[2]}")
            topic_url = f'https://www.bbc.com{selected_topic[2]}'

            # Make a request for the topic page
            topic_response = requests.get(topic_url)

            if topic_response.status_code == 200:
                soup = BeautifulSoup(topic_response.text, 'html.parser')
                
                # Classes to check
                classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

                # Scrape elements with specified classes
                scraped_data = scrape_with_classes(soup, classes_to_check)

                # Ask the user to enter a statement for comparison
                user_statement = input("Enter the statement to verify: ")

                # Compare the user's statement with the scraped data
                matched_data = compare_statement(user_statement, scraped_data)

                if matched_data:
                    print("Matching contexts found:")
                    for match in matched_data:
                        class_name, data = match
                        parent_link = soup.find(class_=class_name).find_parent('a')['href']
                        print(f"Class: {class_name}, Data: {data}, Parent Link: https://www.bbc.com{parent_link}")
                else:
                    print("No matching context found. The statement might not be legitimate.")

            else:
                print(f"Error: Unable to fetch topic page. Status code: {topic_response.status_code}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid topic number.")


# In[18]:


import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = {}
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            scraped_data[class_name] = [element.get_text(strip=True) for element in elements]
    
    return scraped_data

def compare_statement(statement, scraped_data):
    matched_data = []
    for class_name, data_list in scraped_data.items():
        for data in data_list:
            ratio = fuzz.partial_ratio(statement.lower(), data.lower())
            if ratio >= 80:
                parent_link = soup.find(string=data).find_parent('a')['href']
                matched_data.append((f"https://www.bbc.com{parent_link}", data))
    
    return matched_data

if __name__ == "__main__":
    # Get available topics
    topics = get_bbc_news_topics()

    if not topics:
        print("No topics found. Exiting.")
    else:
        # Display available topics to the user
        print("Available topics:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a topic
        try:
            user_choice = input("Enter the number corresponding to the desired topic: ")
            selected_topic = topics[int(user_choice) - 1]

            print(f"You selected: {selected_topic[1]} - URL: https://www.bbc.com{selected_topic[2]}")
            topic_url = f'https://www.bbc.com{selected_topic[2]}'

            # Make a request for the topic page
            topic_response = requests.get(topic_url)

            if topic_response.status_code == 200:
                soup = BeautifulSoup(topic_response.text, 'html.parser')
                
                # Classes to check
                classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

                # Scrape elements with specified classes
                scraped_data = scrape_with_classes(soup, classes_to_check)

                # Ask the user to enter a statement for comparison
                user_statement = input("Enter the statement to verify: ")

                # Compare the user's statement with the scraped data
                matched_data = compare_statement(user_statement, scraped_data)

                if matched_data:
                    print("Matching contexts found:")
                    for link, data in matched_data:
                        print(f"Link: {link} - Matched: {data}")
                else:
                    print("No matching context found. The statement might not be legitimate.")

            else:
                print(f"Error: Unable to fetch topic page. Status code: {topic_response.status_code}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid topic number.")


# In[12]:


import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def get_bbc_news_topics():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []

        # Find topics under the 'News' section
        news_section = soup.find('a', {'href': '/news'})
        if news_section:
            topic_list = news_section.find_next('ul')
            if topic_list:
                topics = [(index + 1, topic.text, topic['href']) for index, topic in enumerate(topic_list.find_all('a'))]

        return topics

    else:
        print(f"Error: Unable to fetch topics. Status code: {response.status_code}")
        return []

def scrape_with_classes(soup, classes):
    scraped_data = {}
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        if elements:
            scraped_data[class_name] = [element.get_text(strip=True) for element in elements]

    return scraped_data

def compare_statement(statement, scraped_data, soup):
    matched_data = []
    for class_name, data_list in scraped_data.items():
        for data in data_list:
            ratio = fuzz.partial_ratio(statement.lower(), data.lower())
            if ratio >= 80:
                parent_link = soup.find(string=data).find_parent('a')
                if parent_link:
                    href = parent_link.get('href')
                    matched_data.append((f"https://www.bbc.com{href}", data))
    
    return matched_data

if __name__ == "__main__":
    # Get available topics
    topics = get_bbc_news_topics()

    if not topics:
        print("No topics found. Exiting.")
    else:
        # Display available topics to the user
        print("Available topics:")
        for topic in topics:
            print(f"{topic[0]}. {topic[1]} - URL: https://www.bbc.com{topic[2]}")

        # Ask the user to choose a topic
        try:
            user_choice = input("Enter the number corresponding to the desired topic: ")
            selected_topic = topics[int(user_choice) - 1]

            print(f"You selected: {selected_topic[1]} - URL: https://www.bbc.com{selected_topic[2]}")
            topic_url = f'https://www.bbc.com{selected_topic[2]}'

            # Make a request for the topic page
            topic_response = requests.get(topic_url)

            if topic_response.status_code == 200:
                soup = BeautifulSoup(topic_response.text, 'html.parser')
                
                # Classes to check
                classes_to_check = ["gclMev", "dEAAFJ", "czRLo", "jqwZKz", "kTrQIN", "dJMMNx", "crzIlm"]

                # Scrape elements with specified classes
                scraped_data = scrape_with_classes(soup, classes_to_check)

                # Ask the user to enter a statement for comparison
                user_statement = input("Enter the statement to verify: ")

                # Compare the user's statement with the scraped data
                matched_data = compare_statement(user_statement, scraped_data, soup)

                if matched_data:
                    print("Matching contexts found:")
                    for link, data in matched_data:
                        print(f"Link: {link} - Matched: {data}")
                else:
                    print("No matching context found. The statement might not be legitimate.")

            else:
                print(f"Error: Unable to fetch topic page. Status code: {topic_response.status_code}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid topic number.")


# In[ ]:




