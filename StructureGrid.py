class grid():
    def __init__(self) -> None:
        self.free = True
        self.height = 0
        self.add = True
        self.function = []

    def __str__(self) -> str:
        if self.function:
            return '0'
        else:
            return '1'

    def __repr__(self) -> str:
        if self.function:
            return '0'
        else:
            return '1'