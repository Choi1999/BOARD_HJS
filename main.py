from board_dao import *

board_dao=BoardDAO()

board_dao.get_connection

while True:
    print("="*40)
    print("1.목록  2.등록  3.내용  4.삭제  0.종료")
    print("="*40)

    menu=input("선택> ")

    if menu==("0"):
        break
    elif menu==("1"):
        boards=board_dao.select_all()
        for board in boards:
            print(board[0],
                  board[1],
                  board[3],
                  board[4])
    elif menu==("2"):
      pass
      # insults=board_dao.insult()
    elif menu==("3"):
        pass
    elif menu==("4"):
        pass
    else:
        print("다시")
print("게시판 종료")