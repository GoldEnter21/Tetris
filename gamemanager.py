import main
import rotationkicks
import random
rotationstates = ["0", "R", "2", "L"]
available_pieces = ["I", "O", "L", "J", "S", "Z", "T"]

class gamestate():
    def __init__(self, grid_width, grid_height, invisibility_radius):
        self.grid = []
        self.garbage = []
        self.lowest_garb_level = grid_height
        for r in range(grid_height):
            self.grid.append([])
            for c in range(grid_width):
                self.grid[r].append("-")
        self.invisible_rows = invisibility_radius
        self.grid_width = grid_width - 1
        self.grid_height = grid_height - 1
        for i in range(grid_width):
            self.garbage.append(self.lowest_garb_level)
    
    def update_garbage(self):
        searchable_indexs = main.searchable_indexes[:]
        omitted_indexs = []
        for row in range(len(self.grid)):
            for c in searchable_indexs:
                if self.grid[row][c] != "-":
                    omitted_indexs.append(c)
                    self.garbage[c] = row
            for o in omitted_indexs:
                searchable_indexs.remove(o)
            omitted_indexs.clear()
        for c in searchable_indexs:
            self.garbage[c] = self.lowest_garb_level

    def clear_rows(self):
        for row in range(len(self.grid)):
            if self.grid[row].count("-") == 0:
                self.grid.pop(row)
                self.grid.insert(0, main.Grid_Row[:])
        self.update_garbage()

    def update_tetromino(self, tetromino):
        for coord in tetromino.Mino_Coords:
            self.grid[coord[1] + self.invisible_rows][coord[0]] = tetromino.piecetype
    
    def destroy_tetromino(self, tetromino):
        for coord in tetromino.Mino_Coords:
            self.grid[coord[1] + self.invisible_rows][coord[0]] = "-"
    
    def test_collision(self, test_coords, original_coords, down):
        validity = True
        for coord in test_coords:
            if coord[0] > self.grid_width or coord[0] < 0:
                validity = False
            elif coord[1] + self.invisible_rows < 0:
                validity = False
            elif coord[1] + self.invisible_rows > self.grid_height:
                validity = "finished"
            else:
                if self.grid[coord[1] + self.invisible_rows][coord[0]] != "-":
                    if not original_coords.count(coord) > 0:
                        if down:
                            validity = "finished"
                        elif not down:
                            validity = False
        return validity
    
    def rotate_tetromino(self, tetromino, direction):
        starting_loc = rotationstates.index(tetromino.rotationstate)
        ending_loc = starting_loc + direction
        rotation = str(tetromino.rotationstate) + "->" + str(rotationstates[ending_loc % 4])
        verification = rotationkicks.verify_rotation(self, tetromino, rotation)
        if verification[0] == True:
            self.destroy_tetromino(tetromino)
            tetromino.Mino_Coords = verification[1]
            tetromino.rotationstate = str(rotationstates[ending_loc % 4])
            tetromino.x += verification[2][0]
            tetromino.y -= verification[2][1]
            self.update_tetromino(tetromino)
    
    def move_tetromino(self, tetromino, down, direction):
        test_coords = []
        if not down:
            for coord in tetromino.Mino_Coords:
                test_coords.append([coord[0] + direction, coord[1]])
        if down:
            for coord in tetromino.Mino_Coords:
                test_coords.append([coord[0], coord[1] + direction])
        can_move = self.test_collision(test_coords, tetromino.Mino_Coords, down)
        if can_move == True:
            self.destroy_tetromino(tetromino)
            tetromino.Mino_Coords = test_coords
            if not down:
                tetromino.x += direction
            if down:
                tetromino.y += direction
            self.update_tetromino(tetromino)
            return False
        elif can_move == False:
            return False
        elif can_move == "finished":
            return True
    
    def harddrop(self, tetromino):
        harddropcoords = {}
        for coord in tetromino.Mino_Coords:
            if coord[0] in harddropcoords.keys():
                if harddropcoords[coord[0]] < coord[1]:
                    harddropcoords.pop(coord[0])
                    harddropcoords.update({coord[0] : coord[1]})
            else:
                harddropcoords.update({coord[0] : coord[1]})
        for key in harddropcoords:
            harddropcoords[key] = self.garbage[key] - harddropcoords[key]
        harddrop = min(harddropcoords.values()) - 1 - self.invisible_rows
        self.destroy_tetromino(tetromino)
        for coord in tetromino.Mino_Coords:
            coord[1] += harddrop
        tetromino.y += harddrop
        self.update_tetromino(tetromino)

class tetromino():
    def __init__(self, type):
        if (type in available_pieces): 
            self.piecetype = type
            if type == "T":
                self.Mino_Coords = [[3,-2], [4,-3], [4,-2], [5,-2]]
            if type == "Z":
                self.Mino_Coords = [[3,-3], [4,-3], [4,-2], [5,-2]]
            if type == "S":
                self.Mino_Coords = [[3,-2], [4,-3], [4,-2], [5,-3]]
            if type == "O":
                self.Mino_Coords = [[4,-2], [4,-3], [5,-2], [5,-3]]
            if type == "J":
                self.Mino_Coords = [[3,-2], [3,-3], [4,-2], [5,-2]]
            if type == "L":
                self.Mino_Coords = [[3,-2], [4,-2], [5,-2], [5,-3]]
            if type == "I":
                self.Mino_Coords = [[3,-2], [4,-2], [5,-2], [6,-2]]
            self.rotationstate = "0"
            self.x = 3
            self.y = -3

class upcoming():
    def __init__(self):
        self.queue = []
        i = 0
        while i < 2:
            pieces = available_pieces[:]
            while len(pieces) > 0:
                selector = random.randint(0, len(pieces) - 1)
                selected_piece = pieces.pop(selector)
                self.queue.append(selected_piece)
            i += 1
        self.hold = []
        self.hold_usable = True
    
    def recharge(self):
        pieces = available_pieces[:]
        while len(pieces) > 0:
            selector = random.randint(0, len(pieces) - 1)
            selected_piece = pieces.pop(selector)
            self.queue.append(selected_piece)
    
    def update_hold(self, gamestate, tetromino):
        if self.hold_usable:
            holded_piece = self.queue.pop(0)
            gamestate.destroy_tetromino(tetromino)
            if len(self.hold) > 0:
                unholded_piece = self.hold.pop(0)
                self.queue.insert(0, unholded_piece)
            elif len(self.hold) == 0:
                unholded_piece = self.queue[0]
            self.hold.append(holded_piece)
            return unholded_piece
        else:
            return None
            