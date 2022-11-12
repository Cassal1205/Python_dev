EXIT = ["Exit"]
LIST = ["List"]
list_of_products = ["Milk", "Bread", "Sugar", "Chicken", "Coke", "Candies", "Cookies", "Cereal", "Nesquik",
                    "Yoghurt", "Juice", "Coffee", "Nachos", "Shampoo", "Chips"]


def ask_to_user():
    return input("\nInsert an item to add to the shop list. Type '{}' to exit the program or \
'{}' to show the list of eligible products: ".format(EXIT[0], LIST[0]))


def add_item(input_user, shop_list):
    if input_user.lower() in [a.lower() for a in LIST]:
        print("Eligible items: ")
        for a in list_of_products:
            print("-" + a)
    elif input_user.lower() in [a.lower() for a in list_of_products]:
        if input_user.lower() in [a.lower() for a in shop_list]:
            print("'{}' is already on the shop list!".format(input_user.capitalize()))
        else:
            shop_list.append(input_user.capitalize())
            print("{} added. Current shop list: ".format(input_user.capitalize()))
            for a in shop_list:
                print("-" + a)
    elif input_user.lower() not in [a.lower() for a in list_of_products]:
        print("'{}' is not an eligible item. Try again.".format(input_user.capitalize()))


def file_creation(shop_list):
    file_name = input("\nInsert a name for the file: ")
    with open(file_name + ".txt", "w") as my_fyle:
        my_fyle.write("\n".join(shop_list))


def main():
    shop_list = []
    input_user = ask_to_user()
    while input_user.lower() not in [a.lower() for a in EXIT]:
        add_item(input_user, shop_list)
        input_user = ask_to_user()
    file_creation(shop_list)


if __name__ == "__main__":
    main()
