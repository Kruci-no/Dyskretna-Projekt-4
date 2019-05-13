import numpy as np
import itertools
class polynomian:
    def __init__(self,arr):
        self.arr = arr
    def __add__(self,other):
        arr=[]
        for i in range(min(len(self.arr), len(other.arr) ) ):
            arr.append(self.arr[i]+other.arr[i])
        if len(self.arr) < len(other.arr):
            arr.extend(other.arr[len(self.arr):])
        else:
            arr.extend(self.arr[len(other.arr):])
        return polynomian(arr)
    def __mul__(self,other):
        arr = [0 for i in range(len(other.arr) + len(self.arr)-1)]
        for n in range(len(other.arr) + len(self.arr)-1):
            for k in range(n+1):
                try:
                    arr[n]+=self.arr[n-k] * other.arr[k]
                except:
                    pass
        return polynomian(arr)
    def __str__(self):
        s = str(self.arr[0])
        for i in range(1,len(self.arr)):
            if self.arr[i]!=0:
                s+=" + {0}*x**{1}".format(self.arr[i],i)
                
        return s
    def last_coefficient(self):
        return self.arr[len(self.arr)-1]
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(str(self))
    def __eq__(self,other):
        return self.arr == other.arr

class tuple_matrix:
    def __init__(self,array):
        def totuple(a):
            try:
                return tuple(totuple(i) for i in a)
            except TypeError:
                return a
        self.matrix = totuple(array)
    def __hash__(self):
        return hash(str(self))
    def __str__(self):
        s="\n"
        for tup in self.matrix:
            s += str(tup) + "\n"
        return s
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(str(self))
    def __eq__(self,other):
        return self.matrix == other.matrix
    def drop(self,n):
        arr = ((self.matrix[i][j] for j in range(len(self.matrix[i])) if j != n) for i in range(len(self.matrix)) if i!=0) 
        return tuple_matrix(arr)

class commission:
    def __init__(self,m,M,lecturers_num,subjects,matrix):
        self.m = m
        self.M = M
        self.lecturers_num = lecturers_num
        self.lecturers = list(range(lecturers_num))
        self.subjects = subjects
        self.matrix = np.array(matrix)
        self.x = polynomian([0,1])
        self.computed_polynomian = {}
    def generetate(self):
        self.lecturers_sets = []
        for i in range(self.m,self.M + 1):
            self.lecturers_sets.extend( [x for x in itertools.combinations(self.lecturers, i)] ) 
    
    def compute(self,table):
        try:
            return self.computed_polynomian[table]
        except:
            if len(table.matrix) == 1:
                w = polynomian([1,sum(table.matrix[0])])
                self.computed_polynomian[table] = w
                return self.computed_polynomian[table]
            for i in range(len(table.matrix[0])):
                if table.matrix[0][i] == 1:
                    K = list(table.matrix) 
                    K[0] = list(K[0])
                    K[0][i] = 0
                    table_B = tuple_matrix(K)
                    self.computed_polynomian[table] = self.compute(table.drop(i))*self.x+self.compute(table_B)
                    return self.computed_polynomian[table]
            else:
                table_B = tuple_matrix(table.matrix[1:])
                self.computed_polynomian[table] = self.compute(table_B)
                return self.computed_polynomian[table]
    def compute_lecturers_polynomian(self):
        self.lecturers_polynomian = {x:self.compute(tuple_matrix(self.matrix[x,:])) for x in self.lecturers_sets}
    def choise(self):
        maximum = 0
        for key,value in self.lecturers_polynomian.items():
            if value.last_coefficient() > maximum:
                maximum = value.last_coefficient()
        self.maximum = maximum
        self.best_choise = [key for key,value in self.lecturers_polynomian.items() if value.last_coefficient() == self.maximum]
        return self.best_choise 



if __name__ == "__main__":
    m = 2
    M = 5
    lecturers_num = 5
    subjects = 5
    A = np.random.uniform(-1,1,size=(5,5))
    A=np.array(A>0,dtype = int)
    C=commission(m,M,lecturers_num,subjects,A)
    C.generetate()
    C.compute_lecturers_polynomian()
    print("Optymalne wybor wykładowców",C.choise())
    print("Maksymalna liczba egzaminów",C.maximum)