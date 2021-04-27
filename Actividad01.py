import os 
import math 
import statistics 

#programa para calcular coordenadas crudas archivos 
#listas vacias 
coorx = [] 
coory = [] 
archivos_as = [] 
coorz = [] 
direccion = ''
#funcion para llamar el archivos as  la lista vacia 
def carpeta_as(direccion):
    for root,dirs,files in os.getcwd(direccion):
        for file in files:
            if file.endswith('.as'):
                archivos_as.append(file) 
#funcion para convetir los archivos crudos a .o 
def convetir(archivos_as):
    for archivos in archivos_as:
        name = archivos.split('.')[0] + '.o '
        comando = "teqc -O.dec 30 +obs " + name +  archivos 
        os.system(comando) 
#extraer coordenas y agregarlas a lista de cada coordenada
def extrack_as():
    for files,dirs,root in os.getcwd(direccion):
        for archivo in files:
            if archivo.endswith(".o"):
                with open(archivo) as o:
                    linea = o.readline()[9:10] 
                    for line in linea:
                        leer = line.strip().split(' ')
                        x = float(leer[0]) 
                        coorx.append(x)
                        y = float(leer[1])
                        coory.append(y)
                        z = float(leer[2]) 
                        coorz.append(z) 

#calcular coordenadas 
def calculo():
    x_media = statistics.mean(coorx)
    y_media = statistics.mean(coory) 
    z_media = statistics.mean(coorz) 
    return [x_media,y_media,z_media] 

x_mean = calculo()[0] 
y_mean = calculo()[1] 
z_mean = calculo()[2] 
print("Valores calculados de coordenadas")
print(f"coordenada x cruda: {round(x_mean)}")
print(f"coordenada y cruda: {round(y_mean)}") 
print(f"coordenada z cruda: {round(z_mean)}")
print("calculando parametros de tranformacion a coordenadas UTM")
a = 6378137
b = 6356752.314 
#funcion de exentricidad 
def ex(a,b):
    den = a**2 - b**2
    num = a**2
    exentricidad = den / num 
    den1 = a**2 - b**2
    num2 = b**2
    exentricidad_prin = den1/num2
    return [exentricidad , exentricidad_prin] 
e = ex(a,b)[0]
e_prim = ex(a,b)[1] 
#funcion convertir de radianes a metros
def radianes_a_grados(radianes):
    ra = 180 *(radianes/math.pi)
    return ra 
#funcion valor de p 
def p(x,y):
    p = math.sqrt(x**2 + y**2)
    return p 
p = p(x_mean,y_mean) 
#funcion de theta
def theta(z,a,p,b):
    Za = z*a
    Pb = p*b
    theta = math.atan(Za/Pb)
    return theta 
#ϴ = theta(z3_total,a,p,b)  #funcion en radianes 
theta_g = radianes_a_grados(theta(z_mean,a,p,b))
#funcion para sacar phi
def phi(z,e2,b,ϴ,p,e,a):
    den = z + (e2*b*math.sin(ϴ)**3)
    num = p - (e*a*math.cos(ϴ)**3)
    phi = math.atan(den / num)
    return phi  
angulo = phi(z_mean,e_prim,b,theta_g,p,e,a)
phi2 = radianes_a_grados(phi(z_mean,e_prim,b,theta_g,p,e,a))  #funcion a radianes 
#funcion para sacar N 
def N(a,e2,phi):
    num = math.sqrt(1-e2*math.sin(phi)**2)
    N = a / num
    return N 
N = N(a,e,phi2) 
#funcion para sacar h 
def h(p,phi,N):
    fraccion = p/math.cos(phi) 
    h = fraccion - N 
    return h 
h = h(p,angulo,N) 
#funcion para calcular lamba 
def lamba(y,x):
    lamda = math.atan(y/x) 
    return lamda 
l = lamba(y_mean, x_mean)
lamba_g = radianes_a_grados(l) 
print("coordenadad geodesicas calculadas")
print("coordenada X geodesica es: " , round(phi2,3)) 
print("coordenada Y geodesica es:" , round(lamba_g,3))
print("coordenada z es: " , round(h,3))  
    

                        






