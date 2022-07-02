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
    
    if tetromino.piecetype != "I":
        kick_ind = Rkicklocs[rotation]
        kick_tests = Rkicks[kick_ind]

    test_num = 0
    found_rotation = False
    final_rotation_coords = []
    while test_num <= 4 and found_rotation == False:
        test_coords = []
        verification = 0
        for coord in range(len(testable_rotation)):
            x = kick_tests[test_num][0] + testable_rotation[coord][0]
            y = kick_tests[test_num][1] + testable_rotation[coord][1]
            test_coords.append([x, y])
        
        for coord in test_coords:
            if gamestate.grid[coord[1]][coord[0]] != "-":
                test_num += 1
                break
            elif gamestate.grid[coord[1]][coord[0]] == "-":
                verification += 1
            if verification == 4:
                found_rotation = True
                final_rotation_coords = test_coords
                break
                
        
    return [found_rotation, final_rotation_coords]
