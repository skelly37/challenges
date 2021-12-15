def extended_gcd(a, b): 
   if a == 0 :  
        return b,0,1
             
    gcd,x1,y1 = extended_gcd(b%a, a) 
     
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd, x, y

if __name__ == "__main__":
	print(extended_gcd(26513, 32321))

