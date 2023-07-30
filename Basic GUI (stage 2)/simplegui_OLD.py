class GUI(UI):

    def __init__(self):
        super().__init__()
        self.__UI_type = "GRAPHICAL"

        self.__root = self.__setup_root()

        self.__setup_home_page()

        self.__home_page.tkraise()

        self.__board_img = PhotoImage(file="board_img.png")

        # self.__root.attributes('-fullscreen', True)

    def get_UI_type(self):
        return self.__UI_type
    
    def __setup_root(self):
        root = Tk()
        root.title("Surakarta")
        root.geometry("800x600")

        # root.resizable(False, False)
        return root
    
    def __setup_home_page(self):

        home_page = Frame(self.__root, bg="RoyalBlue1")
        home_page.pack(side="top", fill="both", expand=True)

        home_page.pack_propagate(False)

        title_frame = Frame(home_page, bg="RoyalBlue1")
        title_frame.pack(side="top")
        title = Label(title_frame, text="Surakarta", font=("Helvetica", 50), pady=20, bg="RoyalBlue1", fg="yellow")
        title.pack()

        col1_buttons_frame = Frame(home_page, bg="RoyalBlue1")
        col1_buttons_frame.pack(side="left", expand=True, fill="both")

        col2_buttons_frame = Frame(home_page, bg="RoyalBlue1")
        col2_buttons_frame.pack(side="right", expand=True, fill="both")

        col1_button_names = ["New Game", "Login", "Help"]
        col2_button_names = ["Load Game", "Sign Up", "Quit"]

        for i,name in enumerate(col1_button_names):
            button = Button(col1_buttons_frame, text=name, bg="blue4", fg="yellow", font=("Helvetica", 20), width=20,)
            button.grid(row=i+1, column=0, pady=10, padx=10)

        for i,name in enumerate(col2_button_names):
            button = Button(col2_buttons_frame, text=name, bg="blue4", fg="yellow", font=("Helvetica", 20), width=20,)
            button.grid(row=i+1, column=1, padx=10, pady=10)


        self.__home_page = home_page

    def __make_home_page_button(self, text, parent):
        button = Button(parent, text=text, bg="blue4", fg="yellow", font=("Helvetica", 20), width=10)
        return button

    def run_GUI(self):

        self.__root.mainloop() 


ui = GUI()
ui.run_GUI()









