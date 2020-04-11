class Index():
    def __init__(self, df, index):
        self.df = df.set_index( keys = index )

    def __enter__(self):
        return self.df

    def __exit__(self, *args):
        pass

    def update(self):
        pass
