from disk2pi import Main
import sys
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    a = Main(sys.argv[1:])
