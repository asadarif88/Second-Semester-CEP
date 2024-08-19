from datetime import datetime
import hashlib
import os
from colorama import Fore, Style, init
import pyfiglet
import shutil
from abc import ABC, abstractmethod


class Exiting(BaseException):
    # the purpose of this class is to exit program on user demand with particular message displayed on screen
    pass


class UserRecordCheck(ABC):
    # this class is model for other classes which inherited it to implement the method of database check
    # in our program Signup and History classes utilizes this class for implementing database_check method
    @abstractmethod
    def database_check(self, a):
        pass


class Signup(UserRecordCheck):
    # This class is used to make the account of user
    def __init__(self):
        self.username = ''
        self.password = ''
        self.confirm_password = ''

    def user(self):
        # This method take username and password and also verify that this user exist in database through database_check
        # method and if user don't exist in database then it make user account
        records = {}
        while True:  # This loop runs till user not fulfilled the required conditions of username and password in
            # signing up
            self.username = input('Enter Your username (it should be greater than or equal to 7 characters,it should not contain any space and its first character should be alphabet): ')
            self.password = input('Enter your password (it should be greater than or equal to 7 characters and it should not contain any space): ')
            self.confirm_password = input('Confirm Password: ')
            if len(self.username) >= 7 and (self.username.find(' ') == -1) and self.username[0].isalpha():
                if len(self.password) >= 7 and (self.password.find(' ') == -1) and self.password == self.confirm_password:
                    h = hashlib.new("SHA256")
                    h.update(self.password.encode())
                    check = h.hexdigest()
                    records['Username'] = self.username
                    records['password'] = check
                    if self.database_check(records) == 'Make your Account':
                        self.store_database(records)
                        print('Account successfully created')
                        return records
                    else:
                        records.clear()
                        print('Account with same user name already exist')
                        print('Make your account with different user name')
                else:
                    if len(self.password) < 7:
                        print('Password is short of length')
                    elif self.password != self.confirm_password:
                        print('Entered password does\'nt match with confirm password')
                    else:
                        print('Password should not contain space')

            else:
                if len(self.username) < 7:
                    print('Username is short of length')
                elif not self.username[0].isalpha():
                    print('Username Should start with alphabet character')
                else:
                    print('Username should not contain space')

    def database_check(self, a):
        # this method check the user exist in database or not
        try:
            # here we are first checking that UserPrivateRecords file exist then we check user exist in that file, if
            # the file not exists the exception raised automatically that indicates user trying to signup has no
            # account before. Since database_check method used in both signup and login class, it returns appropriate
            # message according to the condition
            with open('UsersPrivateRecords.txt', 'r') as database:
                file_reading = database.readlines()
                for i in range(len(file_reading)):
                    information = file_reading[i]
                    info_without_space = information.strip()
                    correct_info = eval(info_without_space)
                    if correct_info['Username'] == a['Username']:
                        hash_obj = hashlib.new("SHA256")
                        hash_obj.update(a['password'].encode())
                        hash_pass = hash_obj.hexdigest()
                        if correct_info['password'] == hash_pass:
                            return 'account exists and same username and same password'
                        return 'account exists and same username and but not same password'
                return 'Make your Account'
        except FileNotFoundError:
            return 'Make your Account'

    @staticmethod
    def store_database(user_record):
        # This method stores the user account details in database file (UsersPrivateRecords.txt)
        with open('UsersPrivateRecords.txt', 'a') as file:
            file.write(str(user_record) + '\n')


class Login(Signup):
    def user(self):
        # This method takes username and password and after verification if user exist in database then it Log in the
        # user account and allow user to access the application
        records = {}
        while True:
            self.username = input('Enter Your account name : ')
            self.password = input('Enter your password: ')
            records['Username'] = self.username
            records['password'] = self.password
            if self.database_check(records) == 'account exists and same username and same password':
                print('Welcome back')
                return records
            elif self.database_check(records) == 'account exists and same username and but not same password':
                records.clear()
                print('Enter correct password\nTry Again')
                while True:  # this loop runs till user either not login or user want to return to options of signup,
                    # login and exit
                    user_demand = input('Do You want to continue logging up your account \'Press \'Y\' to continue or type \'done\'to return\' : ')
                    if user_demand.lower() == 'y':
                        break
                    elif user_demand.lower() == 'done':
                        return 'return'
                    else:
                        print('Enter \'Y\' or \'done\' not anything else')
            elif self.database_check(records) == 'Make your Account':
                print('Make your Account')
                return 'Make your Account'


