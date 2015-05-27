from requests import main
from time import sleep

if __name__ == '__main__':
  while True:
    print '*' * 30
    print 'Checking for requests...'
    main()
    print
    sleep(10)

