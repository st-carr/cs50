import sys
import crypt

def main():
    _password = ["", "", "", ""]
    _str = ""
    _str_one = ""
    _str_two = ""
    _str_three = ""
    my_hash = sys.argv[1]
    
    if len(sys.argv) != 2:
        print("Usage: file hash")
        exit(1)

    for counter in range(4):
        for a in range(65, 123):
            for b in range(65, 123):
                for c in range(65, 123):
                    for d in range(65, 123):
                        _password[0] = chr(d)
                        if counter == 1:
                            _password[1] = chr(c)
                        elif counter == 2:
                            _password[1] = chr(c)
                            _password[2] = chr(b)             
                        elif counter == 3:
                            _password[1] = chr(c)
                            _password[2] = chr(b) 
                            _password[3] = chr(a)
                        
                        _str = "".join(_password)
                        

                        
                        if crypt.crypt(_str, "50") == my_hash:
                            print("MATCH: {}".format(_str))
                            exit(0)                        
    print("no match")
    exit(2)
    
    
if __name__ == "__main__":
    main()