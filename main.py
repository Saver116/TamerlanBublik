import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk

class Product:
    def __init__(self, name, price, image):
        self.__name = name
        self.__price = price
        self.__image = image

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_image(self):
        return self.__image

class Cart:
    def __init__(self):
        self.__items = {}

    def add_item(self, product):
        if product:
            product_name = product.get_name()
            if product_name in self.__items:
                self.__items[product_name] += 1
            else:
                self.__items[product_name] = 1

    def get_items(self):
        return self.__items

    def calculate_total(self, products):
        total = 0
        for product_name, quantity in self.__items.items():
            for product in products:
                if product.get_name() == product_name:
                    total += product.get_price() * quantity
                    break
        return total

class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def check_password(self, password):
        return self.__password == password

class AdminPanel:
    def __init__(self, root, app):
        self.__root = root
        self.__app = app
        self.product_name_entry = None
        self.product_price_entry = None
        self.product_image_path = None

    def show_update_product(self):
        self.admin_actions_frame.destroy()

        self.update_product_frame = tkinter.Frame(self.__root, bg="black")
        self.update_product_frame.place(x=400, y=50)

        self.update_label = tkinter.Label(self.update_product_frame, text="Select a product to update:", bg="black", fg="white")
        self.update_label.pack()

        self.product_to_update = tkinter.StringVar()
        product_choices = [product["name"] for product in self.__app.products]
        product_menu = tkinter.OptionMenu(self.update_product_frame, self.product_to_update, *product_choices)
        product_menu.pack()

        self.new_product_name_label = tkinter.Label(self.update_product_frame, text="New Product Name:", bg="black", fg="white")
        self.new_product_name_label.pack()

        self.new_product_name_entry = tkinter.Entry(self.update_product_frame)
        self.new_product_name_entry.pack()

        self.new_product_price_label = tkinter.Label(self.update_product_frame, text="New Product Price:", bg="black", fg="white")
        self.new_product_price_label.pack()

        self.new_product_price_entry = tkinter.Entry(self.update_product_frame)
        self.new_product_price_entry.pack()

        self.update_product_button = tkinter.Button(self.update_product_frame, text="Update Product", command=self.__update_product)
        self.update_product_button.pack()

    def __update_product(self):
        old_product_name = self.product_to_update.get()
        new_product_name = self.new_product_name_entry.get()
        new_product_price = self.new_product_price_entry.get()

        if new_product_name and new_product_price:
            for product in self.__app.products:
                if product["name"] == old_product_name:
                    product["name"] = new_product_name
                    product["price"] = int(new_product_price)
                    self.__app.save_products_txt(self.__app.products)
                    messagebox.showinfo("Product Updated", f"{old_product_name} has been updated!")
                    break
            else:
                messagebox.showerror("Update Product Error", "Product not found")
        else:
            messagebox.showerror("Update Product Error", "Please fill in all fields")

    def show_admin_actions(self):

        self.admin_actions_frame = tkinter.Frame(self.__root, bg="black")
        self.admin_actions_frame.place(x=400, y=50)

        action_label = tkinter.Label(self.admin_actions_frame, text="Select an action:", bg="black", fg="white")
        action_label.pack()

        add_button = tkinter.Button(self.admin_actions_frame, text="Add Product", command=self.show_add_product)
        add_button.pack()

        update_button = tkinter.Button(self.admin_actions_frame, text="Update Product",command=self.show_update_product)
        update_button.pack()

        delete_button = tkinter.Button(self.admin_actions_frame, text="Delete Product",command=self.show_delete_product)
        delete_button.pack()

    def show_add_product(self):
        self.admin_actions_frame.destroy()

        self.add_product_frame = tkinter.Frame(self.__root, bg="black")
        self.add_product_frame.place(x=400, y=50)

        self.product_name_label = tkinter.Label(self.add_product_frame, text="Product Name:", bg="black", fg="white")
        self.product_name_label.pack()

        self.product_name_entry = tkinter.Entry(self.add_product_frame)
        self.product_name_entry.pack()

        self.product_price_label = tkinter.Label(self.add_product_frame, text="Product Price:", bg="black", fg="white")
        self.product_price_label.pack()

        self.product_price_entry = tkinter.Entry(self.add_product_frame)
        self.product_price_entry.pack()

        self.product_image_label = tkinter.Label(self.add_product_frame, text="Product Image Path:", bg="black", fg="white")
        self.product_image_label.pack()

        self.product_image_entry = tkinter.Entry(self.add_product_frame)
        self.product_image_entry.pack()

        self.add_product_button = tkinter.Button(self.add_product_frame, text="Add Product", command=self.__add_product)
        self.add_product_button.pack()

    def show_delete_product(self):
        self.admin_actions_frame.destroy()

        self.delete_product_frame = tkinter.Frame(self.__root, bg="black")
        self.delete_product_frame.place(x=400, y=50)

        self.delete_label = tkinter.Label(self.delete_product_frame, text="Select a product to delete:", bg="black", fg="white")
        self.delete_label.pack()

        self.product_to_delete = tkinter.StringVar()
        product_choices = [product["name"] for product in self.__app.products]
        product_menu = tkinter.OptionMenu(self.delete_product_frame, self.product_to_delete, *product_choices)
        product_menu.pack()

        delete_button = tkinter.Button(self.delete_product_frame, text="Delete Product", command=self.__delete_product)
        delete_button.pack()

    def __delete_product(self):
        product_name = self.product_to_delete.get()

        if product_name:
            for product in self.__app.products:
                if product["name"] == product_name:
                    self.__app.products.remove(product)
                    self.__app.save_products_txt(self.__app.products)
                    messagebox.showinfo("Product Deleted", f"{product_name} has been deleted!")
                    self.show_admin_actions()
                    break
            else:
                messagebox.showerror("Delete Product Error", "Product not found")

    def __add_product(self):
        product_name = self.product_name_entry.get()
        product_price = int(self.product_price_entry.get())
        product_image = self.product_image_entry.get()

        if product_name and product_price and product_image:
            product = {"name": product_name, "price": product_price, "image": product_image}

            self.__app.products.append(product)
            self.__app.save_products_txt(self.__app.products)  # Use self.__app to access the method
            messagebox.showinfo("Product Added", f"{product_name} has been added to the store!")
            self.product_name_entry.delete(0, tkinter.END)
            self.product_price_entry.delete(0, tkinter.END)
            self.product_image_path = None

        else:
            messagebox.showerror("Add Product Error", "Please fill in all fields")

    def show_admin_panel(self):

        self.admin_frame = tkinter.Frame(self.__root, bg="black")
        self.admin_frame.place(x=400, y=50)

        self.product_name_label = tkinter.Label(self.admin_frame, text="Product Name:", bg="black", fg="white")
        self.product_name_label.pack()

        self.product_name_entry = tkinter.Entry(self.admin_frame)
        self.product_name_entry.pack()

        self.product_price_label = tkinter.Label(self.admin_frame, text="Product Price:", bg="black", fg="white")
        self.product_price_label.pack()

        self.product_price_entry = tkinter.Entry(self.admin_frame)
        self.product_price_entry.pack()

        self.product_image_label = tkinter.Label(self.admin_frame, text="Product Image:", bg="black", fg="white")
        self.product_image_label.pack()

        self.product_image_entry = tkinter.Entry(self.admin_frame)
        self.product_image_entry.pack()

        self.add_product_button = tkinter.Button(self.admin_frame, text="Add Product", command=self.__add_product)
        self.add_product_button.pack()


