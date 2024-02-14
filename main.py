import tkinter
import customtkinter
import requests
from bs4 import BeautifulSoup


# Search Term
# AllField=%28"Transtheoretical+Model"+OR+"Behavioral+Change"%29+AND+%28"chatbot"+OR+"virtual+assistant"+OR+"Virtual+Agents"+OR+"Conversational+Agent"%29&startPage=0&pageSize=20

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # System Settings
        self._set_appearance_mode("System")
        self.title("ACM Article Scraper")
        self.geometry("600x400")
        self.minsize(600, 400)

        searchTerm = tkinter.StringVar()
        self.searchTermTitle = customtkinter.CTkLabel(master=self, text="Insert Search Term")
        self.searchTermLink = customtkinter.CTkEntry(master=self, width=350, height=40, textvariable=searchTerm)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.searchTermTitle.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.searchTermLink.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        self.combobox = customtkinter.CTkComboBox(master=self, values=["10", "20", "30", "40", "50"])
        self.combobox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(master=self, command=self.start_article_scrape, text="Fetch Articles")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

    def start_article_scrape(self):
        searchTerm = self.searchTermLink.get()
        numberOfArticles = self.combobox.get()
        self.scrape_article_links(searchTerm, numberOfArticles)
    
    def button_callback(self):
        self.textbox.insert("insert", self.combobox.get() + "\n")

    def scrape_article_links(self, searchTerm, number_of_articles):
        url = f'https://dl.acm.org/action/doSearch?AllField={searchTerm}&startPage=0&pageSize={number_of_articles}'
        response = requests.get(url)

        try:
            if response.status_code == 200:
                scrape = BeautifulSoup(response.text, 'html.parser')

                articleTitles = scrape.find_all('span', class_='hlFld-Title')
                totalArticles = len(articleTitles)

                with open('OUTPUT/list_of_articles.txt', 'w', encoding='utf-8') as file:
                    for i, title in enumerate(articleTitles, 1):
                        articleLink = title.find('a')

                        if articleLink:
                            link = articleLink.get('href')
                            article_info = f"Title: {title.text}, Link: {'https://dl.acm.org/' + link}\n"
                            print(article_info)
                            file.write(article_info)

                        # Calculate progress percentage
                        progress_percentage = (i / totalArticles) * 100

                        # Print dynamic progress update using carriage return
                        print(f"Progress: {progress_percentage:.2f}%", end='\r')
                    
                    self.search_statistics()
                
        except:
            print("Could not perform scrape")

    def search_statistics(self):
        statisticsOutputHeader = "* RESULTS FROM ACM DIGITAL LIBRARY *" + "\n"
        articlesSearched = "Number of Articles Searched: " + self.combobox.get()
        searchTermUsed = "Search Term Used: " + self.searchTermLink.get()
        outputDirectory = "Directory Output for TextFile: " + "OUTPUT/list_of_articles.txt"
        
        self.textbox.insert("insert", statisticsOutputHeader + "\n")
        self.textbox.insert("insert", articlesSearched + "\n")
        self.textbox.insert("insert", searchTermUsed + "\n")
        self.textbox.insert("insert", outputDirectory + "\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()