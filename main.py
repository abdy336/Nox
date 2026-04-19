import os
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

# Arka Plan: Tam Siyah
Window.clearcolor = (0.01, 0.01, 0.01, 1)

# --- YARDIMCI BİLEŞEN ---
class NoxKart(ButtonBehavior, BoxLayout):
    def __init__(self, ad, resim_yolu, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = Window.width / 2 / 1.77 + 45 
        if os.path.exists(resim_yolu):
            self.img = Image(source=resim_yolu, allow_stretch=True, keep_ratio=False, size_hint_y=0.78)
        else:
            self.img = Label(text="NOX", size_hint_y=0.78, color=(0.12, 0.12, 0.12, 1), bold=True)
        self.add_widget(self.img)
        self.add_widget(Label(text=ad, size_hint_y=0.22, bold=True, font_size='14sp', color=(0.8, 0.8, 0.8, 1)))

# --- EKRANLAR ---

class EsasyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[10, 5, 10, 5])
        ust_bar = BoxLayout(size_hint_y=None, height='60dp', orientation='horizontal', spacing=10, padding=[0, 5])
        
        if os.path.exists("nox_logo.png"):
            logo_img = Image(source="nox_logo.png", size_hint=(None, 1), width='100dp', allow_stretch=True, keep_ratio=True)
            ust_bar.add_widget(logo_img)
        else:
            ust_bar.add_widget(Label(text="[color=BF00FF]NOX[/color]", markup=True, font_size='24sp', bold=True, size_hint_x=None, width='70dp'))
        
        arama = TextInput(hint_text='Gözleg...', hint_text_color=(0.5, 0.5, 0.5, 1), multiline=False, size_hint=(1, None), height='40dp', pos_hint={'center_y': 0.5}, background_normal='', background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1), padding=[15, 10], cursor_color=(0.7, 0, 1, 1))
        ust_bar.add_widget(arama)
        layout.add_widget(ust_bar)
        
        scroll = ScrollView(do_scroll_x=False)
        grid = GridLayout(cols=2, spacing=15, size_hint_y=None, padding=[0, 10, 0, 10])
        grid.bind(minimum_height=grid.setter('height'))
        
        # TÜM KATEGORİLER BURADA
        kategoriler = [
            ("Filmler", "Filmler.jpeg"), ("Seriallar", "Seriallar.jpeg"), 
            ("Sport", "Sport.jpeg"), ("Aýdym-saz", "Aýdym-saz.jpeg"), 
            ("Karaoke", "karaoke.jpeg"), ("Multfilmler", "Multfilmler.jpeg"), 
            ("Anime", "Anime.jpeg"), ("Dokumental", "Dokumental.jpeg")
        ]
        for ad, resim in kategoriler:
            grid.add_widget(NoxKart(ad=ad, resim_yolu=resim))
            
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

class ShortsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Henüz bir şey yok", font_size='18sp', color=(0.4, 0.4, 0.4, 1)))

class ProfilMain(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[40, 50, 40, 50], spacing=20)
        layout.add_widget(Label(text="Profil", font_size='32sp', bold=True, size_hint_y=None, height='80dp', color=(0.7, 0, 1, 1)))
        
        btn_giris = Button(text="Hasaba gir", size_hint_y=None, height='55dp', background_normal='', background_color=(0.5, 0, 0.8, 1), color=(1, 1, 1, 1), bold=True)
        btn_giris.bind(on_release=self.git_giris)
        
        btn_kayit = Button(text="Hasap döret", size_hint_y=None, height='55dp', background_normal='', background_color=(0.15, 0.15, 0.15, 1), color=(0.8, 0.8, 0.8, 1), bold=True)
        btn_kayit.bind(on_release=self.git_giris)
        
        layout.add_widget(btn_giris)
        layout.add_widget(btn_kayit)
        layout.add_widget(Label())
        self.add_widget(layout)

    def git_giris(self, instance):
        self.manager.current = 'giris_yap'

class GirisYap(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[40, 50, 40, 50], spacing=20)
        layout.add_widget(Label(text="Giriş", font_size='32sp', bold=True, size_hint_y=None, height='80dp', color=(0.7, 0, 1, 1)))
        
        self.tel_input = TextInput(text='+993', font_size='18sp', multiline=False, size_hint_y=None, height='50dp', background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0.7, 0, 1, 1), padding=[10, 12])
        layout.add_widget(self.tel_input)
        
        btn_devam = Button(text="Dowam et", size_hint_y=None, height='55dp', background_normal='', background_color=(0.5, 0, 0.8, 1), color=(1, 1, 1, 1), bold=True)
        btn_devam.bind(on_release=self.kontrol)
        layout.add_widget(btn_devam)
        
        btn_yza = Button(text="Yza dön", size_hint_y=None, height='40dp', background_normal='', background_color=(0,0,0,0), color=(0.5, 0.5, 0.5, 1))
        btn_yza.bind(on_release=lambda x: setattr(self.manager, 'current', 'profil_main'))
        layout.add_widget(btn_yza)
        layout.add_widget(Label())
        self.add_widget(layout)

    def kontrol(self, instance):
        if self.tel_input.text == "+99361965496":
            self.manager.current = 'profil_oz'
        else:
            self.tel_input.text = "+993"
            self.tel_input.hint_text = "Nätanyş belgi!"

class ProfilOz(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[40, 50, 40, 50], spacing=20)
        layout.add_widget(Label(text="👤", font_size='80sp', size_hint_y=None, height='100dp'))
        layout.add_widget(Label(text="Abdyrahman Gullyyew", font_size='24sp', bold=True, color=(1, 1, 1, 1)))
        layout.add_widget(Label(text="+993 61 965496", font_size='16sp', color=(0.6, 0.6, 0.6, 1)))
        
        btn_cikis = Button(text="Hasapdan çyk", size_hint_y=None, height='50dp', background_normal='', background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        btn_cikis.bind(on_release=lambda x: setattr(self.manager, 'current', 'profil_main'))
        layout.add_widget(btn_cikis)
        layout.add_widget(Label())
        self.add_widget(layout)

# --- ANA UYGULAMA ---

class NoxPlayer(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(EsasyScreen(name='esasy'))
        self.sm.add_widget(ShortsScreen(name='shorts'))
        self.sm.add_widget(ProfilMain(name='profil_main'))
        self.sm.add_widget(GirisYap(name='giris_yap'))
        self.sm.add_widget(ProfilOz(name='profil_oz'))
        
        self.main_layout.add_widget(self.sm)
        
        self.alt_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing=2)
        self.nav_buttons = {}
        for metin, ekran_adi in [("Esasy", 'esasy'), ("Shorts", 'shorts'), ("Profil", 'profil_main')]:
            btn = Button(text=metin, font_size='12sp', background_normal='', background_color=(0.05, 0.05, 0.05, 1), color=(0.5, 0.5, 0.5, 1), bold=True)
            btn.bind(on_release=lambda x, name=ekran_adi: self.degistir(name))
            self.nav_buttons[ekran_adi] = btn
            self.alt_bar.add_widget(btn)
        
        self.nav_buttons['esasy'].color = (0.7, 0, 1, 1) 
        self.main_layout.add_widget(self.alt_bar)
        return self.main_layout

    def degistir(self, name):
        self.sm.current = name
        for ekran, btn in self.nav_buttons.items():
            btn.color = (0.7, 0, 1, 1) if ekran == name else (0.5, 0.5, 0.5, 1)

if __name__ == "__main__":
    NoxPlayer().run()