class AnimeStoreApp:
    def __init__(self, root):
        self.__root = root
        self.bg_width = 1920
        self.bg_height = 1090
        self.background_path = r"shop_bg.jpg"
        self.load_images()

        self.__froot = root
        self.__froot.geometry(f"{self.bg_width}x{self.bg_height}")
        self.__froot.title("Geekstore.az")
        self.__froot.iconbitmap("geekstore_logo.ico")

        self._user_data = {}
        self.__load_user_data()

        self.__cart = Cart()

        self.products = self.load_products_txt()

        self.__logged_in_user = None

        self.__cart_frame = None

        self.__show_main_window()

    def save_products_txt(self, products):
        with open("products.txt", "w") as file:
            for product in products:
                file.write(f"{product['name']},{product['price']},{product['image']}\n")


    def __show_admin_panel(self):
        admin_panel = AdminPanel(self.__root, self)
        admin_panel.show_admin_actions()

    def load_images(self):
        pil_image = Image.open(self.background_path)
        resized_bg_image = pil_image.resize((self.bg_width, self.bg_height))
        self.bg_image = ImageTk.PhotoImage(resized_bg_image)

    def __load_user_data(self):
        try:
            with open("user_data.txt", "r") as f:
                for line in f:
                    username, password = line.strip().split(",")
                    self._user_data[username] = {"password": password}
        except FileNotFoundError:
            self._user_data = {}

    def save_user_data(self):
        with open("user_data.txt", "w") as f:
            for username, data in self._user_data.items():
                f.write(f"{username},{data['password']}\n")

    def __login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "Admin" and password == "admin":
            self.__logged_in_user = "Admin"
            self.login_frame.destroy()
            self.__show_admin_panel()
        elif username in self._user_data and self._user_data[username]["password"] == password:
            self.__logged_in_user = username
            self.login_frame.destroy()
            self.__show_main_window()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def load_products_txt(self):
        try:
            products = []
            with open("products.txt", "r") as file:
                for line in file:
                    name, price, image = line.strip().split(",")
                    products.append({"name": name, "price": int(price), "image": image})
            return products
        except FileNotFoundError:
            return []

    def __show_main_window(self):

        self.main_bg_frame = tkinter.Label(self.__froot, image=self.bg_image)
        self.main_bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = tkinter.Label(self.__froot)
        self.main_frame.place(x=400, y=50)
        # Product list - hele elave olucey

        self.products = self.load_products_txt()

        row = 0
        col = 0

        for product_info in self.products:
            product_obj = Product(product_info["name"], product_info["price"], product_info["image"])

            product_frame = tkinter.Frame(self.main_frame, bg="black")
            product_frame.grid(row=row, column=col, padx=10, pady=10)

            product_image = Image.open(product_obj.get_image())
            product_image = product_image.resize((200, 200))
            product_image = ImageTk.PhotoImage(product_image)

            image_label = tkinter.Label(product_frame, image=product_image)
            image_label.image = product_image
            image_label.pack()

            name_label = tkinter.Label(product_frame, text=product_obj.get_name(), bg="black", fg="white", font=15,pady=10)
            name_label.pack()

            price_label = tkinter.Label(product_frame, text=f"{product_obj.get_price()} AZN", bg="black", fg="white", pady=10)
            price_label.pack()

            buy_button = tkinter.Button(product_frame, text="Buy", padx=30, bg="#fec401", font=6,command=lambda prod=product_obj: self.__add_to_cart(prod))
            buy_button.pack()

            buy_button = tkinter.Button(product_frame, text="Show Cart", padx=30, bg="#fec401", font=6,command=lambda: self.__show_cart())
            buy_button.pack()

            col += 1
            if col > 5:
                col = 0
                row += 1

    def show_login_panel(self):
        self.main_frame.destroy()
        self.load_images()

        self.login_bg_frame = tkinter.Label(self.__froot, image=self.bg_image)
        self.login_bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.login_frame = tkinter.Frame(self.__froot, bg="black")
        self.login_frame.place(x=860, y=100)

        self.username_label = tkinter.Label(self.login_frame, text="Username:", bg="black", fg="white")
        self.username_label.grid(row=1, column=1, pady=5)
        self.username_entry = tkinter.Entry(self.login_frame)
        self.username_entry.grid(row=2, column=1, pady=5)

        self.password_label = tkinter.Label(self.login_frame, text="Password:", bg="black", fg="white")
        self.password_label.grid(row=3, column=1, pady=5)
        self.password_entry = tkinter.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=4, column=1, pady=5)

        self.login_button = tkinter.Button(self.login_frame, text="Login", command=self.__login)
        self.login_button.grid(row=5, column=1, pady=10)
        self.login_button.configure(pady=2, padx=27, background="#fec401", foreground="black", font=4)

        self.registration_button = tkinter.Button(self.login_frame, text="Registration",command=self.__show_registration_panel)
        self.registration_button.grid(row=6, column=1, pady=5)
        self.registration_button.configure(pady=2, padx=20, background="#fec401", foreground="black", font=4)

    def __show_cart(self):
        if self.__cart_frame:
            self.__cart_frame.destroy()

        self.__cart_frame = tkinter.Frame(self.__froot, height=1080, width=1920, bg="black")
        self.__cart_frame.pack()

        title_label = tkinter.Label(self.__cart_frame, text="Shopping Cart", bg="black", fg="white", font=20)
        title_label.pack(pady=20)

        total_price = sum([self.__get_product_price(product_name) * quantity for product_name, quantity in self.__cart.get_items().items()])

        for product_name, quantity in self.__cart.get_items().items():
            product_info = f"{product_name} - {self.__get_product_price(product_name)} AZN x {quantity}"
            product_label = tkinter.Label(self.__cart_frame, text=product_info, bg="black", fg="white", font=15)
            product_label.pack()

        total_label = tkinter.Label(self.__cart_frame, text=f"Total: {total_price} AZN", bg="black", fg="white",font=15)
        total_label.pack(pady=20)

        confirm_button = tkinter.Button(self.__cart_frame, text="Confirm", padx=30, bg="#fec401", font=6,command=self.__confirm_order)
        confirm_button.pack()

        self.__cart_frame.update_idletasks()

    def __get_product_price(self, product_name):
        for product in self.products:
            if product["name"] == product_name:
                return product["price"]
        return 0

    def __confirm_order(self):
        self.__cart_frame.destroy()
        messagebox.showinfo("Order Confirmation", "Your order has been confirmed! Thank you for shopping with us!")

    def __add_to_cart(self, product):
        if self.__logged_in_user:
            product_name = product.get_name()
            if product_name in [p["name"] for p in self.products]:
                if product_name in self.__cart.get_items():
                    self.__cart.add_item(product)
                else:
                    self.__cart.add_item(product)
                messagebox.showinfo("Cart", f"{product_name} has been added to your cart!")
            else:
                messagebox.showerror("Cart Error", "Invalid product selected")
        else:
            self.show_login_panel()
            messagebox.showinfo("Login","To buy a product you must first log into your account")

    def get_user_data(self):
        return self._user_data

    def __show_registration_panel(self):
        self.login_frame.destroy()
        self.load_images()
        RegistrationPanel(self.__froot, self)


