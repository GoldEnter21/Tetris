import rotations

Rkicklocs = {
    "0->R": 0,
    "R->0": 1,
    "R->2": 2,
    "2->R": 3,
    "2->L": 4,
    "L->2": 5,
    "L->0": 6,
    "0->L": 7
}

Rkicks = [[(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)], 
          [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],
          [(0, 0), (+1, 0),	(+1, -1), (0, +2), (+1, +2)],
          [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],
          [(0, 0), (+1, 0), (+1, +1), (0 ,-2), (+1, -2)],
          [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],
          [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],
          [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],
          ]

RkicksI =[[(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
          [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
          [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],
          [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
          [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
          [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
          [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
          [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],
          ]

Wkicks = [(0, 0), (-1, 0), (+1, 0)]

def matrice_to_coords(matrice):
    coords = []
    for num in matrice:
        x = num % 4
        y = (num - x) // 4
        coords.append([x, y])
    
    return coords

def verify_rotation(gamestate, tetromino, rotation):
    Rot_all = rotations.type_matchup[tetromino.piecetype]
    matrice_NRot = Rot_all[rotation[3]]
    Prim_NRotcoords = matrice_to_coords(matrice_NRot)
    testable_rotation = []
    for coord in range(len(Prim_NRotcoords)):
        x = Prim_NRotcoords[coord][0]
        y = Prim_NRotcoords[coord][1]
        testable_rotation.append([tetromino.x + x, tetromino.y + y])
    
    use_wall_kicks = False
    
    for coord in testable_rotation:
        if coord[0] < 0 or coord[0] > gamestate.grid_width:
            use_wall_kicks = True
            found_rotation = False
            final_rotation_coords = []
        elif coord[1] + gamestate.invisible_rows < 0 or coord[1] + gamestate.invisible_rows > gamestate.grid_height:
            use_wall_kicks = True
            found_rotation = False
            final_rotation_coords = []
    
    if use_wall_kicks == False:
        if tetromino.piecetype != "I":
            kick_ind = Rkicklocs[rotation]
            kick_tests = Rkicks[kick_ind]
        elif tetromino.piecetype == "I":
            kick_ind = Rkicklocs[rotation]
            kick_tests = RkicksI[kick_ind]    

    elif use_wall_kicks:
        kick_tests = Wkicks   

    test_num = 0
    found_rotation = False
    final_rotation_coords = []
    while test_num <= len(kick_tests) - 1 and found_rotation == False:
        test_coords = []
        verification = 0
        for coord in range(len(testable_rotation)):
            x = kick_tests[test_num][0] + testable_rotation[coord][0]
            y = testable_rotation[coord][1] - kick_tests[test_num][1]
            if x >= 0 and x <= gamestate.grid_width:
                if y + gamestate.invisible_rows >= 0 and y + gamestate.invisible_rows <= gamestate.grid_height:
                    test_coords.append([x, y])
        
        if len(test_coords) == 4:
            for coord in test_coords:
                if gamestate.grid[coord[1] + gamestate.invisible_rows][coord[0]] != "-":
                    if not tetromino.Mino_Coords.count(coord) > 0:
                        test_num += 1
                        break
                    elif tetromino.Mino_Coords.count(coord) > 0:
                        verification += 1
                elif gamestate.grid[coord[1] + gamestate.invisible_rows][coord[0]] == "-":
                    verification += 1
                if verification == len(kick_tests) - 1:
                    found_rotation = True
                    final_rotation_coords = test_coords
                    break
        else:
            test_num += 1
    
    if test_num > len(kick_tests) - 1:
        test_num = 0
        
    return [found_rotation, final_rotation_coords, kick_tests[test_num]]
