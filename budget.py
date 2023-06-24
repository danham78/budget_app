class Category:

    def __init__(self, name):
        self.ledger = []
        self.ledger_total = 0
        self.name = str(name)
        self.withdrawal_total = 0

    def __str__(self):
        self.stars_left = '*' * ((30 - len(self.name)) // 2)
        self.title = f'{self.stars_left}{self.name}'
        self.total = self.ledger_total
        self.list = [(item['description'] + (' ' * 23), item['amount'])
                    for item in self.ledger]
        self.itemised = ''
        for item in self.list:
            self.itemised += f'{item[0][:23]}{f"{item[1]:.2f}":>7}\n'
        while len(self.title) < 30:
            self.title += '*'
        return f'{self.title}\n{self.itemised}Total: {self.total}'

    def deposit(self, amount, description=''):
        self.amount = amount
        self.description = description
        self.ledger.append({
        'amount': self.amount,
        'description': self.description
        })
        self.ledger_total += self.amount

    def withdraw(self, amount, description=''):
        self.amount = amount
        self.description = description
        if self.check_funds((self.amount)) == True:
            self.ledger.append({
            'amount': -self.amount,
            'description': self.description
        })
            self.ledger_total -= self.amount
            self.withdrawal_total += self.amount
            return True
        else:
            return False

    def get_balance(self):
        return self.ledger_total

    def transfer(self, amount, budget_category):
        self.amount = amount
        self.budget_category = budget_category
        if self.check_funds(self.amount) is True:
            self.withdraw(amount, f'Transfer to {budget_category.name}')
            budget_category.deposit(amount, f'Transfer from {self.name}')
        # takes transfer amount out of withdrawal total when withdraw is called so that transfers aren't counted in the chart
            self.withdrawal_total -= amount
            return True
        else:
            return False

    def check_funds(self, amount):
        self.amount = amount
        if self.amount > self.ledger_total:
            return False
        else:
            return True


def create_spend_chart(categories):
    cat_list_str = [i.name for i in categories]
    longest_cat = max(cat_list_str, key=len)
    cat_one_spend = categories[0].withdrawal_total
    if len(categories) >= 2:
        cat_two_spend = categories[1].withdrawal_total
    else:
        cat_two_spend = 0
    if len(categories) >= 3:
        cat_three_spend = categories[2].withdrawal_total
    else:
        cat_three_spend = 0
    if len(categories) == 4:
        cat_four_spend = categories[3].withdrawal_total
    else:
        cat_four_spend = 0
    def cat_spend_percent(category):
        return category / (cat_one_spend + cat_two_spend + cat_three_spend +
                    cat_four_spend) * 100

    cat_one_percent = cat_spend_percent(cat_one_spend)
    cat_two_percent = cat_spend_percent(cat_two_spend)
    cat_three_percent = cat_spend_percent(cat_three_spend)
    cat_four_percent = cat_spend_percent(cat_four_spend)

    title = 'Percentage spent by category'
    column_one_list = [
        '100|', ' 90|', ' 80|', ' 70|', ' 60|', ' 50|', ' 40|', ' 30|', ' 20|',
        ' 10|', '  0|'
    ]
    while len(column_one_list) < (len(longest_cat) + 12):
        column_one_list.append('    ')
    columns_list = [column_one_list]
    column_two_list = [
        ' o ' if cat_one_percent >= percent else '   '
        for percent in range(100, -10, -10)
    ] + ['---'] + [f' {letter} ' for letter in categories[0]
                .name] + [
        '   ' for i in range(len(longest_cat) - len(categories[0].name))
    ]
    columns_list.append(column_two_list)
    column_three_list = ['   ' for i in range(len(longest_cat) + 12)]
    if len(categories) >= 2:
        column_three_list = [
        ' o ' if cat_two_percent >= percent else '   '
        for percent in range(100, -10, -10)
        ] + ['---'] + [f' {letter} ' for letter in categories[1].name] + [
        '   ' for i in range(len(longest_cat) - len(categories[1].name))
        ]
    columns_list.append(column_three_list)
    column_four_list = ['   ' for i in range(len(longest_cat) + 12)]
    
    if len(categories) >= 3:
        column_four_list = [
        ' o ' if cat_three_percent >= percent else '   '
        for percent in range(100, -10, -10)
        ] + ['---'] + [f' {letter} ' for letter in categories[2].name] + [
        '   ' for i in range(len(longest_cat) - len(categories[2].name))
        ]
    columns_list.append(column_four_list)
    column_five_list = ['   ' for i in range(len(longest_cat) + 12)]
    
    if len(categories) == 4:
        column_five_list = [
        ' o ' if cat_four_percent >= percent else '   '
        for percent in range(100, -10, -10)
        ] + ['---'] + [f' {letter} ' for letter in categories[3].name] + [
        '   ' for i in range(len(longest_cat) - len(categories[3].name))
        ]
        columns_list.append(column_five_list)
    
    column_six_list = [' ' for percent in range(100, -10, -10)] + ['-'] + [' ' for i in range(len(longest_cat))]
    columns_list.append(column_six_list)
    chart_columns = ''
    for i in range(len(longest_cat) + 12):
        for column in columns_list:
            chart_columns += column[i]
        chart_columns += '\n'
    chart = f'{title}\n{chart_columns}'.rstrip('\n')
    return chart

food = Category('Food')
entertainment = Category('Entertainment')
clothing = Category('Clothing')
business = Category('Business')


food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
actual = create_spend_chart([business, food, entertainment])
print(actual)
#print(clothing)
#print(food)


