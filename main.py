import tkinter as tk
from tkinter import messagebox
import threading
from gui import TaskManagerGUI
from task_manager import TaskManager
from scheduler import TaskScheduler
from database import Database
import logging

# Logging konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager - Aqlli Rejalashtirish")
        self.root.geometry("900x700")
        
        # Database va Task Manager
        self.db = Database()
        self.task_manager = TaskManager(self.db)
        self.scheduler = TaskScheduler(self.task_manager, self.db)
        
        # GUI
        self.gui = TaskManagerGUI(root, self.task_manager, self.db, self.scheduler)
        
        # Scheduler thread
        self.scheduler_thread = threading.Thread(target=self.scheduler.start, daemon=True)
        self.scheduler_thread.start()
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        logging.info("Ilova muvaffaqiyatli ishga tushdi")
    
    def on_closing(self):
        if messagebox.askokcancel("Chiqish", "Ilovani yopmoqchimisiz?"):
            self.scheduler.stop()
            self.db.close()
            self.root.destroy()
            logging.info("Ilova yopildi")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()