class Products:
    # This class keep track of products.It displays products to user and updates products list as well.
    def __init__(self):
        self.products = {}

    def write_products_to_file(self):
        # This method write products to file
        filename = 'shop_items.txt'
        self.products = {"Bats": {"price": 1000, "quantity": 100},
                    "Tennis Ball": {"price": 50, "quantity": 100},
                    "Shuttlecock": {"price": 100, "quantity": 100},
                    "Nike Shoes": {"price": 700, "quantity": 100},
                    "Football": {"price": 2800, "quantity": 100},
                    "Sports glasses": {"price": 2500, "quantity": 100},
                    "Hard Ball": {"price": 25, "quantity": 100},
                    "Wicketkeeping Gloves": {"price": 899, "quantity": 100},
                    "Batting gloves": {"price": 1500, "quantity": 100},
                    "Pads": {"price": 20, "quantity": 100}}
        with open(filename, 'w') as file:
            for i in self.products:
                file.write(
                    f'Product Name : {i} , Quantity Available : {self.products[i]["quantity"]} , Price : {self.products[i]["price"]}\n')

    @staticmethod
    def upload_products():
        # This method display products to user when user entered display product option in main menu
        list_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        iter_obj = iter(list_)
        with open('shop_items.txt', 'r') as file:
            for i in file:
                print(f"{next(iter_obj)}.{i.strip()}")

    @staticmethod
    def upd_aft_shop(immediate_aft_shop, products_fr_file):
        # This method update product list when user buy some product
        for i in immediate_aft_shop:
            # in this loop, we are removing the quantity of products from products file to maintain stock
            # that updates when user shops
            products_fr_file[i]['quantity'] -= immediate_aft_shop[i]

        with open('shop_items.txt', 'w') as file:
            for h in products_fr_file:
                file.write(f'Product Name : {h} , Quantity Available : {products_fr_file[h]["quantity"]} , Price : {products_fr_file[h]["price"]}\n')

    @staticmethod
    def extract_from_products_file():
        # This method extract product list from product list text file in a way that helps in updating product list
        # and displaying product list to user
        list_for_printing = []
        dict_for_updating_products_purpose = {}
        with open('shop_items.txt', 'r') as file:
            for i in file:
                empty_dict = {}
                extract_line = i.strip()
                # below three lines of code extracting product name,product price, product quantity from the
                # line extracted from the file
                product_name = extract_line[15:extract_line.index(',') - 1]
                product_quantity = int(extract_line[extract_line.index(',') + 23:extract_line.rindex(',') - 1])
                product_price = int(extract_line[extract_line.rindex(',') + 10:])
                # below lines of code making dictionary of product name with dictionary of product quantity and
                # product price as value
                empty_dict['quantity'] = product_quantity
                empty_dict['price'] = product_price
                dict_for_updating_products_purpose[product_name] = empty_dict
                list_for_printing.append(extract_line)
        return list_for_printing, dict_for_updating_products_purpose

    def upd_product_list_aft_removal_from_cart(self, z):
        # This method update product list when user remove some products from its cart
        list_for_printing, dict_for_updating_products_purpose = self.extract_from_products_file()
        for q in z:
            # here we are increasing quantity of product in products list by checking how much quantity of product user
            # removed from the cart
            if q in dict_for_updating_products_purpose:
                dict_for_updating_products_purpose[q]['quantity'] += z[q]
        with open('shop_items.txt', 'w') as f:
            for h in dict_for_updating_products_purpose:
                f.write(f'Product Name : {h} , Quantity Available : {dict_for_updating_products_purpose[h]["quantity"]} , Price : {dict_for_updating_products_purpose[h]["price"]}\n')


