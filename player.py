import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import vlc
from pygame import mixer
import random

class CyberpunkPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberFlux Player")
        self.root.geometry("1000x600")
        self.root.configure(bg="#0a0a12")
        
        # Couleurs cyberpunk
        self.bg_color = "#0a0a12"
        self.primary_color = "#00f0ff"  # Bleu-cyan fluo
        self.secondary_color = "#ff00ff"  # Rose fluo
        self.text_color = "#ffffff"
        self.highlight_color = "#00ffaa"
        
        # Initialisation VLC avec des paramètres supplémentaires
        vlc_args = [
            '--no-xlib', 
            '--avcodec-hw=any',
            '--avcodec-fast',
            '--drop-late-frames',
            '--skip-frames'
        ]
        self.instance = vlc.Instance(vlc_args)
        self.player = self.instance.media_player_new()
        
        # Initialisation mixer pour les effets sonores
        mixer.init()
        
        # Variables
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.volume = 70
        self.player.audio_set_volume(self.volume)
        
        # Charger une police futuriste
        self.font_large = ("Courier New", 16, "bold")
        self.font_medium = ("Courier New", 12)
        self.font_small = ("Courier New", 10)
        
        # Création de l'interface
        self.create_widgets()
        self.create_menu()
        
        # Effet de scanlines
        self.scanline_canvas = tk.Canvas(root, bg=self.bg_color, highlightthickness=0)
        self.scanline_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.draw_scanlines()
        
        # Mettre les autres widgets au premier plan
        self.bring_widgets_to_front()
        
        # Animation de lueurs
        self.glow_animation()
        
    def bring_widgets_to_front(self):
        """Met tous les widgets au premier plan par rapport aux scanlines"""
        for child in self.root.winfo_children():
            if child != self.scanline_canvas:
                child.lift()
    
    def draw_scanlines(self):
        """Dessine des lignes de scan pour un effet rétro"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        self.scanline_canvas.delete("scanline")
        
        for y in range(0, height, 4):
            self.scanline_canvas.create_line(
                0, y, width, y,
                fill=self.primary_color,
                tags="scanline",
                width=1
            )
    
    def glow_animation(self):
        """Animation de lueurs cyberpunk"""
        colors = [self.primary_color, self.secondary_color, self.highlight_color]
        widgets = [
            self.play_button, self.pause_button, self.stop_button,
            self.prev_button, self.next_button, self.volume_slider
        ]
        
        for widget in widgets:
            current_color = random.choice(colors)
            widget.config(highlightbackground=current_color)
            widget.config(highlightcolor=current_color)
            widget.config(highlightthickness=1)
        
        self.root.after(3000, self.glow_animation)
    
    def create_menu(self):
        """Crée le menu principal"""
        menubar = tk.Menu(self.root, bg=self.bg_color, fg=self.text_color, 
                          activebackground=self.primary_color, activeforeground="#000000")
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_color, fg=self.text_color,
                            activebackground=self.primary_color)
        file_menu.add_command(label="Ouvrir une playlist", command=self.load_playlist)
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_color, fg=self.text_color,
                           activebackground=self.primary_color)
        help_menu.add_command(label="À propos", command=self.show_about)
        help_menu.add_command(label="Dépannage", command=self.show_troubleshooting)
        menubar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        messagebox.showinfo("À propos", "CyberFlux Player\n\nLecteur M3U/M3U8 Cyberpunk\nVersion 1.0")
    
    def show_troubleshooting(self):
        """Affiche des conseils de dépannage"""
        tips = """Problèmes de lecture courants :

1. Assurez-vous que VLC est bien installé sur votre système
2. Installez les codecs nécessaires :
   - sudo apt-get install ubuntu-restricted-extras (Ubuntu)
   - sudo pacman -S gst-libav (Arch)
