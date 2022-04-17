def read_user_info():
    with open("userinfo.txt") as file:
        data = file.read()
        lines = data.split("\n")
        return lines

def main():
    print(read_user_info())
    if read_user_info()==['']:
        import login
    else:
        print(1231212312)
        import main_window


if __name__ == "__main__":
    main()