class ShoppingCart(Products):
    # This class manages user and helps user in adding products to cart as well as removing products from cart,and
    # it also manages user checkout and history.
    def __init__(self, a):
        super().__init__()
        self.cart = {}
        self.history_obj = a

    def user_products(self):
        # This method display products to user when user want to add product to its cart and also products to cart.
        list_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        iter_obj = iter(list_)
        list_for_printing, dict_for_updating_products_purpose = self.extract_from_products_file()
        for products in list_for_printing:
            print(f'{next(iter_obj)}.{products}')
        for_selection = {'1': "Bats", '2': "Tennis Ball", '3': "Shuttlecock", '4': "Nike Shoes", '5': "Football",
                         '6': "Sports glasses", '7': "Hard Ball", '8': "Wicketkeeping Gloves", '9': "Batting gloves",
                         '10': "Pads"}  # this dictionary helps in making easier for user to enter product by just
        # product number
        while True:  # this loop runs till user enter done to return to main menu
            try:
                product_number = input('Enter your product number or type \'done\' to return to main menu : ')
                if product_number.lower() == 'done':
                    pass
                elif product_number.isdigit():
                    pass
                else:
                    raise ValueError('Enter integer only without any space or type \'done\' properly to return to main menu')
            except ValueError as ve:
                print(ve)
            else:
                # here we check that product exists in products list file then we proceed further
                if product_number in for_selection and dict_for_updating_products_purpose[for_selection[product_number]]['quantity'] != 0:
                    while True:
                        try:
                            user_quantity = input('Enter quantity : ')
                            # here we are checking that user entered integer or not
                            assert user_quantity.isdigit()
                            user_quantity = int(user_quantity)

                        except AssertionError:
                            print('Enter integer only')
                        else:
                            if user_quantity > 0:
                                if dict_for_updating_products_purpose[for_selection[product_number]]['quantity'] < user_quantity and (user_quantity != 0):
                                    print('Enter quantity less than available quantity')
                                elif user_quantity == 0:
                                    print('Enter valid quantity')
                                else:
                                    if self.cart and for_selection[product_number] in self.cart:
                                        shopped_product = {}
                                        shopped_product[for_selection[product_number]] = user_quantity
                                        self.upd_aft_shop(shopped_product, dict_for_updating_products_purpose)
                                        self.cart[for_selection[product_number]]['quantity'] += user_quantity
                                        print(f'{user_quantity} more pieces of {for_selection[product_number]} are added to the cart')
                                        break
                                    else:
                                        product_dict = {}
                                        product_dict['quantity'] = user_quantity
                                        product_dict['price'] = dict_for_updating_products_purpose[for_selection[product_number]]['price']
                                        shopped_product = {}
                                        shopped_product[for_selection[product_number]] = user_quantity
                                        self.upd_aft_shop(shopped_product, dict_for_updating_products_purpose)
                                        self.cart[for_selection[product_number]] = product_dict
                                        print(f'{user_quantity} pieces of {for_selection[product_number]} are added to the cart')
                                        break
                            else:
                                print('Enter correct quantity')
                elif product_number.lower() == 'done':
                    break
                elif product_number not in for_selection:
                    print('Enter Valid Key')
                else:
                    print('Product is short in stock ')

    def remove_product(self):
        # This method remove products from user cart and also update product list through parent class method
        # (upd_product_list_aft_removal_from_cart)
        removed_products = {}
        completely_removed_products = []
        if len(self.cart) == 0:
            print('Your cart is empty')
        elif self.cart:
            while True:
                try:
                    for_selection = {'1': "Bats", '2': "Tennis Ball", '3': "Shuttlecock", '4': "Nike Shoes",
                                     '5': "Football", '6': "Sports glasses", '7': "Hard Ball",
                                     '8': "Wicketkeeping Gloves", '9': "Batting gloves", '10': "Pads"}
                    remove_product_number = input('Enter your product number or type \'done\' to return to main menu: ')
                    assert remove_product_number.isdigit() or remove_product_number.lower() == 'done'
                except AssertionError:
                    print('Enter integer only without any space or type \'done\' properly to return to main menu ')
                else:
                    if remove_product_number in for_selection:
                        if for_selection[remove_product_number] in self.cart:
                            while True:
                                try:
                                    remove_product_quantity = input('Enter quantity : ')
                                    assert remove_product_quantity.isdigit()
                                    remove_product_quantity = int(remove_product_quantity)
                                except AssertionError:
                                    print('Please enter positive integer value')
                                else:
                                    if remove_product_quantity > 0:
                                        if self.cart[for_selection[remove_product_number]]['quantity'] == remove_product_quantity:
                                            removed_products[for_selection[remove_product_number]] = remove_product_quantity
                                            self.cart.pop(for_selection[remove_product_number])
                                            print(f'{for_selection[remove_product_number]} completely removed from your cart')
                                            completely_removed_products.append(for_selection[remove_product_number])
                                            break
                                        elif self.cart[for_selection[remove_product_number]][
                                            'quantity'] > remove_product_quantity:
                                            removed_products[for_selection[remove_product_number]] = remove_product_quantity
                                            self.cart[for_selection[remove_product_number]][
                                                'quantity'] -= remove_product_quantity
                                            print(f'{remove_product_quantity} pieces of {for_selection[remove_product_number]} removed from your cart')
                                            break
                                        else:
                                            print(f'Enter quantity less than or equal to quantity of {for_selection[remove_product_number]} present in your cart')
                                    else:
                                        print('Enter valid quantity')
                        else:
                            print('You did\'nt bought this product')
                    elif remove_product_number.lower() == 'done':
                        break
                    else:
                        print('Enter valid product number')
        if removed_products:
            self.upd_product_list_aft_removal_from_cart(removed_products)

    def user_checkout(self):
        # This method update user history file and clears the user products cart
        total_bill = 0
        string = ''
        string1 = ''
        for i in self.cart:
            string1 += f'Product : {i} Price : Rs{self.cart[i]["price"]}  Quantity Bought : {self.cart[i]["quantity"]}  Subtotal : {self.cart[i]["price"]*self.cart[i]["quantity"]}\n'
            string += f'{i} -- {self.cart[i]["quantity"]} pieces --Rs{self.cart[i]["price"]*self.cart[i]["quantity"]}\n'
            total_bill += (self.cart[i]["price"]*self.cart[i]["quantity"])
        string += f'Total_bill is Rs{total_bill}'
        string1 += f'Total : Rs{total_bill}'
        self.history_obj.checkout(string1)  # here we are calling checkout method of history class that write user
        # shopping history to user file
        print('Your Shopping cart :')
        print(string)
        self.cart.clear()

    def user_cart(self):
        # This method display the user his/her shopping cart
        total_bill = 0
        string = ''
        for i in self.cart:
            string += f'{i} -- {self.cart[i]["quantity"]} pieces --Rs{self.cart[i]["price"] * self.cart[i]["quantity"]}\n'
            total_bill += (self.cart[i]["price"] * self.cart[i]["quantity"])
        string += f'Total_bill is Rs{total_bill}'
        print('Your shopping cart :')
        print(string)

    def user_history(self):
        # This method displays the history to user
        self.history_obj.history_retrieval()


