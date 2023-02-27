from argparse import ArgumentParser
from modules import app


if __name__ == '__main__':
    parser = ArgumentParser(description='Parse arguments from cmd')
    parser.add_argument('--p', type=str)

    args = parser.parse_args()
    app.run(args.p)
