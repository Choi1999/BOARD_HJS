import pymysql

class BoardDAO:

    def init(self):
        self.host ="localhost"
        self.user ="board_user"
        self.port= 3306
        self.password ="board1234"
        self.database ="board_db"

    def get_connection(self):
        return pymysql.connect(
            host="localhost",
            user="board_user",
            password="board1234",
            database="board_db",
            charset="utf8mb4" # 
        )


    def select_all(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT *
        FROM board
        ORDER BY id DESC
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result
    # def insult(self):
    
    #     sql=="""
    #     insult 
    #     """
    # def select_content(self):
    #     Select content from board

    #     print(board[2])
    # def delete(self):
