import sys

from model import convert_to_model

def main():
    num_1 = int(sys.argv[1])
    num_2 = int(sys.argv[2])
    num_3 = int(sys.argv[3])
    num_4 = int(sys.argv[4])
    num_5 = int(sys.argv[5])
    num_list = [
                num_1,
                num_2,
                num_3,
                num_4,
                num_5
               ]
    print(convert_to_model(num_list))

if __name__ == "__main__":
    main()