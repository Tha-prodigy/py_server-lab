def gen_numbers():
   l = [1,2,3,4]
   yield l

gen = gen_numbers()
print(next(gen))