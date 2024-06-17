#Not used in the game
#Tamanho do tabuleiro é 9x9 logo, salvamos esse tamanho
tamanho = 9
def desenha(a):
    for i in range(tamanho):
        for j in range(tamanho):
            print(a[i][j],end = " ")
        print()
        
def disponibilidadecheck(grid, linha, col, num):
    for x in range(9):
        if grid[linha][x] == num:
            return False
             
    for x in range(9):
        if grid[x][col] == num:
            return False
 
 
    linhaInicial = linha - linha % 3
    colunaInicial = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + linhaInicial][j + colunaInicial] == num:
                return False
    return True

def soluciona(grid, linha, col):
    if ((linha == tamanho - 1) and (col == tamanho)):
        return True
    if col == tamanho:
        col = 0
        linha += 1
    if grid[linha][col] > 0:
        return soluciona(grid, linha, col+1)
    for numero in range(1, tamanho+1, 1):
        if disponibilidadecheck(grid, linha, col, numero):
            grid[linha][col]= numero
            if soluciona(grid, linha, col + 1):
                return True
            grid[linha][col] = 0
    return False


grid = [[4, 5, 0, 0, 3, 0, 9, 0, 1],
        [0, 1, 0, 0, 0, 4, 0, 0, 0],
    [4, 0, 7, 0, 0, 0, 2, 0, 8],
    [0, 0, 5, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 9, 8, 1, 0, 0],
    [0, 4, 0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 3, 6, 0, 0, 7, 2],
    [0, 7, 0, 0, 0, 0, 0, 0, 3],
    [9, 0, 3, 0, 0, 0, 6, 0, 4]]
 
if (soluciona(grid, 0, 0)):
    print("Opa, achei solução:")
    desenha(grid)
else:
    print("Opa, não achei solução:")