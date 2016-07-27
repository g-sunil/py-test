li = [1, 2, 3]
a = li[1]
print a, id(a)
b = li[:][1]
print b, id(b)
print id(li), id(li[:])
a = 1
print id(a), id(b), a, b


some_guy = 'Fred'

first_names = []
first_names.append(some_guy)

another_list_of_names = first_names
another_list_of_names.append('George')
some_guy = 'Bill'

print (some_guy, first_names, another_list_of_names)


first_names = ['Fred', 'George', 'Bill']
last_names = ['Smith', 'Jones', 'Williams']
name_tuple = (first_names, last_names)

first_names.append('Igor')
print name_tuple


def foo(bar):
    bar = 'new value'
    print bar

answer_list = 'old value'
foo(answer_list)
print(answer_list)
