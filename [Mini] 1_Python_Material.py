# -*- coding: utf-8 -*-
import sqlite3
from prettytable import PrettyTable

CURRENT_USER_ID = 1

## 구매기계 클래스
class Vending_Machine():
    def __init__(self, db_name, create=False, auto=False):
        ## 데이터베이스를 연결하는 코드
        self.connection_sqlite = sqlite3.connect(db_name)
        self.c = self.connection_sqlite.cursor()

        if create:
            self.mk_Table()
        if auto:
            self.auto_Insert_Table()

    ## 상품과 주문 테이블을 생성하는 코드
    def mk_Table(self):
        CREATE_PROP_TABLE = """
            CREATE TABLE props(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PROP_NAME TEXT NOT NULL,
                PRICE INT NOT NULL, 
                QUANTITY UNSIGNED INT NOT NULL,
                PROP_TYPE TEXT
            )
        """
        CREATE_USER_TABLE = """
            CREATE TABLE users(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL
            )
        """

        CREATE_BASKET_TABLE = """
            CREATE TABLE basket(
                ORDER_NUMBER INTEGER PRIMARY KEY AUTOINCREMENT,
                QUANTITY UNSIGNED INT NOT NULL,
                PROP_ID INT NOT NULL,
                BUYER_ID INT NOT NULL,
                SALE_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(PROP_ID) REFERENCES props(ID)
            )
        """
        self.c.execute(CREATE_PROP_TABLE)
        self.c.execute(CREATE_USER_TABLE)
        self.c.execute(CREATE_BASKET_TABLE)

    ## 상품 데이터를 추가하는 코드
    # c.execute("INSERT INTO ...
    def auto_Insert_Table(self):
        # 유저 추가
        self.c.execute("""
            INSERT INTO users (NAME)
            VALUES ('이호섭')
        """
        )
        self.c.execute("""
            INSERT INTO users (NAME)
            VALUES ('케인')
        """
        )
        self.c.execute("""
            INSERT INTO users (NAME)
            VALUES ('마리오')
        """
        )

        # 상품 추가
        self.c.execute("""
            INSERT INTO props (ID, PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES (1, '우유', 1500, 20, 'Dairy product')
        """)
        self.c.execute("""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ('사탕', 300, 100, 'Snack')
        """)
        self.c.execute("""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ('감자칩', 1000, 30, 'Snack')
        """)
        self.c.execute("""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ('라면', 800, 50, 'Food')
        """)
        self.c.execute("""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ('물', 800, 100, 'Water')
        """)
        self.c.execute("""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ('연어', 7000, 10, 'Sea food')
        """)
        self.c.execute("""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ('오이', 500, 40, 'Vegetable')
        """)
        self.c.execute("""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ('당근', 550, 40, 'Vegetable')
        """)
        self.connection_sqlite.commit()

    ## 새 user 추가
    def insert_User(self, user_name):
        self.c.execute(f"""
            INSERT INTO users (NAME)
            VALUES ({user_name})
        """)
        self.connection_sqlite.commit()

    ## 새 상품 추가
    def insert_Item(self, prop_name, price, quantity, prop_type="None"):
        self.c.execute(f"""
            INSERT INTO props (PROP_NAME, PRICE, QUANTITY, PROP_TYPE) 
            VALUES ({prop_name}, {price}, {quantity}, {prop_type})
        """)
        self.connection_sqlite.commit()

    ## 상품 업데이트
    def update_Item(self, prop_id, prop_name=False, price=False, quantity=False, prop_type=False):
        if prop_name:
            self.c.execute(f"""
                UPDATE props
                SET prop_name = {prop_name}
                WHERE id = {prop_id}
            """
            )
        if price:
            self.c.execute(f"""
                UPDATE props
                SET price = {price}
                WHERE id = {prop_id}
            """
            )
        if quantity:
            self.c.execute(f"""
                UPDATE props
                SET quantity = {quantity}
                WHERE id = {prop_id}
            """
            )
        if prop_type:
            self.c.execute(f"""
                UPDATE props
                SET prop_type = {prop_type}
                WHERE id = {prop_id}
            """
            )
        self.connection_sqlite.commit()

    ## 상품 수량 증감
    def update_Item_Quantity(self, prop_id, quantity):
        if quantity > 0:
            self.c.execute(f"""
                UPDATE props
                SET QUANTITY = QUANTITY + {quantity}
                WHERE id = {prop_id}
            """)
        else:
            self.c.execute(f"""
                UPDATE props
                SET QUANTITY = QUANTITY - {quantity}
                WHERE id = {prop_id}
            """)
        self.connection_sqlite.commit()

    ## user name getter
    def get_User(self, user_id):
        SQL_CURRENT_USER_QUERY = f"""
            SELECT name
            FROM users
            WHERE id = {user_id}
        """
        self.c.execute(SQL_CURRENT_USER_QUERY)
        user = self.c.fetchone()[0]

        return user

    ## 상품 목록을 표시하는 코드
    def print_Props_List(self):
        prop_table = PrettyTable()

        print('')
        SQL_PROP_LIST_QUERY = """
            SELECT ID, PROP_NAME, PRICE, QUANTITY
            FROM props
            WHERE QUANTITY > 0
        """
        self.c.execute(SQL_PROP_LIST_QUERY)
        stock_list = self.c.fetchall()
        prop_table.title = "상품 목록"
        prop_table.field_names = ["번호", "상품 이름", "가격", "개수"]
        prop_table.add_rows(stock_list)

        print(prop_table)

    ## 현재까지 주문 내역을 출력하는 코드
    def print_Sales_History(self, user_id):
        user_basket = PrettyTable()
        print('')
        print("현재까지 구매한 내역 보기")
        print('')

        SQL_BASKET_LIST_QUERY = f"""
            SELECT order_number, prop_name, basket.quantity
            FROM basket
            LEFT OUTER JOIN props
            ON basket.PROP_ID = props.ID
            WHERE buyer_id = {user_id}
        """
        self.c.execute(SQL_BASKET_LIST_QUERY)

        basket_list = self.c.fetchall()
        user_basket.title = f"회원번호 {user_id}번 님의 구매내역"
        user_basket.field_names = ["주문 번호", "상품 이름", "개수"]
        user_basket.add_rows(basket_list)

        print(user_basket)

    ## 구매하는 코드
    def selling(self, buy_item_id, buy_item_many):
        available = self.checking(buy_item_id, buy_item_many)
        if not available[0]:
            return available[1]

        try:
            # 구매한 수량만큼 재고에서 감소
            self.update_Item_Quantity(buy_item_id, buy_item_many)

            ## 주문 데이터를 db에 추가하는 코드
            # c.execute("INSERT INTO ...
            SQL_INSERT_BASKET = f"""
                INSERT INTO basket (QUANTITY, PROP_ID, BUYER_ID) 
                VALUES ({buy_item_many}, {buy_item_id}, {CURRENT_USER_ID})
            """
            self.c.execute(SQL_INSERT_BASKET)
            self.connection_sqlite.commit()

            return "구매에 성공했습니다. 감사합니다."
        except:
            # 오류시 롤백
            self.connection_sqlite.rollback()
            
            return "구매에 실패했습니다."

    ## 구매 가능한지 체크
    def checking(self, buy_item_id, buy_item_many):
        # 구매 가능한지 체크
        try:
            SQL_Quantity_Check = f"""
                SELECT QUANTITY
                FROM props
                WHERE id = {buy_item_id}
            """
            self.c.execute(SQL_Quantity_Check)
            in_stock = self.c.fetchone()[0]
            
            if in_stock < buy_item_many:
                return False, f"재고가 부족합니다. 최대 {in_stock}개 만큼만 구매할 수 있습니다."
            else:
                return True, "구매 가능합니다."
        except:
            return False, f"{buy_item_id}번 물건은 현재 구매가 불가능합니다."


my_machine = Vending_Machine(db_name="vending_machne.db", create=True, auto=True)
#my_machine = Vending_Machine(db_name="vending_machne.db")


user = my_machine.get_User(CURRENT_USER_ID)
print()
print(f"{user}님 환영합니다.")

while True:
    ## 상품 목록을 표시하는 코드
    my_machine.print_Props_List()

    ## 상품 번호와 주문 수량을 입력받는 코드
    while True:
        try:
            print()
            buy_item_id = int(input("구매하실 상품의 번호를 입력해주세요: "))
            print()
            buy_item_many = int(input("구매할 수량을 입력해주세요: "))
        except:
            print("잘못된 입력입니다.")
        else:
            break

    res = my_machine.selling(buy_item_id, buy_item_many)
    print()
    print(res)

    ## 현재까지 주문 내역을 출력하는 코드
    my_machine.print_Sales_History(CURRENT_USER_ID)
    
    print()
    sig = input("나가기 [Y]\n더 구매하기 [아무키]\n\n>>> ")

    if sig.upper() == 'Y':
        print()
        print("구매해주셔서 감사합니다.")
        break
