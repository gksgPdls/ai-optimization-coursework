#purchase_price, selling_price 입력받음
purchase_price=int(input("Enter purchase price: "))
selling_price=int(input("Enter selling price: "))

#markup, percentage_markup, profit_margin 계산함
markup=selling_price-purchase_price
percentage_markup=(markup/purchase_price)*100
profit_margin=(markup/selling_price)*100

#출력
print("Markup: ${:.1f}".format(markup))
print("Percentage markup: {:.1f}%".format(percentage_markup))
print("Profit margin: {:.2f}%".format(profit_margin))