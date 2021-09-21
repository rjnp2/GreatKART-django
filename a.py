a = '''
Order Flow Explained
05:05
Making Order Model, Order Product model and Payment Model
07:54
Place Order View and Generate Order Number Part 01
09:39
Place Order View and Generate Order Number Part 02
21:09
Review Order Page Setup
08:23
Review Order Payment Page



'''

a = a.split('\n')[1::2]
for i in a:
    if i:
        i = '- ' + i
        print(i)