3. Essayez des flux différents
4. Vérifiez votre connexion Internet pour les streams
5. Redémarrez l'application"""
        messagebox.showinfo("Dépannage", tips)
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Frame principale
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame pour les contrôles
        control_frame = tk.Frame(main_frame, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Boutons de contrôle
        button_style = {
            "bg": self.bg_color,
            "fg": self.text_color,
            "activebackground": self.primary_color,
            "activeforeground": "#000000",
            "borderwidth": 2,
            "relief": tk.RAISED,
            "font": self.font_medium,
            "padx": 10,
            "pady": 5
        }
        
        self.play_button = tk.Button(control_frame, text="▶ PLAY", 
                                    command=self.play, **button_style)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(control_frame, text="⏸ PAUSE", 
                                     command=self.pause, **button_style)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(control_frame, text="⏹ STOP", 
                                    command=self.stop, **button_style)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.prev_button = tk.Button(control_frame, text="⏮ PRÉC", 
                                    command=self.prev_track, **button_style)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = tk.Button(control_frame, text="⏭ SUIV", 
                                    command=self.next_track, **button_style)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Slider de volume
        volume_frame = tk.Frame(control_frame, bg=self.bg_color)
        volume_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(volume_frame, text="VOLUME:", bg=self.bg_color, 
                fg=self.primary_color, font=self.font_medium).pack(side=tk.LEFT)
        
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, 
                                     orient=tk.HORIZONTAL, command=self.set_volume,
                                     bg=self.bg_color, fg=self.text_color,
                                     highlightthickness=0, troughcolor="#1a1a2e",
                                     activebackground=self.secondary_color,
                                     font=self.font_small)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(side=tk.LEFT)
        
        # Affichage du morceau en cours
        self.current_track_label = tk.Label(main_frame, text="Aucun morceau sélectionné", 
                                           bg=self.bg_color, fg=self.primary_color,
                                           font=self.font_large)
        self.current_track_label.pack(pady=(0, 10))
        
        # Liste de lecture
        playlist_frame = tk.Frame(main_frame, bg=self.bg_color)
        playlist_frame.pack(fill=tk.BOTH, expand=True)
        
        self.playlist_tree = ttk.Treeview(playlist_frame, columns=("title", "duration"), 
                                         selectmode="browse")
        
        # Style personnalisé pour le Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#1a1a2e", 
                       foreground=self.text_color,
                       fieldbackground="#1a1a2e",
                       bordercolor=self.primary_color,
                       font=self.font_small)
        style.map("Treeview", 
                 background=[("selected", self.primary_color)],
                 foreground=[("selected", "#000000")])
        
        self.playlist_tree.heading("#0", text="N°")
        self.playlist_tree.heading("title", text="Titre")
        self.playlist_tree.heading("duration", text="Durée")
        
        self.playlist_tree.column("#0", width=50, anchor="center")
        self.playlist_tree.column("title", width=400, anchor="w")
        self.playlist_tree.column("duration", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(playlist_frame, orient="vertical", 
                                 command=self.playlist_tree.yview)
        self.playlist_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.playlist_tree.pack(fill="both", expand=True)
        
        # Événements
        self.playlist_tree.bind("<Double-1>", self.on_double_click)
        self.root.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Redessine les effets graphiques lors du redimensionnement"""
        self.draw_scanlines()
    
    def load_playlist(self):
        """Charge une playlist M3U/M3U8"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Fichiers M3U", "*.m3u *.m3u8"), ("Tous les fichiers", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            self.playlist = []
            self.playlist_tree.delete(*self.playlist_tree.get_children())
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    self.playlist.append(line)
            
            for idx, track in enumerate(self.playlist, 1):
                track_name = os.path.basename(track)
                self.playlist_tree.insert("", "end", text=str(idx), 
                                         values=(track_name, "--:--"))
            
            if self.playlist:
                self.current_index = 0
                self.playlist_tree.selection_set(self.playlist_tree.get_children()[0])
                self.update_current_track_label()
                messagebox.showinfo("Playlist chargée", 
                                    f"{len(self.playlist)} morceaux chargés avec succès!")
            else:
                messagebox.showwarning("Playlist vide", 
                                     "La playlist ne contient aucun morceau valide.")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger la playlist:\n{str(e)}")
    
    def play(self):
        """Joue le morceau sélectionné"""
        if not self.playlist:
            messagebox.showwarning("Aucun morceau", "Veuillez charger une playlist d'abord.")
            return
        
        selected_item = self.playlist_tree.selection()
        if selected_item:
            self.current_index = int(self.playlist_tree.index(selected_item[0]))
        
        if 0 <= self.current_index < len(self.playlist):
            track = self.playlist[self.current_index]
            try:
                media = self.instance.media_new(track)
                media.add_option(':preferred-resolution=720')
                media.add_option(':network-caching=3000')
                self.player.set_media(media)
                self.player.play()
                self.is_playing = True
                self.update_current_track_label()
                
                # Mettre en surbrillance le morceau en cours
                for item in self.playlist_tree.get_children():
                    self.playlist_tree.item(item, tags=())
                self.playlist_tree.item(self.playlist_tree.get_children()[self.current_index], 
                                       tags=("current",))
                self.playlist_tree.tag_configure("current", background=self.secondary_color)
                
            except Exception as e:
                messagebox.showerror("Erreur de lecture", 
                                   f"Impossible de lire le flux:\n{str(e)}\n\n"
                                   "Vérifiez que vous avez les codecs nécessaires installés.")
                self.stop()
    
    def pause(self):
        """Met en pause ou reprend la lecture"""
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
        else:
            if self.player.get_media():
                self.player.play()
                self.is_playing = True
    
    def stop(self):
        """Arrête la lecture"""
        self.player.stop()
        self.is_playing = False
    
    def prev_track(self):
        """Passe au morceau précédent"""
        if not self.playlist:
            return
        
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.playlist_tree.selection_set(self.playlist_tree.get_children()[self.current_index])
        self.play()
    
    def next_track(self):
        """Passe au morceau suivant"""
        if not self.playlist:
            return
        
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.playlist_tree.selection_set(self.playlist_tree.get_children()[self.current_index])
        self.play()
    
    def set_volume(self, volume):
        """Ajuste le volume"""
        self.volume = int(volume)
        self.player.audio_set_volume(self.volume)
    
    def on_double_click(self, event):
        """Joue le morceau double-cliqué"""
        item = self.playlist_tree.identify_row(event.y)
        if item:
            self.play()
    
    def update_current_track_label(self):
        """Met à jour l'affichage du morceau en cours"""
        if 0 <= self.current_index < len(self.playlist):
            track_name = os.path.basename(self.playlist[self.current_index])
            self.current_track_label.config(text=f"EN COURS: {track_name}")
        else:
            self.current_track_label.config(text="Aucun morceau sélectionné")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberpunkPlayer(root)
    root.mainloop()