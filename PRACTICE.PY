a="255248"
if a==a[::-1]:
    print("yes")
else:
    print("no")

for i in range(int(len(a)/2)):
    if a[i]!=a[-1-i]:
        print("no")
        break
    
#reverse
print(a[::-1])
b=""
for i in range(len(a)):
    b=b+a[-1-i]
print(b)

#REMOVE DUPLICATE
def my_function(x):
  print(set(x))
  return list(dict.fromkeys(x))

mylist = my_function(["a", "b", "a", "c", "c"])

print(mylist)