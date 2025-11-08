#!/usr/bin/env python3

from src.primitive_db.engine import welcome

def main():
    print('DB project is running!')
    command = welcome()
    print(command)

if __name__ == '__main__':
    main()
