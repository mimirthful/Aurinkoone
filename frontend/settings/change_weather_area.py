import wx
from pubsub import pub

district_list = ["Aakkula", "Aitoniemi", "Amuri", "Annala", "Atala",
                 "Epilä", "Epilänharju", "Finlayson", "Haihara", "Hakametsä",
                 "Hallila", "Hankkio", "Hatanpää", "Haukiluoma", "Hervanta",
                 "Hervantajärvi", "Hiedanranta", "Holvasti", "Huikas", "Hyhky",
                 "Härmälä", "Ikuri", "Jokipohja", "Jussinkylä", "Järvensivu",
                 "Kaakinmaa", "Kaarila", "Kaleva", "Kalevanharju", "Kalevanrinne",
                 "Kalkku", "Kaukajärvi", "Kauppi", "Kissanmaa", "Koivistonkylä",
                 "Korkinmäki", "Kumpula", "Kyttälä", "Kämmenniemi", "Lahdesjärvi",
                 "Lakalaiva", "Lamminpää", "Lapinniemi", "Lappi", "Leinola", "Lentävänniemi",
                 "Lielahti", "Liisankallio", "Linnainmaa", "Lintulampi", "Lukonmäki", "Messukylä",
                 "Multisilta", "Muotiala", "Myllypuro", "Nalkala", "Nekala", "Niemenranta", "Niemi",
                 "Niihama", "Nirva", "Nurmi", "Ojala", "Olkahinen", "Osmonmäki", "Pappila", "Peltolammi",
                 "Petsamo", "Pispala", "Pohtola", "Polso", "Pyynikinrinne", "Pyynikki", "Rahola", "Rantaperkiö",
                 "Ratina", "Rautaharkko", "Ristimäki", "Ristinarkku", "Ruotula", "Rusko", "Ryydynpohja", "Santalahti",
                 "Sarankulma", "Sorila", "Särkänniemi", "Taatala", "Tahmela", "Takahuhti", "Tammela", "Tammerkoski",
                 "Tampella", "Tasanne", "Terälahti", "Tesomajärvi", "Tohloppi", "Tulli", "Turtola", "Uusikylä",
                 "Vehmainen", "Veisu", "Velaatta", "Vihioja", "Viiala", "Viinikka", "Viitapohja", "Villilä",
                 "Vuohenoja", "Vuores",]


class ChangeWeatherAreaWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.choice = None
        self.text = wx.StaticText(self, label="Weather area")
        self.choicebox = wx.Choice(self, choices=district_list)
        self.choicebox.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.button = wx.Button(self, label="Send")
        self.Bind(wx.EVT_BUTTON, self.on_click, source=self.button)
        self.sizer.AddMany(((self.text, 1, wx.ALL, 5), (self.choicebox, 1, wx.ALL, 5),
                           (self.button, 1, wx.ALL, 5)))

    def OnChoice(self, event):
        self.choice = self.choicebox.GetString(self.choicebox.GetSelection())

    def on_click(self, evt):
        if self.choice:
            pub.sendMessage("weather_area_changed",
                            district=self.choice.strip())
