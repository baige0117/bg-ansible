class User:
    """A User Class"""
    def __init__(self, name, age, work, salary):
        self.name = name
        self.age = age
        self.work = work
        self.salary = salary

    def user_name(self):
        print(f"{self.name} is the name of the user")

    def user_age(self):
        print(f"{self.name} is {self.age} years old!")

    def user_work(self):
        print(f"{self.name} is a {self.work}!")

    def user_salary(self):
        print(f"{self.name}'s salary is SGD{self.salary}!")

class Company_A(User):
    def __init__(self, name, age, work, salary):
        super().__init__(name, age, work, salary)
        self.hobby = 'Swimming'

    def user_hobby(self):
        print(f"{self.name}'s hobby is {self.hobby}")


company_A_user = Company_A('John', 40, 'Software Engineer', 4000)
company_A_user.user_age()
company_A_user.user_hobby()