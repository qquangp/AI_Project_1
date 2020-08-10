import sys
def readfile(filename,mode)->tuple:
    try:
        with open(filename,mode) as file:
            a=file.readline()
            size=tuple(map(int,a.split()))
            a=file.readline()
            start=tuple(map(int,a.split()))
            a=file.readline()
            goal=tuple(map(int,a.split()))
            data=[]
            for i in range(size[0]):
                d=file.readline()
                data.append(list(map(int,d.split())))
            return (data,start,goal)
    except IOError:
        print('Could not read file:',filename)
        return False
def writefile(filename,mode,data,matrix,start,goal):
    try:
        with open(filename,mode) as file:
            if data==-1:
                file.write('-1')
            else:
                file.write(str(len(data))+'\n')
                res=''
                for i in data:
                    res+='{} '.format(i)
                file.write(res)
                file.write('\n')
                for step in data:
                    matrix[step[0]][step[1]]=2
                matrix[start[0]][start[1]]=3
                matrix[goal[0]][goal[1]]=4
                for row in matrix:
                    line=[]
                    for col in row:
                        if col == 1:
                            line.append("o ")
                        elif col == 0:
                            line.append("- ")
                        elif col == 2:
                            line.append("x ")
                        elif col==3:
                            line.append('S ')
                        elif col==4:
                            line.append('G ')
                    file.write("".join(line))
                    file.write('\n')

    except EOFError:
        print('Could not write file:',filename)
        return False
class node:
    #constructor
    def __init__(self, parent=None, vitri=None):
        self.parent=parent
        self.vitri=vitri

        self.g=0
        self.h=0
        self.f=0
    #implement toan tu ==
    def __eq__(self,other):
        return self.vitri == other.vitri
    
def duongdingannhat(node_ht):
        path=[]
        hientai=node_ht
        while hientai is not None:
            path.append(hientai.vitri)
            hientai=hientai.parent
        return path[::-1]
def gtricell(matran,node_pos):
    return matran[node_pos[0]][node_pos[1]]
def create_child_node(matran,node_ht):
    children=[]
    neighbor=[(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for new_position in neighbor:
        node_position=(node_ht.vitri[0]+new_position[0],node_ht.vitri[1]+new_position[1])
        if node_position[0]>(len(matran)-1) or node_position[0]<0 or node_position[1]>(len(matran[len(matran)-1])-1) or node_position[1]<0:
            continue
        if gtricell(matran,node_position)==1:
            continue
        if node_position[0]-node_ht.vitri[0] ==-1 and node_position[1]-node_ht.vitri[1] ==-1 and matran[node_ht.vitri[0]-1][node_ht.vitri[1]]==1 and matran[node_ht.vitri[0]][node_ht.vitri[1]-1]==1:
            continue
        if node_position[0]-node_ht.vitri[0] ==-1 and node_position[1]-node_ht.vitri[1] ==1 and matran[node_ht.vitri[0]-1][node_ht.vitri[1]]==1 and matran[node_ht.vitri[0]][node_ht.vitri[1]+1]==1:
            continue
        if node_position[0]-node_ht.vitri[0] ==1 and node_position[1]-node_ht.vitri[1] ==1 and matran[node_ht.vitri[0]][node_ht.vitri[1]+1]==1 and matran[node_ht.vitri[0]+1][node_ht.vitri[1]]==1:
            continue
        if node_position[0]-node_ht.vitri[0] ==1 and node_position[1]-node_ht.vitri[1] ==-1 and matran[node_ht.vitri[0]][node_ht.vitri[1]-1]==1 and matran[node_ht.vitri[0]+1][node_ht.vitri[1]]==1:
            continue
        node_=node(node_ht,node_position)
        children.append(node_)
       
    return children


def thuattoan(matran,start,end):
    #khoi tao diem bat dau va diem ket thuc
    node_bd= node(None,start)
    node_bd.g=node_bd.h=node_bd.f=0
    node_kt= node(None,end)
    node_kt.g=node_kt.h=node_kt.f=0
    #khoi tao danh sach mo va dong
    open_list=[]
    close_list=[]

    open_list.append(node_bd)
    #dieu kien dung
    outer_iterations=0
    #max_iterations=(len(matran)//2)**10
    max_iterations = (len(matran[0]) * len(matran) // 2)
    #vong lap cho den khi tim thay diem dung
    while len(open_list)>0:
        outer_iterations+=1
        if outer_iterations > max_iterations:
            return -1
        node_ht= open_list[0]
        index_ht=0
        for index,item in enumerate(open_list):
            if item.f <node_ht.f:
                node_ht=item
                index_ht=index
        open_list.pop(index_ht)
        close_list.append(node_ht)
        if node_ht==node_kt:
            return duongdingannhat(node_ht)
        #khoi tao node con
        children=[]
        children=create_child_node(matran,node_ht)
        for child in children:
            for closed_child in close_list:
                if child==closed_child:
                    continue
            child.g=node_ht.g+1
            child.h=((child.vitri[0]-node_kt.vitri[0])**2)+((child.vitri[1]-node_kt.vitri[1])**2)
            child.f=child.g+child.h
            for open_node in open_list:
                if child== open_node and child.g >open_node.g:
                    continue
            open_list.append(child)
    return None
def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s)) 

def main():
    if (len(sys.argv)==3):
        file=readfile(sys.argv[1],'r')
        if file==False:
            return False
        matrix=file[0]
        start=file[1]
        goal=file[2]
        path=thuattoan(matrix,start,goal)
        writefile(sys.argv[2],'w',path,matrix,start,goal)
    else:
        print('Thieu tham so dau vao')
if __name__ == '__main__':
    main()  






        

