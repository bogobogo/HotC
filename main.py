import sys
import Control.HotC as HotC

def main():
    hotc = HotC.HotC()
    hotc.serve_forever()

if __name__ == "__main__":
    sys.exit(main())
