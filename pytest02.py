#test something:
print('''first:line1
... line2
... line3''')
print('''second:line1
line2
line3''')
print(r'''third:line1
line2
line3''')
a = 123     # a是整数
print('a=',a)
a = 'ABC'   # a变为字符串
print('a=',a)
b = a
a = 'XYZ'
print('a=',a)
print('b=',b)
n = 123
f = 456.789
s1 = " 'hello,world' "
s2 = r" 'hello,\'Adam\' ' "
s3 = "r'hello,\"Bart\" ' "
s4 = "r'\'\'Hello,\nLisa!'\'\' "
print ('''
n = %s
f = %s
s1 = %s
s2 = %s
s3 = %s
s4 = %s'''%(n,f,s1,s2,s3,s4))
