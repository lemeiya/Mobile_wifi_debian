#关于开展2023年度哈尔滨市中小学生信息素养提升实践活动参赛作品
#所需库
import tkinter as tk
import requests
import json
import sv_ttk
from tkinter import messagebox
from tkinter import ttk


class Head:#头部
    def __init__(self, master: tk.Tk):
        self.root = master
        self.root.title("图书管理系统")
        self.root.maxsize(700, 500)
        self.root.minsize(700, 500)
        self.menu()
        self.isbn_input = tk.Entry(self.root, width=50)
        sv_ttk.set_theme("light")
        self.result_text = None
        self.cloud_frame = None
        self.add_frame = None
        self.isbn_frame = None
        self.current_frame = None
        self.isbn = None
        self.show_cloud_frame()

    def menu(self):
        menuber = tk.Menu(self.root)
        menuber.add_command(label="云端查询", command=self.show_cloud_frame)
        menuber.add_command(label="添加书籍", command=self.show_add_frame)
        menuber.add_command(label="ISBN查询", command=self.show_isbn_frame)
        menuber.add_command(label="关于", command=self.about_me)
        self.root['menu'] = menuber

    def show_cloud_frame(self):
        if self.cloud_frame is None:
            self.cloud_frame = tk.Frame(self.root, width=500, height=400)
            self.cloud_frame.place(relx=0.5, rely=0.3, anchor='center')
            self.result_text_cloud = tk.Text(self.cloud_frame, width=50, height=20)
            self.result_text_cloud.pack()
            ttk.Button(self.cloud_frame, text="云端查书", command=self.book_search_for_btn_cloud,
                       style='Accent.TButton').pack(side="left", padx=10, pady=10)
            ttk.Button(self.cloud_frame, text="刷新", command=self.book_search_for_btn_cloud,
                       style='Accent.TButton').pack(side="left", padx=10, pady=10)
        elif self.current_frame == self.cloud_frame:
            return
        self.show_frame(self.cloud_frame)

    def show_add_frame(self):
        if self.add_frame is None:
            self.add_frame = tk.Frame(self.root, width=500, height=400)
            self.add_frame.place(relx=0.5, rely=0.3, anchor='center')
            title_lbl = ttk.Label(self.add_frame, text='书名:')
            title_lbl.place(relx=0.1, rely=0.2)
            self.title_input = ttk.Entry(self.add_frame, width=20)
            self.title_input.place(relx=0.2, rely=0.2)
            author_lbl = ttk.Label(self.add_frame, text='作者:')
            author_lbl.place(relx=0.1, rely=0.3)
            self.author_input = ttk.Entry(self.add_frame, width=20)
            self.author_input.place(relx=0.2, rely=0.3)
            isbn_lbl = ttk.Label(self.add_frame, text='ISBN:')
            isbn_lbl.place(relx=0.1, rely=0.4)
            self.isbn_input = ttk.Entry(self.add_frame, width=20)
            self.isbn_input.place(relx=0.2, rely=0.4)
            add_btn = ttk.Button(self.add_frame, text='添加', command=self.book_add_btn)
            add_btn.place(relx=0.2, rely=0.5)
        self.show_frame(self.add_frame)

    def show_isbn_frame(self):
        if self.isbn_frame is None:
            self.isbn_frame = tk.Frame(self.root, width=500, height=400)
            self.isbn_frame.place(relx=0.5, rely=0.3, anchor='center')
            isbn_lbl = ttk.Label(self.isbn_frame, text='ISBN:')
            isbn_lbl.grid(row=0, column=0, padx=10, pady=10)
            self.isbn_input = ttk.Entry(self.isbn_frame, width=20)
            self.isbn_input.grid(row=0, column=1, padx=10, pady=10)
            ttk.Button(self.isbn_frame, text='查询', command=self.book_ISBN_btn, style='Accent.TButton').grid(row=0,
                                                                                                              column=2,
                                                                                                              padx=10,
                                                                                                              pady=10)
            self.result_text_ISBN = tk.Text(self.isbn_frame, width=50, height=20)
            self.result_text_ISBN.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        else:
            self.show_frame(self.isbn_frame)
            if self.isbn:
                self.isbn_input.delete(0, tk.END)
                self.isbn_input.insert(0, self.isbn)

    def show_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        frame.pack()
        self.current_frame = frame

    def book_add_btn(self):
        url = 'https://api.fastmay.top/book/add_library.php'
        data = {
            'title': self.title_input.get(),
            'author': self.author_input.get(),
            'isbn': self.isbn_input.get()
        }
        response = requests.post(url, data=data)
        result = response.json()
        if result['status']:
            messagebox.showinfo(message=result['message'])

    def about_me(self):
        messagebox.showinfo(title="关于",
                            message="图书管理系统\n\n对接api:\nhttps://api.fastmay.top/book/library.php\nhttps://www.maitanbang.com/apis/mtbisbn/\n\n所使用库：\nrequests，json，tkinter以及美化库sv_ttk\n\n作者：戏。\n禁止对此源码进行二次更改以及禁止任何1商业行为！")

    def book_search_for_btn_cloud(self):
        data = {
            'search_term': '西游记'
        }
        url = 'https://api.fastmay.top/book/library.php'
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        json_data = response.json()
        result_text = ''
        for book in json_data:
            result_text += f"书名：{book['title']}\n"
            result_text += f"作者：{book['author']}\n"
            result_text += f"编号：{book['description']}\n"
            result_text += '------------------\n'
        self.result_text_cloud.delete("1.0", tk.END)
        self.result_text_cloud.insert(tk.END, result_text)

    def book_ISBN_btn(self):
        isbn = self.isbn_input.get()

        if not isbn:
            messagebox.showerror(title="错误", message="请输入ISBN号码")
            return
        url = 'http://www.maitanbang.com/apis/mtbisbn'
        headers = {
            'Content-Type': 'application/json'
        }
        key = 'a30f49b41e038a116144a9235e7bf2a0 '
        data = {
            'key': key,
            'isbn': isbn
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        json_data = response.json()
        if json_data['code'] != 200:
            messagebox.showinfo(title="提示", message="未找到相关书籍")
            return
        result_text = ''
        result_text += f"书名：{json_data['data']['subname']}\n"
        result_text += f"作者：{json_data['data']['author']}\n"
        result_text += f"出版社：{json_data['data']['publishing']}\n"
        result_text += f"出版时间：{json_data['data']['published']}\n"
        self.result_text_ISBN.delete("1.0", tk.END)
        self.result_text_ISBN.insert(tk.END, result_text)
        self.isbn = isbn


if __name__ == '__main__':
    root = tk.Tk()
    Head(root)
    root.mainloop()