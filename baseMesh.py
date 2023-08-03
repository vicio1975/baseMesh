# -*- coding: utf-8 -*-
"""
Author: Vincenzo Sammartano
"""
#### Libraries
import numpy as np
import shutil
####


#### Function definitions
def headerLines(cl,loc,obj,con="convertToMeters 1;"):
    h = [
    "/*--------------------------------*- C++ -*----------------------------------*\\",
    "| =========                 |                                                 |",
    "| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |",
    "|  \\\    /   O peration     | Version:  v1812                                 |",
    "|   \\\  /    A nd           | Web:      www.OpenFOAM.com                      |",
    "|    \\\/     M anipulation  |                                                 |",
    "\*---------------------------------------------------------------------------*/",
    "FoamFile",
    "{",
    "    version     2.0;",
    "    format      ascii;",
    "    class       {};",
    '    location    "{}";',
    "    object      {};",
    "}",
    "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //",
    "",
    "{}",
    ""]
   
    h[11] = h[11].format(cl)
    h[12] = h[12].format(loc)
    h[13] = h[13].format(obj)
    h[17] = h[17].format(con)    
    return h
        
    
def Geometry():
    ############################
    ## vertices and their coord
    px = []
    py = []
    pz = []

    px.append(C[0])
    px.append(px[0]+a)
    px.append(px[1])
    px.append(px[0])

    py.append(C[1]-b)
    py.append(py[0])
    py.append(py[1]+b)
    py.append(py[2])

    pz.append(C[2])
    for i in range(3):
        pz.append(pz[0])
    pz.append(pz[0]+H)
    for i in range(3):
        pz.append(pz[4])

    px = px + px
    py = py + py

    Ixyz = [index for index,i in enumerate(px)]
    
    ##########################################
    ### Write file block #####################
    fid = open("blockMeshDict","w")
    
    #header
    header = headerLines(cl,loc,obj)
    for l in range(len(header)):
        fid.write("{}\n".format(header[l]))
    ####
    
    #vertices
    fid.write("vertices\n")    
    fid.write("(\n")
    for i in range(len(px)):
        fid.write("\t({} {} {}) \t\t //{}\n".format(px[i],py[i],pz[i],i))
    fid.write(");\n")
    fid.write("")
    ####
    
    #blocks blocks
    fid.write("\nblocks\n")
    fid.write("(\n")
    #block1
    fid.write("\t hex (") 
    for i in list(range(Nnod)):
        fid.write(" {} ".format(Ixyz[i]))
    fid.write(")\t")
    ##number of subdivisions
    fid.write("({} {} {})\t".format(Nx0,Ny0,Nz0))
    ##simpleGrading
    fid.write("simpleGrading ({} {} {})\n".format(sx1,sy1,sz1))
    fid.write(");\n")
    fid.write("")
    ####
    
    #edges
    fid.write("\nedges\n")
    fid.write("(\n")
    fid.write(");\n")
    fid.write("")
    ####
    
    #boundary 
    fid.write("\nboundary\n")
    fid.write("(\n")
    #dir x
    for i in list(range(2)):
        fid.write("\t{}\n".format(face[i]))
        fid.write("\t{\n")
        fid.write("\t\ttype {};\n".format(typos[face[i]]))
        fid.write("\t\tfaces\n")
        fid.write("\t\t(\n")
        fid.write("\t\t({} {} {} {})\n".format(Ixyz[i], Ixyz[i]+int(0.5*Nnod)-1-2*i , Ixyz[i]+int(0.5*Nnod), Ixyz[i]+int(Nnod)-1-2*i ))
        fid.write("\t\t);\n")
        fid.write("\t}\n")

    #dir y
    st = "\t\t({a} {b} {c} {d})\n"
    ss = []        
    for i in list(range(2)):
        st = "\t\t({a} {b} {c} {d})\n"
        ss = [i for i in Ixyz[:2]]
        ss = ss + [i+int(0.5*Nnod) for i in ss]
        ss2 = [i+3 if (index%2 == 0)  else i+1 for index,i in enumerate(ss)]            
        if i == 0:
           strin = st.format(a=ss[0],b=ss[1],d=ss[0]+int(0.5*Nnod),c=ss[1]+int(0.5*Nnod))     
        elif i ==1:
            ss = ss2
            strin = st.format(a=ss[0],b=ss[1],d=ss[2],c=ss[3])
        fid.write("\t{}\n".format(face[i+2]))
        fid.write("\t{\n")
        fid.write("\t\ttype {};\n".format(typos[face[i+2]]))
        fid.write("\t\tfaces\n")
        fid.write("\t\t(\n")    
        fid.write(strin)         
        fid.write("\t\t);\n")
        fid.write("\t}\n")

        fid.write("")
    ####

    #dir z
    for i in list(range(2)):
            st = "\t\t({a} {b} {c} {d})\n"
            ss = []        
            for j in list(range(int(0.5*Nnod))):
                ss.append(Ixyz[j+int(0.5*Nnod)*i])
            fid.write("\t{}\n".format(face[i+4]))
            fid.write("\t{\n")
            fid.write("\t\ttype {};\n".format(typos[face[i+4]]))
            fid.write("\t\tfaces\n")
            fid.write("\t\t(\n")    
            fid.write(st.format(a=ss[0],b=ss[1],c=ss[2],d=ss[3]))
            fid.write("\t\t);\n")
            fid.write("\t}\n")
    fid.write(");\n")
    fid.write("")
    
    #mergPatchPairs
    fid.write("\nmergPatchPairs\n")
    fid.write("(\n")
    fid.write(");\n")
    fid.write("\n")
    ####
    fid.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
    print("\n--> Moving the blockMeshDict file in system ...")
    shutil.move("blockMeshDict","system/blockMeshDict" )
############################# END Functions ##############################################################


################ MAIN Program
cl = "dictionary"
loc = "system"
obj = "blockMeshDict"
bcs = "faceX0 faceX+ faceY0 faceY+ faceZ0 faceZ+".split(" ")
face = []
typos = {}
print("\n--> Selection of BCs")

for bc in bcs:
    q1 = "    - Assign a name for the face {}\t: ".format(bc)
    face.append(input(q1).strip())
    f = face[-1]
    q2 = "    - Set a BC type for the face {}\t: ".format(f)
    typos[f] = input(q2).strip() 
    
######################## This could be in a function 
#Geometry specifications
print("\n--> Geometry definition")
a = float((input("   - X total length: ").strip()))
b = float((input("   - Y total length: ").strip()))
H = float((input("   - Z total length: ").strip()))

print("\n--> Position of lower vertex:")
c1 = float((input("     - x0 = ").strip()))
c2 = float((input("     - y0 = ").strip()))
c3 = float((input("     - z0 = ").strip()))

C = [c1,c2,c3]

Nnod = 8 #Number of nodes
Ngr =  0
NnTot = Nnod + 4*Ngr
Nfac = int((2+Nnod/2)+5*Ngr)

#cells for block 0 
lx = float((input("\n--> length of cells along x direction dx = ").strip()))

Nx0 = int(np.ceil(a/lx))
ly = lx   
Ny0 = int(np.ceil(b/ly))
lz = ly    
Nz0 = int(np.ceil(H/lz))
    
#simpleGrading
print("\n--> Simplegrading")
sx1 = int((input("   -  sx = ").strip()))
sy1 = int((input("   -  sy = ").strip()))
sz1 = int((input("   -  sz = ").strip()))
 
#######################

Geometry()

#######################