class RegistrationPanel:
    def __init__(self, root, app):
        self.__root = root
        self.__app = app
        self._user_data = app.get_user_data()

        bg_width = 1920
        bg_height = 1090
        background_path = r"shop_bg.jpg"
        pil_image = Image.open(background_path)
        resized_bg_image = pil_image.resize((bg_width, bg_height))
        self.bg_image = ImageTk.PhotoImage(resized_bg_image)

        self.register_bg_frame = tkinter.Label(self.__root, image=self.bg_image)
        self.register_bg_frame.place(x=0, y=0)

        self.registration_frame = tkinter.Frame(self.__root, bg="black")
        self.registration_frame.grid(row=7, column=1, pady=5)
        self.registration_frame.place(x=860, y=100)

        self.username_label = tkinter.Label(self.registration_frame, text="Username:", bg="black", fg="white")
        self.username_label.grid(row=1, column=1, pady=5)
        self.username_entry = tkinter.Entry(self.registration_frame)
        self.username_entry.grid(row=2, column=1, pady=5)

        self.password_label = tkinter.Label(self.registration_frame, text="Password:", bg="black", fg="white")
        self.password_label.grid(row=3, column=1, pady=5)
        self.password_entry = tkinter.Entry(self.registration_frame, show="*")
        self.password_entry.grid(row=4, column=1, pady=5)

        self.confirm_password_label = tkinter.Label(self.registration_frame, text="Confirm Password:", bg="black",fg="white")
        self.confirm_password_label.grid(row=5, column=1, pady=5)
        self.confirm_password_entry = tkinter.Entry(self.registration_frame, show="*")
        self.confirm_password_entry.grid(row=6, column=1, pady=5)

        self.register_button = tkinter.Button(self.registration_frame, text="Register", command=self.__register)
        self.register_button.grid(row=7, column=1, pady=10)
        self.register_button.configure(pady=2, padx=27, background="#fec401", foreground="black", font=4)

        self.back_button = tkinter.Button(self.registration_frame, text="Back", command=self.__back_to_login)
        self.back_button.grid(row=8, column=1, pady=5)
        self.back_button.configure(pady=2, padx=20, background="#fec401", foreground="black", font=4)

    def __back_to_login(self):
        self.registration_frame.destroy()
        self.__app.show_login_panel()

    def __register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if username and password and confirm_password:
            if password == confirm_password:
                if username not in self.__app.get_user_data():
                    self.__app.get_user_data()[username] = {"password": password}
                    self.__app.save_user_data()
                    messagebox.showinfo("Registration", "Registration successful!")
                    self.__app.show_login_panel()
                    self.registration_frame.place_forget()
                else:
                    messagebox.showerror("Registration Error", "Username already exists")
            else:
                messagebox.showerror("Registration Error", "Passwords do not match")
        else:
            messagebox.showerror("Registration Error", "Please fill in all fields")


froot = tkinter.Tk()
app = AnimeStoreApp(froot)
froot.mainloop()
