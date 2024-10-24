import tkinter as tk
import random
import time
from PIL import Image, ImageTk
import os
import threading
import numpy as np
import sounddevice as sd
import collectData
import json

class ExperimentApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Brainwave Experiment")
        self.root.geometry("1200x800")

        self.current_frame = None
        self.label = None

        # Biến để lưu thông tin hành động
        self.actions = []

        # Start with the login screen
        self.create_login_screen()
    
    def on_spacebar_press(self, event):
        """Xử lý sự kiện khi nhấn phím Space"""
        if self.current_frame:
            if hasattr(self, 'next_function'):
                self.next_function()

    def on_arrow_press(self, event):
        """Xử lý sự kiện khi nhấn phím mũi tên trái hoặc phải"""
        if event.keysym == 'Left':
            action = "No"  # Người dùng chọn "No"
            print(f"No selected for image {self.current_image_index}")
        elif event.keysym == 'Right':
            action = "Yes"  # Người dùng chọn "Yes"
            print(f"Yes selected for image {self.current_image_index}")

        # Lưu lại thông tin hình ảnh và hành động
        self.actions.append({
            'image': self.image_paths[self.current_image_index - 1],  # Ảnh vừa được hiển thị
            'action': action
        })

        self.root.unbind('<Left>')
        self.root.unbind('<Right>')

        self.root.after_cancel(self.timeout_id)
    
    def too_slow(self):
        """Xử lý khi người dùng không bấm phím kịp thời"""
        action = "Too slow"
        print(f"Have not pressed any key for image {self.current_image_index}")
        
        self.actions.append({
            'image': self.image_paths[self.current_image_index - 1],  # Ảnh vừa được hiển thị
            'action': action
        })

        

    def create_login_screen(self):
        """Tạo màn hình đăng nhập"""
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Login").pack()
        
        self.name_var = tk.StringVar()
        tk.Label(frame, text="Name:").pack()
        tk.Entry(frame, textvariable=self.name_var).pack()

        self.age_var = tk.StringVar()
        tk.Label(frame, text="Age:").pack()
        tk.Entry(frame, textvariable=self.age_var).pack()
        
        self.gender_var = tk.StringVar()
        tk.Label(frame, text="Gender:").pack()
        tk.Entry(frame, textvariable=self.gender_var).pack()
        
        self.phone_var = tk.StringVar()
        tk.Label(frame, text="Phone Number:").pack()
        tk.Entry(frame, textvariable=self.phone_var).pack()
        
        tk.Button(frame, text="Login", command=self.login_success).pack(pady=10)

        self.current_frame = frame

    def login_success(self):
        """Xử lý sau khi đăng nhập thành công"""
        # Hiển thị label thông báo đã đăng nhập thành công
        self.clear_frame()

        # Tạo một frame mới để hiển thị thông báo thành công và chuyển tiếp
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # Thêm label thông báo đăng nhập thành công
        tk.Label(frame, text="Đã đăng nhập thành công!", font=("Helvetica", 18), fg="green").pack(pady=10)
        tk.Label(frame, text=f"Xin chào, {self.name_var.get()}!").pack(pady=10)

        # Nút nhấn tiếp tục
        tk.Label(frame, text="Press [spacebar] to start the experiment.").pack(pady=10)

        # Gắn lại sự kiện nhấn phím space để bắt đầu hiển thị hình ảnh
        self.root.bind('<space>', self.on_spacebar_press)

        self.current_frame = frame

        # Chuyển đến màn hình hiển thị hình ảnh sau khi nhấn space
        self.next_function = self.create_image_display_screen

    def create_image_display_screen(self):
        """Bắt đầu màn hình hiển thị hình ảnh khi người dùng nhấn spacebar"""
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # Tạo canvas để hiển thị hình ảnh
        self.canvas = tk.Canvas(frame, width=800, height=600)
        self.canvas.pack()

        self.label = tk.Label(frame, text="Press [spacebar] to start showing images.")
        self.label.pack(pady=20)

        # Danh sách các ảnh
        self.image_paths = [f"assets/image{i}.png" for i in range(1, 7)] * 5
        random.shuffle(self.image_paths)
        self.images = [ImageTk.PhotoImage(Image.open(path).resize((800, 600))) for path in self.image_paths] 
        print(self.image_paths)

        # Biến đếm số lần hiển thị ảnh
        self.current_image_index = 0

        # Gắn sự kiện cho phím mũi tên sau khi nhấn spacebar

        # Sự kiện đầu tiên: khi nhấn spacebar, bắt đầu tự động hiển thị ảnh
        self.next_function = self.start_image_sequence
        self.current_frame = frame

    def start_image_sequence(self):
        """Bắt đầu quá trình hiển thị hình ảnh tự động sau lần nhấn spacebar đầu tiên"""
        self.root.unbind('<space>')  # Gỡ bỏ sự kiện space sau lần nhấn đầu tiên
        self.show_next_image()  # Bắt đầu hiển thị hình ảnh
        if self.label:  # Nếu label tồn tại
            self.label.pack_forget()  # Ẩn label

    def show_next_image(self):
        """Hiển thị hình ảnh tiếp theo"""

        self.root.bind('<Left>', self.on_arrow_press)   # Mũi tên trái (No)
        self.root.bind('<Right>', self.on_arrow_press)  # Mũi tên phải (Yes)

        print(self.current_image_index)
        print(len(self.images))

        if self.current_image_index < len(self.images):
            # Hiển thị hình ảnh tiếp theo từ danh sách
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.images[self.current_image_index])

            self.current_image_index += 1
            # Chuyển đến ảnh tiếp theo sau thời gian đã định
            self.root.after(int(time_rec) * (1000), self.show_black_screen)
            self.timeout_id = self.root.after(int(time_rec) * (1000), self.too_slow)
            
            # Lưu dữ liệu khi hiển thị ảnh
            path = f"Data/{self.name_var.get()}/{self.current_image_index}.txt"
            data_thread = threading.Thread(target=collectData.collectData, args=(path, time_rec, port))
            data_thread.start()
        else:
            self.finish_experiment()

    def show_black_screen(self):
        """Hiển thị màn hình đen sau khi hiện hình ảnh"""
        self.canvas.create_rectangle(0, 0, 800, 600, fill="black")
        # Chờ 1.5 giây trước khi nhận hành động từ phím trái/phải
        self.root.after(1500, self.show_next_image)

    def finish_experiment(self):
        """Hoàn thành thí nghiệm và ghi lại kết quả"""
        print("Calling finish_experiment...")
        self.canvas.delete('all')
        # Ghi lại các hành động vào tệp kết quả
        with open(f"Data/{self.name_var.get()}/results.txt", "w") as f:
            for action in self.actions:
                f.write(f"{action['image']} - {action['action']}\n")

        results_path = f"Data/{self.name_var.get()}/results.json"
        with open(results_path, "w") as f:
            json.dump(self.actions, f, indent=4)

        tk.Label(self.current_frame, text="All images displayed. Experiment complete!").pack(pady=30)
        # Gỡ bỏ sự kiện mũi tên sau khi hoàn tất thí nghiệm
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        self.countdown(3)


    def clear_frame(self):
        """Xóa nội dung của frame hiện tại"""
        if self.current_frame:
            self.current_frame.destroy()

    def countdown(self, count):
        """Hàm đếm ngược từ count đến 0"""
        if count > 0:
            # Xóa nội dung canvas và hiển thị số đếm ngược
            self.canvas.delete('all')
            self.canvas.create_text(400, 300, text=f"{count}", font=("Helvetica", 50))

            # Gọi lại hàm countdown sau 1 giây (1000 ms)
            self.root.after(1000, self.countdown, count - 1)
        else:
            # Sau khi đếm về 0, thoát khỏi chương trình
            self.canvas.delete('all')
            self.canvas.create_text(400, 300, text="Goodbye!", font=("Helvetica", 50))
            self.root.after(1000, self.root.quit)


if __name__ == "__main__":
    # port = "COM5"
    port = "/dev/tty.usbmodem12301"
    time_rec = 2
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()
