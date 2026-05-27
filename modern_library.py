import json
import os

DATA_FILE = "books.json"


def load_books():
    """從 JSON 檔案讀取書籍資料"""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("資料檔格式錯誤，已使用空資料開始")
        return []


def save_books(books):
    """把書籍資料存回 JSON 檔案"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


def isbn_exists(books, isbn):
    """檢查 ISBN 是否已存在"""
    for book in books:
        if book["isbn"] == isbn:
            return True
    return False


def add_book(books, command):
    """新增書籍，格式：add 書名/ISBN/狀態"""
    try:
        data = command[4:].split("/")

        if len(data) != 3:
            print("Format Error，正確格式：add 書名/ISBN/狀態")
            return

        title = data[0].strip()
        isbn = data[1].strip()
        status = data[2].strip()

        if title == "" or isbn == "" or status == "":
            print("Format Error，資料不能空白")
            return

        if isbn_exists(books, isbn):
            print("ISBN Exist")
            return

        book = {
            "title": title,
            "isbn": isbn,
            "status": status
        }

        books.append(book)
        print("Success")

    except Exception as error:
        print("新增書籍時發生錯誤:", error)


def show_books(books):
    """顯示所有書籍"""
    if len(books) == 0:
        print("目前沒有書籍資料")
        return

    for book in books:
        print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")


def borrow_book(books, command):
    """借書，格式：borrow ISBN"""
    target_isbn = command[7:].strip()

    if target_isbn == "":
        print("Format Error，正確格式：borrow ISBN")
        return

    for book in books:
        if book["isbn"] == target_isbn:
            if book["status"] == "borrowed":
                print("這本書已經被借出")
                return

            book["status"] = "borrowed"
            print("Updated")
            return

    print("找不到此 ISBN 的書")


def show_help():
    """顯示使用說明"""
    print("可用指令：")
    print("add 書名/ISBN/狀態")
    print("show")
    print("borrow ISBN")
    print("help")
    print("exit")


def main():
    books = load_books()

    print("=== 圖書管理系統 v1.0 (Modern) ===")
    show_help()

    while True:
        command = input("> ").strip()

        if command == "":
            continue

        if command == "exit":
            save_books(books)
            print("系統關閉")
            break

        elif command.startswith("add "):
            add_book(books, command)

        elif command == "show":
            show_books(books)

        elif command.startswith("borrow "):
            borrow_book(books, command)

        elif command == "help":
            show_help()

        else:
            print("Unknown Command，請輸入 help 查看可用指令")


if __name__ == "__main__":
    main()