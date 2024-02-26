from pyswip import Prolog

prolog = Prolog()

# 定义杯子
prolog.assertz("cup(1)")
prolog.assertz("cup(2)")
prolog.assertz("cup(3)")
prolog.assertz("cup(4)")

# 定义可能的饮料
drinks = ["beer", "cola", "coffee", "none"]

# 定义每个杯子的声明
# 第一个杯子："所有的杯子中都有啤酒"
prolog.assertz("statement(1, X) :- cup(X), drink_in_cup(X, beer)")

# 第二个杯子："本杯中有可乐"
prolog.assertz("statement(2, 2) :- drink_in_cup(2, cola)")

# 第三个杯子："本杯中没有咖啡"
prolog.assertz("statement(3, 3) :- not(drink_in_cup(3, coffee))")

# 第四个杯子："有些杯子中没有啤酒"
prolog.assertz("statement(4, X) :- cup(X), not(drink_in_cup(X, beer))")

# 只有一个声明是真的
prolog.assertz("one_true_statement(S) :- statement(S, X), not((statement(T, Y), T \= S))")

# 定义每个杯子可能含有的饮料
for cup in range(1, 5):
    for drink in drinks:
        prolog.assertz(f"drink_in_cup({cup}, {drink})")

# 查询哪个声明是真的
true_statement = list(prolog.query("one_true_statement(S)"))
print(true_statement)
