import main
import rotationkicks
rotationstates = ["0", "R", "2", "L"]

class gamestate():
    def __init__(self, grid_width, grid_height, invisibility_radius):
        self.grid = []
        for r in range(grid_height + 4):
            self.grid.append([])
            for c in range(grid_width):
                self.grid[r].append("-")
        self.invisible_rows = invisibility_radius
        self.grid_width = grid_width - 1
        self.grid_height = grid_height - 1

    def update_tetromino(self, tetromino):
        for coord in tetromino.Mino_Coords:
            self.grid[coord[1] + self.invisible_rows][coord[0]] = tetromino.piecetype
    
    def destroy_tetromino(self, tetromino):
        for coord in tetromino.Mino_Coords:
            self.grid[coord[1] + self.invisible_rows][coord[0]] = "-"
    
    def test_collision(self, test_coords, original_coords):
        validity = True
        for coord in test_coords:
            if coord[0] > self.grid_width or coord[0] < 0:
                validity = False
            else:
                if self.grid[coord[1] + self.invisible_rows][coord[0]] != "-":
                    if not original_coords.count(coord) > 0:
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
            tetromino.y += verification[2][1]
            self.update_tetromino(tetromino)
    
    def move_tetromino(self, tetromino, direction):
        test_coords = []
        for coord in tetromino.Mino_Coords:
            test_coords.append([coord[0] + direction, coord[1]])
        can_move = self.test_collision(test_coords, tetromino.Mino_Coords)
        if can_move == True:
            self.destroy_tetromino(tetromino)
            tetromino.Mino_Coords = test_coords
            tetromino.x += direction
            self.update_tetromino(tetromino)

class tetromino():
    def __init__(self, type):
        if (type == "I" or 
            type == "L" or 
            type == "J" or 
            type == "O" or 
            type == "S" or 
            type == "Z" or 
            type == "T"): 
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