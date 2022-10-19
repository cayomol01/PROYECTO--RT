import numpy as np




class matlib(object):
    def __init__(self):
        pass
    
    
    def Add(self, matrix1, matrix2):
        try:
            result = [[matrix1[i][j] + matrix2[i][j]  for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
            return result
        except:
            result = [matrix1[i] + matrix2[i] for i in range(len(matrix1))]
            return result
    
    def Subtract(self, matrix1, matrix2):
        if type(matrix1[0]) == list:
            result = [[matrix1[i][j] - matrix2[i][j]  for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
            return result
        else:
            result = [matrix1[i] - matrix2[i] for i in range(len(matrix1))]
            return result
        
    def ScalarMul(self,vector,scalar):
        resul = []
        for i in vector:
            resul.append(i*scalar)
        return resul
    
    def mul(self,v1,v2):
        resul = []
        for i in range(len(v1)):
            resul.append(v1[i]*v2[i])
        return resul
          
    def Product(self, matrix1, matrix2):
        res = [[0,0,0,0],
               [0,0,0,0],
               [0,0,0,0],
               [0,0,0,0]]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    res[i][j] += (matrix1[i][k] * matrix2[k][j])
        return res
    
    def NegativeVector(self, vector):
        res = []
        for i in vector:
            res.append(-i)
        return res
        
    def Division(self, matrix1, matrix2):
        result = [[matrix1[i][j] * matrix2[i][j]  for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        return result
    
    def scalarDiv(self, matrix1, scalar):
        res = []
        for i in range(len(matrix1)):
            if matrix1[i] != 0:
                res.append(matrix1[i]/scalar)
            else:
                res.append(matrix1[i])
        return res
    
    def dot(self, vector1, vector2):
        result = 0
        for i in range(len(vector1)):
            result = result + vector1[i]*vector2[i]
        return result
    
    def cross(self, vector1, vector2):
        result =    [vector1[1]*vector2[2] - vector1[2]*vector2[1],
                    vector1[2]*vector2[0] - vector1[0]*vector2[2],
                    vector1[0]*vector2[1] - vector1[1]*vector2[0]]
        return result
    
    def matmul(self,matrix1,matrix2):
        ''' print(matrix1)
        print(matrix2)
        convertir = False
        rows1 = len(matrix1)
        columns1 = len(matrix1[0])
        rows2 = len(matrix2)
        columns2 = len(matrix2[0])
        print(" ")
        print(matrix1)
        print(matrix2)
        
        result = []
        
        #n1 x m1
        #n2 x m2
        if columns1 == rows2:
            for i in range(rows1):
                result.append([])
                for j in range(columns2):
                    result[i].append(0)
        
            for i in range(rows1):
                for j in range(columns2):
                    for k in range(rows2):
                        result[i][j] += matrix1[i][k] * matrix1[k][j]
            return result '''

        # Fuente: https://www.codingem.com/numpy-at-operator/
    # Equivalente a @
        if type(matrix2[0])!=list:
            matrix2 = list(matrix2)
            for i in range(len(matrix2)):
                matrix2[i] = [matrix2[i]]
            columnas = list(zip(*matrix2))
        
            return self.flatten([[self.dot(x,y) for x in columnas] for y in matrix1])
        else:
            columnas = list(zip(*matrix2))
        
            return ([[self.dot(x,y) for x in columnas] for y in matrix1])
            
        
    def norm(self, matrix):
        suma = 0
        for i in range(len(matrix)):
            suma += matrix[i]**2
        return suma ** 0.5
    
    def identity(self, size):
        self.matrix = []
        for i in range(size):
            self.matrix.append([])
            for j in range(size):
                if i == j:
                    self.matrix[i].append(1)
                else:
                    self.matrix[i].append(0)
                    
                    
    #How to get the inverse of a matrix  obtained from: https://www.codegrepper.com/code-examples/python/matrix+inverse+python+without+numpy
    def transposeMatrix(self, m):
        res = [*zip(*m)]
        for i in range(len(res)):
            res[i] = list(res[i])
        return res
    def getMatrixMinor(self, m,i,j):
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    def getMatrixDeternminant(self, m):
        #base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c)*m[0][c]*self.getMatrixDeternminant(self.getMatrixMinor(m,0,c))
        return determinant

    def getMatrixInverse(self, m):
        determinant = self.getMatrixDeternminant(m)
        #special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                    [-1*m[1][0]/determinant, m[0][0]/determinant]]

        #find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m,r,c)
                cofactorRow.append(((-1)**(r+c)) * self.getMatrixDeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c]/determinant
        return cofactors
    #End of how to get the inverse of a matrix

    def flatten(self, matrix):
        res = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                res.append(matrix[i][j])
        return res    
    
    

