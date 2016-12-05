import Tkinter as tk
from Tkinter import *
import sqlite3
import os
from csv import reader



os.chdir("C:\Users\Brian\SQLiteDBs")
conn = sqlite3.connect("showDB.sqlite")
cur = conn.cursor()


class App(tk.Tk):

    r_query = []
    formatted_episode_array = []

    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, EditPage, ResultPage, EpisodesPage, DetailsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def get_page(self, page_class):
        return self.frames[page_class]

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if page_name == "ResultPage":
            self.show_query(HomePage.ste.get())
        elif page_name == "EpisodesPage":
            self.episode_query(HomePage.ste.get())
        elif page_name == "DetailsPage":
            self.detail_query()
        frame = self.frames[page_name]
        frame.tkraise()

    def show_query(self, show_title):
        cur.execute('SELECT ShowTable.name,Network.networkName FROM ShowTable,Network WHERE name = '
                    + '\'' + show_title + '\'' + 'AND ShowTable.network_id = Network.id')
        raw_string = str(cur.fetchone())
        formatted_string = raw_string.replace('(u' + '\'' + show_title + '\'', show_title)
        formatted_string = formatted_string.replace('u' + '\'', "")
        formatted_string = formatted_string.replace('\'' + ',', "")
        formatted_string = formatted_string.replace('\'' + ')', "")
        formatted_array = formatted_string.split(",")

        ResultPage.result_title.set(formatted_array[0])
        ResultPage.result_network.set(formatted_array[1])

    def episode_query(self, show_title):
        cur.execute('SELECT EpisodeTable.season,EpisodeTable.episode,EpisodeTable.name FROM EpisodeTable,ShowTable '
                    'WHERE ShowTable.name = ' + '\'' + show_title + '\'' + 'AND ShowTable.id = EpisodeTable.show_id')
        tuple_array = cur.fetchall()

        string = ""
        two_d_array = [list(elem) for elem in tuple_array]

        for i in range(0, len(two_d_array)):
            two_d_array[i][2] = two_d_array[i][2].encode('utf-8')
            string += two_d_array[i][2]
            self.get_page("EpisodesPage").list_box.insert(i, two_d_array[i][2])
            print two_d_array[i][2]

    def detail_query(self):
        print self.get_page("EpisodesPage").list_box.get(ACTIVE)

        cur.execute('SELECT EpisodeTable.name,EpisodeTable.airDate,EpisodeTable.season,EpisodeTable.episode,'
                    'EpisodeTable.summary FROM EpisodeTable WHERE EpisodeTable.name = ' + '\'' + self.get_page("EpisodesPage").list_box.get(ACTIVE) + '\'')

        tuple_array = cur.fetchone()
        array = [elem for elem in tuple_array]
        print array

        array[4] = array[4].replace("<p>", "")
        array[4] = array[4].replace("</p>", "")

        DetailsPage.episode_title.set("Episode Title: " + array[0])
        DetailsPage.air_date.set("Air Date: " + array[1])
        DetailsPage.season.set("Season: " + str(array[2]))
        DetailsPage.episode_num.set("Episode Number: " + str(array[3]))
        DetailsPage.summary.set("Summary: " + array[4])


class HomePage(tk.Frame):
    ste = ""

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="TV APP").pack()
        Label(self, text="Title:").pack()

        HomePage.ste = StringVar()
        HomePage.ste.set("Futurama")
        Entry(self, textvariable=HomePage.ste).pack(fill="x")

        Button(self, text="Search", fg="white", bg="green", command=lambda: controller.show_frame("ResultPage")).pack()

        Button(self, text="Insert Page", command=lambda: controller.show_frame("EditPage")).pack()


class EditPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Insert/Delete a show").pack()
        editShowLabel = Entry(self).pack(fill="x")

        insertButton = Button(self, text="Insert", fg="white", bg="green").pack()
        deleteButton = Button(self, text="Delete", fg="white", bg="red").pack()

        homeButton = Button(self, text="Home", command=lambda: controller.show_frame("HomePage")).pack(side=BOTTOM)


class ResultPage(tk.Frame):

    result_title = ""
    result_network = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Result:").pack()

        ResultPage.result_title = StringVar()
        Label(self, text="Title:")
        ResultPage.result_label = Label(self, textvariable=ResultPage.result_title).pack()

        ResultPage.result_network = StringVar()
        Label(self, text="Network:").pack()
        Label(self, textvariable=ResultPage.result_network).pack()

        Button(self, text="Episodes", command=lambda: controller.show_frame("EpisodesPage")).pack()
        Button(self, text="Home", command=lambda: controller.show_frame("HomePage")).pack(side=BOTTOM)


class EpisodesPage(tk.Frame):

    episode_info = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Episodes:").pack()

        self.list_box = Listbox(self)
        self.list_box.pack(fill="x")

        Button(self, text="Details", command=lambda: controller.show_frame("DetailsPage")).pack(side=BOTTOM)
        Button(self, text="Home", command=lambda: controller.show_frame("HomePage")).pack(side=BOTTOM)


class DetailsPage(tk.Frame):

    episode_title = "Episode Title: "
    air_date = "Air Date: "
    season = "Season: "
    episode_num = "Episode Number: "
    summary = "Summary: "

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Details:").grid(row=0, column=0)

        DetailsPage.episode_title = StringVar()
        Label(self, textvariable=DetailsPage.episode_title).grid(row=1, column=0)

        DetailsPage.season = StringVar()
        Label(self, textvariable=DetailsPage.season).grid(row=2, column=0)

        DetailsPage.episode_num = StringVar()
        Label(self, textvariable=DetailsPage.episode_num).grid(row=3, column=0)

        DetailsPage.air_date = StringVar()
        Label(self, textvariable=DetailsPage.air_date).grid(row=4, column=0)

        DetailsPage.season = StringVar()
        Label(self, textvariable=DetailsPage.summary).grid(row=5, column=0)

        DetailsPage.summary = StringVar()
        Label(self, textvariable=DetailsPage.summary).grid(row=6, column=0)

        Button(self, text="Back", command=lambda: controller.show_frame("EpisodesPage")).grid(row=7, column=0)
        Button(self, text="Home", command=lambda: controller.show_frame("HomePage")).grid(row=7, column=1)


run = App()
run.mainloop()
