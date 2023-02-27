from argparse import ArgumentParser
from modules import app


if __name__ == '__main__':
    parser = ArgumentParser(description='Parse arguments from cmd')
    parser.add_argument('--p', type=str, required=True)
    parser.add_argument('--f', type=str, required=True)
    parser.add_argument('--d', type=str, required=False)

    app.run(parser.parse_args())
