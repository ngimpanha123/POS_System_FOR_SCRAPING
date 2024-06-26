import requests
from bs4 import BeautifulSoup
import pandas as pd
# ==========================
def scraper(path):
    url = 'https://data.adb.org/search/content/type/dataset/type/dataset/topics/economics-135'
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response,'html.parser')

    # ==========================
    links = []
    list1 = [2]
    for i in list1: # there exist 2 pages of data
        url = f"https://data.adb.org/search/content/type/dataset/type/dataset/topics/economics-135?page={i}"
        response = requests.get(url)
        response = response.content
        soup = BeautifulSoup(response, 'html.parser')
        ol = soup.find("div",class_="view-content")

        for link in ol.find_all("a", href=True):
              links.append(link['href'])

    # ============================
    link = ['https://data.adb.org/'+ data for data in links]
    # ============================
    download_links = []
    for lis in link:
      response = requests.get(lis)
      response = response.content
      soups = BeautifulSoup(response,'html.parser')
      ols = soups.find("div",class_="col-md-9")

      # if link in ols.find('div',class_='ml-30'):
      for link in ols.find_all("a", href=True):
        download_links.append(link['href'])
    download_links = [elem for elem in download_links if "/media/" in elem]
    download_links = ['https://data.adb.org/' + elem for elem in download_links]
    # =================================
    df =pd.DataFrame({'links':download_links})
    # ==================================
    data = df.to_excel(path+'\\'+'download_links.xlsx')
    df = pd.read_excel(path+'\\'+'download_links.xlsx')
    df.drop_duplicates()
    df.to_excel(path+'\\'+'download_links2.xlsx')
# =================================
    import os
    # Read the DataFrame from the Excel file
    links_df = pd.read_excel(path+'\\'+'download_links2.xlsx')

    # Specify the folder where you want to save the files
    download_folder = path

    # Create the folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Download files
    for index, row in links_df.iterrows():
        url = row['links']
        response = requests.get(url)

        # Define a filename pattern based on index or any other identifier
        file_name = os.path.join(download_folder, f"file_{index}.xlsx")

        with open(file_name, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded: {file_name}")

    print("All files downloaded successfully.")