import os
import random
import tkinter as tk
from PIL import Image, ImageTk

# Desactivar el mensaje de bienvenida de Pygame en la terminal
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class StrangerThingsQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("HAWKINS NATIONAL LABORATORY - TERMINAL SYSTEM")
        
        # Forzar ejecución en pantalla completa
        self.root.attributes("-fullscreen", True)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        
        # Máquina de estados de la aplicación
        self.STATE_BOOT = "BOOT"
        self.STATE_START = "START"
        self.STATE_QUIZ = "QUIZ"
        self.STATE_FEEDBACK = "FEEDBACK"
        self.STATE_RESULTS = "RESULTS"
        self.STATE_ERROR = "ERROR"
        
        self.current_state = self.STATE_BOOT
        
        # Configuración estética retro (Verde fósforo puro de alta intensidad)
        self.COLOR_BG = "#000000"
        self.COLOR_PHOSPHOR = "#00FF00" 
        self.FONT_FAMILY = "Courier New"
        
        # Banco de preguntas (10 preguntas sobre el universo de Stranger Things)
        self.questions = [
            {
                "question": "What is the name of the parallel dimension in Stranger Things?",
                "answers": ["The Void", "Upside Down", "Shadow Realm", "Dark World"],
                "correct": 1
            },
            {
                "question": "What is Eleven's favorite food?",
                "answers": ["French Fries", "Eggo Waffles", "Chocolate Pudding", "Cheeseburgers"],
                "correct": 1
            },
            {
                "question": "Who is the Chief of Police in Hawkins during the first three seasons?",
                "answers": ["Calvin Powell", "Phil Callahan", "Jim Hopper", "Lonnie Byers"],
                "correct": 2
            },
            {
                "question": "What creature does Dustin adopt and name 'Dart' in Season 2?",
                "answers": ["Demodog", "Demogorgon", "Mind Flayer", "Pollywog"],
                "correct": 3
            },
            {
                "question": "What tabletop game are the boys playing in the basement in episode 1?",
                "answers": ["Call of Cthulhu", "Dungeons & Dragons", "Warhammer", "Magic: The Gathering"],
                "correct": 1
            },
            {
                "question": "What is the name of the new mall that opens in Hawkins during Season 3?",
                "answers": ["Starcourt Mall", "Hawkins Square Mall", "Oakridge Center", "Paramus Mall"],
                "correct": 0
            },
            {
                "question": "What song saves Max from Vecna's curse in Season 4?",
                "answers": ["Should I Stay or Should I Go", "Master of Puppets", "Running Up That Hill", "Separate Ways"],
                "correct": 2
            },
            {
                "question": "What is the actual name of the character known as '001' / Vecna?",
                "answers": ["Henry Creel", "Peter Ballard", "Victor Creel", "Martin Brenner"],
                "correct": 0
            },
            {
                "question": "What character famously works at the Scoops Ahoy ice cream parlor?",
                "answers": ["Nancy Wheeler", "Steve Harrington", "Jonathan Byers", "Billy Hargrove"],
                "correct": 1
            },
            {
                "question": "What is the name of Bob Newby's electronics store chain?",
                "answers": ["RadioShack", "Hawkins Radio & TV", "Bob's RadioXpress", "Radio Shack Franchise"],
                "correct": 0
            }
        ]
        
        # Variables de control de juego y animación
        self.current_question_idx = 0
        self.score = 0
        self.cursor_visible = True
        self.feedback_text = ""
        
        self.boot_lines = [
            "BOOTING HAWKINS TERMINAL...",
            "INITIALIZING MEMORY...",
            "LOADING DATABASE...",
            "LOADING SUBJECT FILES...",
            "CONNECTING TO HAWKINS NATIONAL LAB...",
            "ACCESS GRANTED"
        ]
        self.boot_display_lines = []
        self.current_boot_line_idx = 0
        self.current_boot_char_idx = 0
        
        # Inicialización de subsistemas operativos
        self.setup_canvas()
        self.init_audio_system()
        self.load_visual_assets()
        self.bind_keyboard_controls()
        
        # Lanzamiento del bucle inicial si no hay errores críticos de carga
        if self.current_state != self.STATE_ERROR:
            self.play_background_sound()
            self.blink_cursor()
            self.boot_sequence()
        else:
            self.render_screen()

    def setup_canvas(self):
        """Genera el espacio gráfico interactivo con soporte de capas."""
        self.canvas = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height, 
            bg=self.COLOR_BG, 
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def init_audio_system(self):
        """Inicializa el mezclador de audio con control de excepciones."""
        try:
            pygame.mixer.init()
            self.sound_error = False
        except Exception:
            self.sound_error = True
            self.trigger_fatal_error("AUDIO HARDWARE INITIALIZATION FAILURE")

    def load_visual_assets(self):
        """Carga y escala los archivos de imagen aumentados al máximo para el centro CRT."""
        if self.current_state == self.STATE_ERROR:
            return
            
        try:
            # 1. Overlay del Monitor CRT
            if not os.path.exists("monitor.png"):
                raise FileNotFoundError("MONITOR IMAGE NOT FOUND")
            img = Image.open("monitor.png")
            img_resized = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            self.monitor_photo = ImageTk.PhotoImage(img_resized)
            
            # 2. Imagen de Victoria (Tamaño de impacto masivo)
            if os.path.exists("Win.png"):
                win_img = Image.open("Win.png").resize((850, 480), Image.Resampling.LANCZOS)
                self.win_photo = ImageTk.PhotoImage(win_img)
            else:
                self.win_photo = None

            # 3. Imagen de Derrota (Tamaño de impacto masivo)
            if os.path.exists("Loser.png"):
                loser_img = Image.open("Loser.png").resize((850, 480), Image.Resampling.LANCZOS)
                self.loser_photo = ImageTk.PhotoImage(loser_img)
            else:
                self.loser_photo = None
                
            self.image_error = False
        except Exception as e:
            self.image_error = True
            self.trigger_fatal_error(str(e).upper())

    def play_background_sound(self):
        """Inicia el bucle continuo del ambiente del ordenador de laboratorio."""
        if self.sound_error:
            return
        try:
            if not os.path.exists("sound_pc.mp3"):
                raise FileNotFoundError("SOUND FILE NOT FOUND")
            pygame.mixer.music.load("sound_pc.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            self.sound_error = True
            self.trigger_fatal_error(str(e).upper())

    def play_sfx(self, sfx_type):
        """Reproduce efectos de sonido instantáneos sin pausar la música de fondo."""
        if self.sound_error:
            return
        try:
            if sfx_type == "correct" and os.path.exists("correct.mp3"):
                pygame.mixer.Sound("correct.mp3").play()
            elif sfx_type == "error" and os.path.exists("error.mp3"):
                pygame.mixer.Sound("error.mp3").play()
        except Exception:
            pass 

    def bind_keyboard_controls(self):
        """Enlaza las acciones físicas del teclado con las funciones del sistema."""
        self.root.bind("<Return>", self.handle_enter_key)
        for key in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']:
            idx = {'a':0, 'b':1, 'c':2, 'd':3, 'A':0, 'B':1, 'C':2, 'D':3}[key]
            self.root.bind(f"<{key}>", lambda e, i=idx: self.handle_choice_input(i))
        
        self.root.bind("<Control-q>", self.quit_app)
        self.root.bind("<Control-Q>", self.quit_app)

    def trigger_fatal_error(self, message):
        """Cambia el estado del sistema a un bloqueo por error crítico de hardware/software."""
        self.current_state = self.STATE_ERROR
        self.error_msg = f"FATAL ERROR:\n{message}"

    def boot_sequence(self):
        """Efecto typewriter automático de la terminal gubernamental de Hawkins."""
        if self.current_state != self.STATE_BOOT:
            return
            
        if self.current_boot_line_idx < len(self.boot_lines):
            target_line = self.boot_lines[self.current_boot_line_idx]
            
            if self.current_boot_char_idx == 0:
                self.boot_display_lines.append("")
                
            if self.current_boot_char_idx < len(target_line):
                self.boot_display_lines[self.current_boot_line_idx] += target_line[self.current_boot_char_idx]
                self.current_boot_char_idx += 1
                self.render_screen()
                self.root.after(35, self.boot_sequence)
            else:
                self.current_boot_line_idx += 1
                self.current_boot_char_idx = 0
                self.root.after(350, self.boot_sequence)
        else:
            self.root.after(500, self.show_start_screen)

    def show_start_screen(self):
        self.current_state = self.STATE_START
        self.render_screen()

    def start_quiz(self):
        if not self.questions:
            self.trigger_fatal_error("DATABASE COLD RECOVERY FAILURE: NO QUESTIONS")
            self.render_screen()
            return
        self.current_question_idx = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.current_state = self.STATE_QUIZ
        self.render_screen()

    def handle_choice_input(self, selected_index):
        if self.current_state != self.STATE_QUIZ:
            return
            
        q_data = self.questions[self.current_question_idx]
        if selected_index == q_data["correct"]:
            self.score += 1
            self.feedback_text = "ACCEPTED"
            self.play_sfx("correct")
        else:
            self.feedback_text = "-ERROR-"
            self.play_sfx("error")
            
        self.current_state = self.STATE_FEEDBACK
        self.render_screen()
        self.root.after(1200, self.advance_quiz_loop)

    def advance_quiz_loop(self):
        self.current_question_idx += 1
        if self.current_question_idx < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        self.current_state = self.STATE_RESULTS
        self.render_screen()

    def handle_enter_key(self, event=None):
        if self.current_state in (self.STATE_START, self.STATE_RESULTS):
            self.start_quiz()

    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.render_screen()
        self.root.after(500, self.blink_cursor)

    def render_screen(self):
        """Renderiza la interfaz con proporciones basadas en porcentajes para evitar recortes del marco."""
        self.canvas.delete("all")
        
        center_x = self.width // 2
        
        # --- CAPA 2: Elementos del juego e interfaz de usuario ---
        if self.current_state == self.STATE_ERROR:
            self.canvas.create_text(
                center_x, self.height // 2, 
                text=self.error_msg, fill="#FF3333", 
                font=(self.FONT_FAMILY, 30, "bold"), justify=tk.CENTER
            )
            
        elif self.current_state == self.STATE_BOOT:
            display_str = "\n".join(self.boot_display_lines)
            if self.cursor_visible:
                display_str += " █"
            self.canvas.create_text(
                center_x - 450, int(self.height * 0.22), text=display_str, 
                fill=self.COLOR_PHOSPHOR, font=(self.FONT_FAMILY, 26, "bold"), 
                anchor=tk.NW, justify=tk.LEFT
            )
            
        elif self.current_state == self.STATE_START:
            header_text = "========================================\n" \
                          "        HAWKINS TERMINAL SYSTEM         \n" \
                          "             VERSION 1.7.86             \n" \
                          "          STRANGER THINGS QUIZ          \n" \
                          "========================================"
            self.canvas.create_text(
                center_x, int(self.height * 0.28), text=header_text, 
                fill=self.COLOR_PHOSPHOR, font=(self.FONT_FAMILY, 28, "bold"), justify=tk.CENTER
            )
            
            prompt_str = "PRESS ENTER TO START"
            if self.cursor_visible:
                prompt_str += " █"
            self.canvas.create_text(
                center_x, int(self.height * 0.65), text=prompt_str, 
                fill=self.COLOR_PHOSPHOR, font=(self.FONT_FAMILY, 28, "bold"), justify=tk.CENTER
            )
            
        elif self.current_state in (self.STATE_QUIZ, self.STATE_FEEDBACK):
            q_data = self.questions[self.current_question_idx]
            
            # --- CORRECCIÓN MARGO SUPERIOR ---
            # Bajamos de forma segura el indicador de pregunta al 20% de la altura total
            progress_str = f"QUESTION {self.current_question_idx + 1} / {len(self.questions)}"
            self.canvas.create_text(
                center_x, int(self.height * 0.20), text=progress_str, 
                fill=self.COLOR_PHOSPHOR, font=(self.FONT_FAMILY, 20, "bold"), justify=tk.CENTER
            )
            
            # Bajamos el bloque de la pregunta al 29% de la altura
            wrapped_question = self.wrap_text(q_data["question"], 65)
            self.canvas.create_text(
                center_x, int(self.height * 0.29), text=wrapped_question, 
                fill=self.COLOR_PHOSPHOR, font=(self.FONT_FAMILY, 32, "bold"), 
                justify=tk.CENTER, width=1150
            )
            
            labels = ["A) ", "B) ", "C) ", "D) "]
            # Las opciones de respuesta inician cómodamente en el 44% de la pantalla
            choices_y = int(self.height * 0.44)
            for i, ans in enumerate(q_data["answers"]):
                choice_str = f"{labels[i]}{ans}"
                self.canvas.create_text(
                    center_x - 500, choices_y + (i * 65), text=choice_str, 
                    fill=self.COLOR_PHOSPHOR, font=(self.FONT_FAMILY, 26, "bold"), 
                    anchor=tk.NW, justify=tk.LEFT
                )
                
            if self.current_state == self.STATE_FEEDBACK:
                feedback_y = int(self.height * 0.76)
                if self.feedback_text == "-ERROR-":
                    self.canvas.create_rectangle(
                        center_x - 240, feedback_y - 55, 
                        center_x + 240, feedback_y + 55, 
                        fill="#FF0000", outline="#880000", width=5
                    )
                    feedback_color = "#000000"
                else:
                    feedback_color = self.COLOR_PHOSPHOR
                    
                self.canvas.create_text(
                    center_x, feedback_y, text=self.feedback_text, 
                    fill=feedback_color, font=(self.FONT_FAMILY, 44, "bold"), justify=tk.CENTER
                )
                
        elif self.current_state == self.STATE_RESULTS:
            player_survived = self.score >= 6
            
            # Centro de imagen equilibrado verticalmente
            img_center_y = int(self.height * 0.38)
            
            if player_survived and self.win_photo:
                self.canvas.create_image(center_x, img_center_y, image=self.win_photo, anchor=tk.CENTER)
            elif not player_survived and self.loser_photo:
                self.canvas.create_image(center_x, img_center_y, image=self.loser_photo, anchor=tk.CENTER)
            
            if player_survived:
                status_title = "HAWKINS DATABASE ACCESS GRANTED"
                rank_str = "RANK: HAWKINS EXPERT"
                text_color = self.COLOR_PHOSPHOR
            else:
                status_title = "YOU JUST DIED. THE DEMOGORGON GOT YOU."
                rank_str = "RANK: ROOKIE / WASTELAND SUBJECT"
                text_color = "#FF3333"
                
            results_text = f"========================================\n" \
                           f" {status_title}\n" \
                           f"========================================\n\n" \
                           f"FINAL SCORE: {self.score} / {len(self.questions)}\n" \
                           f"{rank_str}\n\n" \
                           f"========================================\n" \
                           f"PRESS ENTER TO RESTART SYSTEM\n" \
                           f"CTRL + Q TO TERMINATE CONNECTION"
            
            # Colocamos el texto de resultados estirado de forma idónea sobre la base negra
            self.canvas.create_text(
                center_x, int(self.height * 0.74), text=results_text, 
                fill=text_color, font=(self.FONT_FAMILY, 20, "bold"), justify=tk.CENTER
            )
            
        # --- CAPA 3: Overlay Fijo monitor.png (Siempre por encima de todo) ---
        if hasattr(self, 'monitor_photo') and self.current_state != self.STATE_ERROR:
            self.canvas.create_image(0, 0, image=self.monitor_photo, anchor=tk.NW)

    def wrap_text(self, text, max_chars):
        words = text.split(' ')
        lines, current_line = [], []
        current_length = 0
        for word in words:
            if current_length + len(word) + len(current_line) <= max_chars:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        if current_line:
            lines.append(" ".join(current_line))
        return "\n".join(lines)

    def quit_app(self, event=None):
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StrangerThingsQuiz(root)
    root.mainloop()