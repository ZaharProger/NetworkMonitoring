from argparse import ArgumentParser
import app

if __name__ == '__main__':
    parser = ArgumentParser(description='Parse arguments from cmd')
    parser.add_argument('--p', type=str, required=True)
    parser.add_argument('--d', type=str, required=False)

    args = parser.parse_args()
    args.f = args.p.split('.')[-1]

    app.run(args)
