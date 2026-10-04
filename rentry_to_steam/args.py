from argparse import Namespace, ArgumentParser

class Args:
    def __init__(self):
        args = self.get_args()

        self.urls: list[str] = args.urls

    def get_args(self) -> Namespace:
        parser = ArgumentParser()

        parser.add_argument(
            "urls",
            nargs="+",
            help="A list of rentry urls to subscribe to."
        )

        return parser.parse_args()