class History(UserRecordCheck):
    def __init__(self, a):
        self.user_file = ''
        self.user_dict = a

    def database_check(self, user_data):
        # This method checks user exist and then update user file according and if user not exists it makes user file
        # and update it accordingly.
        datetime_obj = datetime.now()
        time_obj = datetime_obj.time()
        date_obj = datetime_obj.date()
        formatted_date = date_obj.strftime('%A,%b %d,%Y')
        f_formatted_date = f'History of {formatted_date}'
        self.user_file = user_data + '.txt'
        if os.path.exists(self.user_file):
            user_data_list = self.user_data(self.user_file)
            if f_formatted_date in user_data_list:
                with open(self.user_file, 'a') as file:
                    file.write(f"\nAccount login time : {time_obj.strftime('%I:%M %p')}")
            else:
                with open(self.user_file, 'a') as file:
                    file.write(f"\nEND\n{f_formatted_date}\nAccount login time : {time_obj.strftime('%I:%M %p')}")
        else:
            with open(self.user_file, 'a') as file:
                file.write(f"{f_formatted_date}\nAccount Creation time : {time_obj.strftime('%I:%M %p')}")

    @staticmethod
    def user_data(user_file):
        # This method extract file information of user
        user_data_list = []
        with open(user_file, 'r') as file:
            for i in file:
                user_data_list.append(i.strip())
        return user_data_list

    def history_retrieval(self):
        # This key method of our additional feature to display particular date history to user.It displays history to
        # user according to his/her demand
        self.user_file = self.user_dict['Username']+'.txt'
        while True:
            user_input = input('For complete history enter \'c\' or for particular date history enter \'p\' or type \'done\' to return to main menu  : ')
            if user_input.lower() == 'c':
                user_complete_shopping_history = self.user_data(self.user_file)
                if 'END' in user_complete_shopping_history:
                    for p in range(user_complete_shopping_history.count('END')):
                        user_complete_shopping_history.remove('END')
                for i in user_complete_shopping_history:
                    print(i)
                break
            elif user_input.lower() == 'p':
                while True:
                    try:
                        print('Enter in the format \'dd-mm-yy\' e.g is \'3-6-2024\' or \'03-06-2024\'')
                        user_entered_date = input('Enter \'date\' in the above format  or type \'done\' to return to back step: ')
                        datetime_obj = datetime.now()
                        if user_entered_date.lower() == 'done':
                            break
                        else:
                            # In this else block we are checking user entered date in correct format,then we are
                            # checking that entered date is future date or not
                            user_date_into_datetime_obj = datetime.strptime(user_entered_date, "%d-%m-%Y")
                            user_datetime_obj = datetime(year=user_date_into_datetime_obj.year, month=user_date_into_datetime_obj.month, day=user_date_into_datetime_obj.day, hour=user_date_into_datetime_obj.hour, minute=user_date_into_datetime_obj.minute)
                            time_difference = datetime_obj-user_datetime_obj
                            string_time_difference = str(time_difference)
                            if ',' in string_time_difference:
                                split_time_difference = string_time_difference.split(',')
                                split_days = split_time_difference[0].split()
                                total_days = int(split_days[0])
                                assert total_days > 0
                    except AssertionError:
                        print('The date you entered is future date.Please Enter valid date')
                        break
                    except Exception:
                        print('Enter date in correct format')
                    else:
                        # here we are checking that particular date exist in user file then we will display everything
                        # of that date to user that is stored in user file like login or account creation time and
                        # user shopping history
                        user_file_data = self.user_data(self.user_file)
                        formatted_user_date = user_date_into_datetime_obj.strftime('%A,%b %d,%Y')
                        date_checker_string = f'History of {formatted_user_date}'
                        if date_checker_string in user_file_data:
                            index_of_string = user_file_data.index(date_checker_string)
                            extracted_user_file_data = user_file_data[index_of_string:]
                            if 'END' in extracted_user_file_data:
                                index_of_end = user_file_data.index('END')
                                for o in user_file_data[index_of_string:index_of_end]:
                                    print(o)
                                break
                            else:
                                for o in user_file_data[index_of_string:]:
                                    print(o)
                                break
                        else:
                            print('History dont exist')
                            break

            elif user_input.lower() == 'done':
                break
            else:
                print('Enter correct letter')

    def checkout(self, user_shopping):
        # This method write checkout time in user individual file
        checkout_datetime_obj = datetime.now()
        checkout_time = checkout_datetime_obj.time()
        self.user_file = self.user_dict['Username'] + '.txt'
        if os.path.exists(self.user_file):
            with open(self.user_file, 'a') as file:
                file.write(f"\ncheckout time : {checkout_time.strftime('%I:%M %p')}\n{user_shopping}")


