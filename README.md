alfaCRM site scraper, for collecting data such as data on current and archived clients, financial transactions, groups. The scripts are written in python3.9.11, using the selenium webdriver framework, libraries: pandas, pygsheets. 
The algorithm of our parser is as follows: 
1) login to the site, under a specific username and password via webdriver Firefox
2) finding the necessary category (let's say current customers)
3) passing through the pages of the category in turn -> collecting data from each page in the form of a Pandas Dataframe -> bringing the dataframe to the required form
4) saving the data frame to a json file
5) uploading data to google sheets using pygsheets, GoogleAPI

All actions take place in main.py where you call the required function.
