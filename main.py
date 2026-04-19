import os
import webbrowser # Linki dışarıda açmak için
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Color, Ellipse, StencilPush, StencilUse, StencilUnUse, StencilPop, Rectangle

# Arka Plan
Window.clearcolor = (0, 0, 0, 1)

class RoundImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = False
        self.bind(pos=self._update_canvas, size=self._update_canvas)
    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            StencilPush()
            Ellipse(pos=self.pos, size=self.size)
            StencilUse()
        self.canvas.after.clear()
        with self.canvas.after:
            StencilUnUse()
            Ellipse(pos=self.pos, size=self.size)
            StencilPop()

class NoxKart(ButtonBehavior, BoxLayout):
    def __init__(self, ad, resim_yolu, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        card_width = (Window.width - 35) / 2
        self.height = (card_width / 1.77) + 40 
        self.ad = ad
        self.img = Image(source=resim_yolu if os.path.exists(resim_yolu) else "", allow_stretch=True, keep_ratio=False, size_hint_y=0.8)
        self.add_widget(self.img)
        self.add_widget(Label(text=ad, size_hint_y=0.2, bold=True, font_size='13sp', color=(0.8, 0.8, 0.8, 1)))
        self.bind(on_release=self.git)

    def git(self, instance):
        app = App.get_running_app()
        app.sm.get_screen('kategori_detay').ids['baslik'].text = self.ad
        app.sm.current = 'kategori_detay'

class NavButton(ButtonBehavior, BoxLayout):
    def __init__(self, icon_path, target_name, is_round=False, **kwargs):
        super().__init__(**kwargs)
        self.target_name = target_name
        self.orientation = 'vertical'
        self.size_hint_x = 1
        self.padding = [0, 12]
        self.icon = RoundImage(source=icon_path) if is_round else Image(source=icon_path, allow_stretch=True, keep_ratio=True)
        self.icon.size_hint = (None, None)
        self.icon.size = ('42dp', '42dp')
        self.icon.pos_hint = {'center_x': 0.5}
        self.add_widget(self.icon)
        self.bind(on_release=self.navigate)

    def navigate(self, instance):
        App.get_running_app().sm.current = self.target_name

class EsasyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = BoxLayout(orientation='vertical', padding=[10, 5, 10, 5])
        u = BoxLayout(size_hint_y=None, height='60dp', spacing=10, padding=[0, 5])
        u.add_widget(Label(text="[color=BF00FF]NOX[/color]", markup=True, font_size='26sp', bold=True, size_hint_x=None, width='80dp'))
        u.add_widget(TextInput(hint_text='Gözleg...', multiline=False, size_hint=(1, None), height='40dp', pos_hint={'center_y': 0.5}, background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1)))
        l.add_widget(u)
        s = ScrollView()
        g = GridLayout(cols=2, spacing=12, size_hint_y=None, padding=[0, 10]); g.bind(minimum_height=g.setter('height'))
        
        # TÜM KATEGORİLER (Eksiksiz Liste)
        kategoriler = [
            ("Filmler", "Filmler.jpeg"), ("Seriallar", "Seriallar.jpeg"), 
            ("Sport", "Sport.jpeg"), ("Aýdym-saz", "Aýdym-saz.jpeg"), 
            ("Karaoke", "karaoke.jpeg"), ("Multfilmler", "Multfilmler.jpeg"), 
            ("Anime", "Anime.jpeg"), ("Dokumental", "Dokumental.jpeg")
        ]
        
        for ad, res in kategoriler:
            g.add_widget(NoxKart(ad, res))
        s.add_widget(g); l.add_widget(s); self.add_widget(l)

class ShortsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = BoxLayout(orientation='vertical', padding=30, spacing=20)
        l.add_widget(Label(text="Hızlı Video Oynatıcı", font_size='22sp', bold=True, size_hint_y=None, height='50dp'))
        
        self.url_input = TextInput(hint_text="Video linkini buraya yapıştırın...", multiline=False, size_hint_y=None, height='55dp', background_color=(0.1,0.1,0.1,1), foreground_color=(1,1,1,1), padding=[10, 15])
        
        btn = Button(text="OYNATMAYI BAŞLAT", size_hint_y=None, height='60dp', background_color=(0.5, 0, 0.8, 1), bold=True)
        btn.bind(on_release=self.disarida_oynat)
        
        bilgi = Label(text="Not: Linki yapıştırıp butona bastığınızda\nvideonuz VLC veya Tarayıcıda açılır.", halign='center', color=(0.5, 0.5, 0.5, 1))
        
        l.add_widget(self.url_input)
        l.add_widget(btn)
        l.add_widget(bilgi)
        l.add_widget(Label()) # Boşluk
        self.add_widget(l)

    def disarida_oynat(self, instance):
        url = self.url_input.text.strip()
        if url.startswith("http"):
            # Bu komut linki sistemin varsayılan oynatıcısında açar
            webbrowser.open(url)
        else:
            self.url_input.text = ""
            self.url_input.hint_text = "Lütfen geçerli bir http linki girin!"

class KategoriDetay(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.ids['baslik'] = Label(text="", font_size='28sp', bold=True, color=(0.7, 0, 1, 1), size_hint_y=None, height='60dp')
        l.add_widget(self.ids['baslik'])
        l.add_widget(Label(text="🎬", font_size='60sp'))
        l.add_widget(Label(text="Bu kategoriýa ýakynda\ntäze wideolar goşular!", halign='center', color=(0.7,0.7,0.7,1)))
        b = Button(text="Yza dön", size_hint_y=None, height='50dp', background_color=(0.2, 0.2, 0.2, 1))
        b.bind(on_release=lambda x: setattr(self.manager, 'current', 'esasy'))
        l.add_widget(b); self.add_widget(l)

class ProfilOz(Screen):
    def on_enter(self):
        self.clear_widgets()
        l = BoxLayout(orientation='vertical', padding=30, spacing=20)
        u = BoxLayout(orientation='horizontal', size_hint_y=None, height='120dp', spacing=20)
        u.add_widget(RoundImage(source="profile.jpeg") if os.path.exists("profile.jpeg") else Label(text="👤", font_size='80sp'))
        u.add_widget(Label(text="Abdyrahman\nGullyyew", font_size='20sp', bold=True))
        l.add_widget(u); l.add_widget(Label()); self.add_widget(l)

class NoxPlayer(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(EsasyScreen(name='esasy'))
        self.sm.add_widget(KategoriDetay(name='kategori_detay'))
        self.sm.add_widget(ShortsScreen(name='shorts'))
        self.sm.add_widget(ProfilOz(name='profil_oz'))
        self.root.add_widget(self.sm)
        alt = BoxLayout(orientation='horizontal', size_hint_y=None, height='75dp')
        alt.add_widget(NavButton('Esasy.jpeg', 'esasy'))
        alt.add_widget(NavButton('shorts.png', 'shorts'))
        alt.add_widget(NavButton('profile.jpeg', 'profil_oz', True))
        self.root.add_widget(alt)
        return self.root

if __name__ == "__main__":
    NoxPlayer().run()
  