class ApplicationManager:
    # This class manages the whole application
    def __init__(self):
        # In this constructor method , objects of signup or login class created,this method utilizes history method
        # of ApplicationManager class and update or create user file accordingly.It also utilizes screen_clear method
        # to clear screen on user demand as well as utilizes display_welcome_message method to display welcome message
        # to user at start
        # .It also utilizes start_load_products method to upload products into products file,and it also displays
        # menu to user by utilizing options method.
        self.signup = Signup()
        self.login = Login()
        self.display_welcome_message()
        try:
            self.selection()
            self.start_load_products()
            self.options()
        except Exiting as e:
            print(e)

        except BaseException:
            print('\nDue to some problem\nApplication is exiting')

    def history(self):
        # This method create History object and with the help of that object create user file if user not exist and
        # write user account creation time and date or login time in user file in case user
        # exists and also create ShoppingCart object and pass history object to it to update history of user as user
        # checkouts.
        self.user_history = History(self.user_dict)
        self.user_history.database_check(self.user_dict['Username'])
        self.user_cart = ShoppingCart(self.user_history)

    def options(self):
        # This method display menu to user and takes user selection and manage program flow accordingly
        print('Select Option from below :\n1.Display Products\n2.Make your cart\n3.Remove items from your cart\n4.Show My cart\n5.Show My history\n6.Checkout\n7.Clear Screen\n8.Exit')
        selection_dict = {1: 'self.user_cart.upload_products()', 2: 'self.user_cart.user_products()', 3: 'self.user_cart.remove_product()', 4: 'self.user_cart.user_cart()', 5: 'self.user_cart.user_history()', 6: 'self.user_cart.user_checkout()', 7: 'self.screen_clear()', 8: 'Exit'}
        while True:
            try:
                user_selection = input('Enter your selection "(1-8)" : ')
                if user_selection.isdigit():
                    pass
                else:
                    raise ValueError('Enter only integer')
            except Exception as ve:
                print(ve)

            else:
                if int(user_selection) in selection_dict and user_selection == '8':
                    raise Exiting("Thanks for visiting our store\nExiting")
                elif int(user_selection) in selection_dict:
                    eval(selection_dict[int(user_selection)])
                else:
                    print('enter valid option')

    def start_load_products(self):
        # This method check if shop_items (products file) exists in directory.If file does not exist,
        # it makes file through user cart object
        if os.path.isfile('shop_items.txt'):
            pass
        else:
            self.user_cart.write_products_to_file()

    def selection(self):
        while True:  # This loop runs till user not entered valid option
            print('Select the option from below :')
            print('1. Signup')
            print('2. Login')
            print('3. Exit')
            user_input = input('Enter your selection (1-3) : ')
            if user_input.lower() == '1':
                self.user_dict = self.signup.user() # here dictionary of user information that contains username and
                # user password returned
                self.history()  # it helps in maintaining user history
                break
            elif user_input.lower() == '2':
                self.user_dict = self.login.user()
                if self.user_dict == 'Make your Account':
                    print('Account does\'nt exist')
                elif self.user_dict == 'return':
                    pass
                else:
                    self.history()
                    break
            elif user_input.lower() == '3':
                raise Exiting('Exiting')
            else:
                print('Enter valid option')

    @staticmethod
    def screen_clear():
        # This method clear screen on user command
        # The below program statement check if operating system is windows or other and then clear screen accordingly
        os.system('cls' if os.name == 'nt' else 'clear')
        # we display menu to user after clearing screen so user can see which option he wants to choose
        print(
            'Select Option from below :\n1.Display Products\n2.Make your cart\n3.Remove items from your cart\n4.Show My cart\n5.Show My history\n6.Checkout\n7.Clear Screen\n8.Exit')

    @staticmethod
    def display_welcome_message():
        init(autoreset=True)

        # Generate ASCII art
        ascii_art = pyfiglet.figlet_format("Welcome To ASA Sports Store")

        # Try to get the terminal width
        try:
            terminal_width = shutil.get_terminal_size().columns
        except:
            # Default width if running in an environment where terminal size cannot be detected
            terminal_width = 80

        # Split the ASCII art into lines
        ascii_art_lines = ascii_art.split('\n')

        # Center each line and print
        for line in ascii_art_lines:
            print(Fore.GREEN + Style.BRIGHT + line.center(terminal_width))


application = ApplicationManager()