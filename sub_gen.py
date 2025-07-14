import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os
from tkinter import ttk
import threading
import webbrowser
import sys

class SubtitleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SubGen")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2E2E2E")

        # РЯДОК ДЛЯ ІКОНКИ

        icon_path = None
        if getattr(sys, 'frozen', False):  # Перевіряємо, чи програма запущена як запакована
            # Якщо запакована, беремо шлях з _MEIPASS
            bundle_dir = sys._MEIPASS
        else:
            # Якщо запускаємо звичайний .py файл, беремо поточну директорію скрипта
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        # Будуємо повний шлях до icon.ico
        icon_path = os.path.join(bundle_dir, 'icon.ico')

        try:
            if icon_path and os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                print(f"Іконка не знайдена за шляхом: {icon_path}")
        except tk.TclError:
            print(f"Помилка завантаження іконки з шляху: {icon_path}. Перевірте формат ICO.")
        except Exception as e:
            print(f"Невідома помилка при завантаженні іконки: {e}")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Стилі для Combobox (вибір мови)
        self.style.configure("TCombobox",
                             fieldbackground="#424242",
                             background="#505050",
                             foreground="white",
                             font=("Arial", 16),
                             selectbackground="#606060",
                             selectforeground="white",
                             borderwidth=1,
                             relief="solid",
                             padding=5
                             )
        self.style.map("TCombobox",
                       fieldbackground=[('readonly', '#424242')],
                       background=[('readonly', '#505050')],
                       selectbackground=[('readonly', '#606060')])

        # Стилізація випадаючого списку комбобоксу (ListBox)
        self.style.configure("TCombobox.Popdown.Listbox",
                             background="#505050",
                             foreground="white",
                             selectbackground="#606060",
                             selectforeground="white",
                             font=("Arial", 14),
                             borderwidth=1,
                             relief="solid")

        # Стилі для ОСНОВНИХ кнопок (Load, Generate, Save)
        self.style.configure("TButton",
                             background="#3F51B5",
                             foreground="white",
                             font=("Arial", 13, "bold"),
                             borderwidth=3,
                             relief="groove",
                             focusthickness=0,
                             focuscolor='none',
                             padding=[10, 5],
                             width=26
                             )
        self.style.map("TButton",
                       background=[('active', '#303F9F')])

        # НОВИЙ СТИЛЬ для кнопки "Про програму"
        self.style.configure("About.TButton",
                             background="#757575",
                             foreground="white",
                             font=("Arial", 13, "bold"),
                             borderwidth=2,
                             relief="solid",
                             focusthickness=0,
                             focuscolor='none',
                             padding=[10, 5],
                             width=13
                             )
        self.style.map("About.TButton",
                       background=[('active', '#9E9E9E')])

        # Стилі для Label (статус, інші написи)
        self.style.configure("TLabel",
                             background="#2E2E2E",
                             foreground="white",
                             font=("Arial", 12))

        # Стилі для Progressbar
        self.style.configure("TProgressbar",
                             background="#4CAF50",
                             troughcolor="#424242",
                             thickness=12)

        self.langs = {
            "English": {
                "load_audio": "Load Audio",
                "load_video": "Load Video",
                "generate": "Generate Subtitles",
                "save": "Save Subtitles",
                "about": "About",
                "title": "SubGen",
                "status_ready": "Load audio/video",
                "status_loaded": "Loaded: ",
                "status_loaded_and_prompt": "Loaded: {filename}. Now generate subtitles.",
                "status_transcribing": "Transcribing...",
                "status_generated": "Subtitles generated. Save them to your computer",
                "status_saved": "Subtitles saved.",
                "status_error": "Error during transcription.",
                "warning_no_file": "Please load an audio or video file first.",
                "warning_no_subs": "No subtitles to save.",
                # --- НОВІ КЛЮЧІ ДЛЯ ВІКНА "ПРО ПРОГРАМУ" ---
                "about_text_p1": "SubGen - was created to generate subtitles from video and audio.",
                "about_text_p2": "The program generates subtitles in srt format.",
                "about_developer": "Developer: Oleh Melnytskyi",
                "about_contact": "Contact information: melnitskiy95@gmail.com",
                "about_version": "Program version: 1.0.0",
                "about_telegram_intro": "More programs in the Telegram channel: ",
                # --- НОВІ КЛЮЧІ ДЛЯ ДОНАТУ ---
                "donate_intro": "🎁 Want to support our project?",
                "donate_thanks": "We would be grateful for any donation!",
                "donate_paypal_text": "Donate via "
            },
            "Українська": {
                "load_audio": "Завантажити аудіо",
                "load_video": "Завантажити відео",
                "generate": "Згенерувати субтитри",
                "save": "Зберегти субтитри",
                "about": "Про програму",
                "title": "SubGen",
                "status_ready": "Завантажте аудіо/відео",
                "status_loaded": "Завантажено: ",
                "status_loaded_and_prompt": "Завантажено: {filename}. Тепер згенеруйте субтитри.",
                "status_transcribing": "Транскрибування...",
                "status_generated": "Субтитри згенеровано. Збережіть їх на комп'ютер",
                "status_saved": "Субтитри збережено.",
                "status_error": "Помилка під час транскрибування.",
                "warning_no_file": "Будь ласка, спочатку завантажте аудіо- або відеофайл.",
                "warning_no_subs": "Немає субтитрів для збереження.",
                # --- НОВІ КЛЮЧІ ДЛЯ ВІКНА "ПРО ПРОГРАМУ" ---
                "about_text_p1": "SubGen - було створено для генерації субтитрів з відео та аудіо.",
                "about_text_p2": "Програма генерує субтитри в форматі srt.",
                "about_developer": "Розробник: Олег Мельницький",
                "about_contact": "Контактна інформація: melnitskiy95@gmail.com",
                "about_version": "Версія програми: 1.0.0",
                "about_telegram_intro": "Більше програм в телеграм каналі: ",
                # --- НОВІ КЛЮЧІ ДЛЯ ДОНАТУ ---
                "donate_intro": "🎁 Хочеш підтримати наш проєкт?",
                "donate_thanks": "Будемо вдячні за будь-який донат!",
                "donate_paypal_text": "Переказати через "
            },
            "Deutsch": {
                "load_audio": "Audio laden",
                "load_video": "Video laden",
                "generate": "Untertitel generieren",
                "save": "Untertitel speichern",
                "about": "Über",
                "title": "SubGen",
                "status_ready": "Audio/Video laden",
                "status_loaded": "Geladen: ",
                "status_loaded_and_prompt": "Geladen: {filename}. Generieren Sie jetzt Untertitel.",
                "status_transcribing": "Transkription läuft...",
                "status_generated": "Untertitel generiert. Speichern Sie sie auf Ihrem Computer",
                "status_saved": "Untertitel gespeichert.",
                "status_error": "Fehler während der Transkription.",
                "warning_no_file": "Bitte laden Sie zuerst eine Audio- oder Videodatei.",
                "warning_no_subs": "Keine Untertitel zum Speichern vorhanden.",
                # --- НОВІ КЛЮЧІ ДЛЯ ВІКНА "ПРО ПРОГРАМУ" ---
                "about_text_p1": "SubGen - wurde erstellt, um Untertitel aus Video und Audio zu generieren.",
                "about_text_p2": "Das Programm generiert Untertitel im SRT-Format.",
                "about_developer": "Entwickler: Oleh Melnytskyi",
                "about_contact": "Kontaktinformationen: melnitskiy95@gmail.com",
                "about_version": "Programmversion: 1.0.0",
                "about_telegram_intro": "Weitere Programme im Telegram-Kanal: ",
                # --- НОВІ КЛЮЧІ ДЛЯ ДОНАТУ ---
                "donate_intro": "🎁 Möchten Sie unser Projekt unterstützen?",
                "donate_thanks": "Wir wären dankbar für jede Spende!",
                "donate_paypal_text": "Spenden Sie über "
            }
        }

        self.selected_lang = tk.StringVar(value="English")
        self.current_texts = self.langs[self.selected_lang.get()]

        self.file_path = None
        self.subtitles = None
        self.app_state = "ready"

        self.progress_var = tk.DoubleVar()
        self.progressbar = None

        self.model = None
        self.load_whisper_model()

        # Постійне посилання для донату PayPal
        self.paypal_donate_url = "https://www.paypal.com/donate/?hosted_button_id=WWSDL9ZDYZBCS"

        self.create_widgets()

    def load_whisper_model(self):
        """Завантажує модель Whisper. Викликається після ініціалізації Tk."""
        try:
            self.model = whisper.load_model("small")
        except Exception as e:
            messagebox.showerror("SubGen Error", f"Failed to load Whisper model: {e}\n"
                                                 "Будь ласка, переконайтеся, що у вас стабільне інтернет-з'єднання "
                                                 "або файли моделі присутні.")
            self.model = None

    def create_widgets(self):
        # Заголовок програми
        title_label = ttk.Label(self.root, text="SubGen", font=("Arial", 28, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(30, 20))

        # Комбобокс вибору мови
        lang_menu = ttk.Combobox(self.root, textvariable=self.selected_lang, values=list(self.langs.keys()),
                                 state="readonly", style="TCombobox")
        lang_menu.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew", padx=145)
        lang_menu.bind("<<ComboboxSelected>>", self.update_language)

        # --- Фрейм для групування кнопок "Завантажити" ---
        load_buttons_frame = ttk.Frame(self.root, style="TLabel")
        load_buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        self.load_audio_btn = ttk.Button(load_buttons_frame, text=self.current_texts["load_audio"],
                                         command=self.load_audio,
                                         style="TButton")
        self.load_audio_btn.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.load_video_btn = ttk.Button(load_buttons_frame, text=self.current_texts["load_video"],
                                         command=self.load_video,
                                         style="TButton")
        self.load_video_btn.grid(row=0, column=1, padx=(5, 0), pady=5)

        # --- Фрейм для групування кнопок генерації та збереження ---
        gen_save_buttons_frame = ttk.Frame(self.root, style="TLabel")
        gen_save_buttons_frame.grid(row=3, column=0, columnspan=2, pady=(10, 30))

        self.generate_btn = ttk.Button(gen_save_buttons_frame, text=self.current_texts["generate"],
                                       command=self.start_generation,
                                       style="TButton")
        self.generate_btn.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.save_btn = ttk.Button(gen_save_buttons_frame, text=self.current_texts["save"], command=self.save_srt,
                                   style="TButton")
        self.save_btn.grid(row=0, column=1, padx=(5, 0), pady=5)

        # Прогрес-бар
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="indeterminate",
                                           variable=self.progress_var, style="TProgressbar")
        self.progressbar.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew", padx=100)
        self.progressbar.grid_remove()

        # Статус-лейбл
        self.status_label = ttk.Label(self.root, text=self.current_texts["status_ready"], style="TLabel")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Кнопка "Про програму"
        self.about_btn = ttk.Button(self.root, text=self.current_texts["about"], command=self.show_about,
                                    style="About.TButton")
        self.about_btn.grid(row=6, column=0, columnspan=2, pady=(30, 30))

        # --- НАЛАШТУВАННЯ ГЛАВНОГО ВІКНА ---
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=0)
        self.root.grid_rowconfigure(5, weight=0)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1) # Залишено для гнучкості нижньої частини вікна

        self.update_language()

    def update_language(self, event=None):
        self.current_texts = self.langs[self.selected_lang.get()]

        self.load_audio_btn.config(text=self.current_texts["load_audio"])
        self.load_video_btn.config(text=self.current_texts["load_video"])
        self.generate_btn.config(text=self.current_texts["generate"])
        self.save_btn.config(text=self.current_texts["save"])
        self.about_btn.config(text=self.current_texts["about"])
        self.root.title(self.current_texts["title"])

        # Оновлення тексту статусу та кольору відповідно до app_state
        current_text = ""
        current_color = "white"

        if self.app_state == "ready":
            current_text = self.current_texts["status_ready"]
            current_color = "white"
        elif self.app_state == "loaded":
            current_text = self.current_texts["status_loaded_and_prompt"].format(filename=os.path.basename(self.file_path))
            current_color = "white"
        elif self.app_state == "transcribing":
            current_text = self.current_texts["status_transcribing"]
            current_color = "white"
        elif self.app_state == "generated":
            current_text = self.current_texts["status_generated"]
            current_color = "#8BC34A"
        elif self.app_state == "saved":
            current_text = self.current_texts["status_saved"]
            current_color = "#2196F3"
        elif self.app_state == "error":
            current_text = self.current_texts["status_error"]
            current_color = "red"

        self.status_label.config(text=current_text, foreground=current_color)


    def load_audio(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.m4a")])
        if self.file_path:
            self.app_state = "loaded"
            display_text = self.current_texts["status_loaded_and_prompt"].format(filename=os.path.basename(self.file_path))
            self.status_label.config(text=display_text, foreground="white")
            self.progressbar.grid_remove()
            self.progress_var.set(0)
            self.generate_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
            self.load_audio_btn.config(state=tk.NORMAL)
            self.load_video_btn.config(state=tk.NORMAL)
            self.subtitles = None

    def load_video(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mov *.mkv")])
        if self.file_path:
            self.app_state = "loaded"
            display_text = self.current_texts["status_loaded_and_prompt"].format(filename=os.path.basename(self.file_path))
            self.status_label.config(text=display_text, foreground="white")
            self.progressbar.grid_remove()
            self.progress_var.set(0)
            self.generate_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
            self.load_audio_btn.config(state=tk.NORMAL)
            self.load_video_btn.config(state=tk.NORMAL)
            self.subtitles = None

    def start_generation(self):
        if not self.file_path:
            messagebox.showwarning(self.current_texts["title"], self.current_texts["warning_no_file"])
            return

        if self.model is None:
            messagebox.showerror(self.current_texts["title"],
                                 "Whisper model not loaded. Please restart the application or check your internet connection.")
            return

        self.generate_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.load_audio_btn.config(state=tk.DISABLED)
        self.load_video_btn.config(state=tk.DISABLED)

        self.progressbar.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew", padx=100)
        self.progressbar.start()

        self.app_state = "transcribing"
        self.status_label.config(text=self.current_texts["status_transcribing"], foreground="white")

        threading.Thread(target=self.generate_subtitles).start()

    def generate_subtitles(self):
        try:
            result = self.model.transcribe(self.file_path)
            self.subtitles = result["segments"]
            self.app_state = "generated"
            self.status_label.config(text=self.current_texts["status_generated"],
                                     foreground="#8BC34A")

        except Exception as e:
            self.app_state = "error"
            self.status_label.config(text=self.current_texts["status_error"],
                                     foreground="red")
            messagebox.showerror(self.current_texts["title"], str(e))
            self.subtitles = None
        finally:
            self.progressbar.stop()
            self.progressbar.grid_remove()
            self.generate_btn.config(state=tk.NORMAL)
            self.load_audio_btn.config(state=tk.NORMAL)
            self.load_video_btn.config(state=tk.NORMAL)
            if self.subtitles:
                self.save_btn.config(state=tk.NORMAL)
            else:
                self.save_btn.config(state=tk.DISABLED)

    def save_srt(self):
        if not self.subtitles:
            messagebox.showwarning(self.current_texts["title"], self.current_texts["warning_no_subs"])
            return
        path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT files", "*.srt")])
        if path:
            self.app_state = "saved"
            with open(path, "w", encoding="utf-8") as f:
                for i, seg in enumerate(self.subtitles):
                    f.write(
                        f"{i + 1}\n{self.format_time(seg['start'])} --> {self.format_time(seg['end'])}\n{seg['text'].strip()}\n\n")
            self.status_label.config(text=self.current_texts["status_saved"],
                                     foreground="#2196F3")

    def format_time(self, seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        msecs = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02}:{mins:02}:{secs:02},{msecs:03}"

    def show_about(self):
        self.create_about_window()

    def create_about_window(self):
        about_window = tk.Toplevel(self.root)
        about_window.title(self.current_texts["about"])
        # Збільшимо розмір вікна, щоб вмістити новий текст
        about_window.geometry("400x375")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        about_window.protocol("WM_DELETE_WINDOW", about_window.destroy)

        about_window.configure(bg="#2E2E2E")

        text_widget = tk.Text(about_window, wrap=tk.WORD, bg="#2E2E2E", fg="white",
                              font=("Arial", 11), padx=20, pady=20, borderwidth=0, relief="flat")
        text_widget.pack(expand=True, fill="both")

        # Існуючий текст "Про програму"
        about_text_content = (
            self.current_texts["about_text_p1"] + "\n\n" +
            self.current_texts["about_text_p2"] + "\n\n" +
            self.current_texts["about_developer"] + "\n" +
            self.current_texts["about_contact"] + "\n" +
            self.current_texts["about_version"] + "\n"
        )
        telegram_link_intro = self.current_texts["about_telegram_intro"]
        telegram_link_text = "t.me/mlntsksoft"
        telegram_channel_name = "Mlntsk Soft" # Текст, що відображається для Telegram посилання

        text_widget.insert(tk.END, about_text_content)
        text_widget.insert(tk.END, "\n" + telegram_link_intro)

        # Посилання на Telegram
        link_label = tk.Label(text_widget, text=telegram_channel_name,
                              fg="#2196F3", cursor="hand2", font=("Arial", 11, "underline"),
                              bg="#2E2E2E")

        link_label.bind("<Button-1>", lambda e: self.open_link(telegram_link_text))

        text_widget.window_create(tk.END, window=link_label, stretch=True)

        # Додаємо роздільник для кращої читабельності перед секцією донату
        text_widget.insert(tk.END, "\n\n" + "-"*40 + "\n\n")

        # Новий текст для донату
        text_widget.insert(tk.END, self.current_texts["donate_intro"] + "\n\n")
        text_widget.insert(tk.END, self.current_texts["donate_thanks"] + "\n\n")
        text_widget.insert(tk.END, self.current_texts["donate_paypal_text"] + " ")

        # Посилання на PayPal
        paypal_link_label = tk.Label(text_widget, text="PayPal", # Текст, який буде клікабельним
                                     fg="#2196F3", cursor="hand2", font=("Arial", 11, "underline"),
                                     bg="#2E2E2E")
        paypal_link_label.bind("<Button-1>", lambda e: self.open_link(self.paypal_donate_url))
        text_widget.window_create(tk.END, window=paypal_link_label, stretch=True)


        text_widget.config(state=tk.DISABLED) # Робимо Text віджети тільки для читання

    def open_link(self, url):
        """Відкриває посилання у веб-браузері."""
        try:

            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open link: {e}\nPlease check your browser installation.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleApp(root)
    root.mainloop()