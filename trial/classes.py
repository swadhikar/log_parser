
class Calc:
    pi = 3.14  # class variable is used to declare any var. that should be common across all objects

    def __init__(self, a, b):
        self.num_1 = a
        self.num_2 = b

    def multiply(self):
        mul = self.num_1 * self.num_2
        return mul


c1 = Calc(1, 2)
print(c1.num_1)
print(c1.num_2)


# print(c1.pi)
# print(c2.pi)
# print(c3.pi)


class Employee:
    def __init__(self, name, company):
        self.name = name
        self.company = company
        self._email = f'{self.name.lower()}@{self.company.lower()}.com'

    @property  # Converts a method to an instance attribute; Rule: Method should not have any args.
    def email(self):
        # self._email = f'{self.name.lower()}@{self.company.lower()}.com'
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email


e = Employee('Dilip', 'HCL')
print(e.name)
print(e.email)

e.email = 'dilip.c@hcl.com'
print(e.email)
