class Queen:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'Q'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        row_dist = abs(self.row - row)
        col_dist = abs(self.col - col)
        if row < 0 or col < 0 or row > 7 or col > 7:
            return False
        if row_dist == col_dist or row == self.row or col == self.col:
            return True
        return False
