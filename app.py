from flask import Flask, render_template, request
from abc import ABC, abstractmethod

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/")


#   抽象類別：BaseEmployee

class BaseEmployee(ABC):
    """
    抽象類別 (Abstraction):
    - 無法直接被實例化，強制子類別實作 calculate_salary()。
    封裝 (Encapsulation):
    - 使用私有屬性 __employee_id, __name, __email 保護員工資料。
    - 外部透過 @property 讀取。
    """
    def __init__(self, employee_id: str, name: str, email: str):
        self.__employee_id = employee_id
        self.__name = name
        self.__email = email

    @property
    def employee_id(self):
        return self.__employee_id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @abstractmethod
    def calculate_salary(self) -> float:
        """
        多型 (Polymorphism):
        - 各子類別的薪資計算方式不同。
        """
        pass

    def get_basic_info(self) -> dict:
        return {
            "employee_id": self.__employee_id,
            "name": self.__name,
            "email": self.__email
        }

#  子類別 1：全職員工

class FullTimeEmployee(BaseEmployee):
    """
    繼承 (Inheritance) BaseEmployee
    多型：以「固定月薪」計算
    """
    def __init__(self, employee_id: str, name: str, email: str, monthly_salary: float):
        super().__init__(employee_id, name, email)
        self.__monthly_salary = monthly_salary

    def calculate_salary(self) -> float:
        # 全職員工以固定月薪
        return self.__monthly_salary



#  子類別 2：兼職員工

class PartTimeEmployee(BaseEmployee):
    """
    繼承 BaseEmployee
    多型：時薪 * 工時
    """
    def __init__(self, employee_id: str, name: str, email: str, hourly_wage: float, hours_worked: float):
        super().__init__(employee_id, name, email)
        self.__hourly_wage = hourly_wage
        self.__hours_worked = hours_worked

    def calculate_salary(self) -> float:
        return self.__hourly_wage * self.__hours_worked



#  子類別 3：實習生

class Intern(BaseEmployee):
    """
    繼承 BaseEmployee
    多型：固定津貼
    """
    def __init__(self, employee_id: str, name: str, email: str, stipend: float):
        super().__init__(employee_id, name, email)
        self.__stipend = stipend

    def calculate_salary(self) -> float:
        return self.__stipend


# 假資料庫：範例員工 (用字典模擬 DB)

employees_db = {
    "F001": FullTimeEmployee("F001", "Alice",  "alice@company.com", 50000),
    "F002": FullTimeEmployee("F002", "John",   "john@company.com", 60000),
    "P001": PartTimeEmployee("P001", "Bob",    "bob@company.com", 180, 100),
    "P002": PartTimeEmployee("P002", "Cindy",  "cindy@company.com", 200, 80),
    "I001": Intern("I001", "David",  "david@company.com", 8000),
}


#       Flask 路由


@app.route("/")
def home():
    """首頁：導到查詢薪資的功能"""
    return render_template("index.html")

@app.route("/check_salary", methods=["GET"])
def check_salary_form():
    """顯示查詢表單 (輸入員工編號)"""
    return render_template("salary_form.html")

@app.route("/check_salary", methods=["POST"])
def check_salary():
    """
    接收員工編號，查詢員工物件，計算其薪資並顯示
    """
    user_input_id = request.form.get("employee_id", "").strip().upper()
    employee_obj = employees_db.get(user_input_id)  # 查字典

    if employee_obj is None:
        # 找不到 -> 顯示找不到頁面
        return render_template("employee_not_found.html", emp_id=user_input_id)
    else:
        # 找到 -> 計算薪資
        basic_info = employee_obj.get_basic_info()
        calculated_salary = employee_obj.calculate_salary()
        # 以類別名稱分辨是 FullTime / PartTime / Intern
        emp_type = type(employee_obj).__name__
        return render_template("salary_result.html", info=basic_info, salary=calculated_salary, emp_type=emp_type)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


