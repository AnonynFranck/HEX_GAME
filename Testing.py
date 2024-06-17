temp = 0
aux = 0
for i in range(121, 0, -2):
    temp += 1
    aux += i

print("Nodos: " + str(aux))
print(temp)

t = 0
for i in range(1,temp+1):
    t += (121 - 2*(i-1))
print(t)