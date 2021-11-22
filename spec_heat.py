'''
Calculate heat capacity for a given temperature and magnetic field
'''
import numpy as np
import scipy.integrate

a = 1 #lattice constant
muB = 5.7883818012e-5 #In units eV/T
kB = 8.617333262145e-5 #In units eV/K
NA = 6.02214076e23 #Avogadros number = 1 mol
eVtoJoule = 1.602176634e-19 #1eV in Joules
g = 2 #g-factor
J = 8.2/1000 #Ferromagnetic exchange in eV


#Define primitive lattice vectors (FCC in this case)
a1 = np.array([1,1,0])*a/2
a2 = np.array([0,1,-1])*a/2
a3 = np.array([1,0,-1])*a/2

#Unit cell volume
V = np.dot(a1,np.cross(a2,a3))

#Reciprocal lattice vectors
b1 = 2*np.pi*np.cross(a2,a3)/V
b2 = 2*np.pi*np.cross(a3,a1)/V
b3 = 2*np.pi*np.cross(a1,a2)/V

#Brillouin zone volume
Vbz = np.dot(b1,np.cross(b2,b3))

#Transformation matrix
B = np.zeros((len(a1),len(a1)))
B[:,0], B[:,1], B[:,2] = b1, b2, b3


def E_mag(k_vec,H):
    '''
    Return energy of lowest magnon branch in units of eV
    '''
    kx, ky, kz = k_vec
    Fk = np.cos(kx*a/2)*np.cos(ky*a/2)+np.cos(kx*a/2)*np.cos(kz*a/2)+np.cos(ky*a/2)*np.cos(kz*a/2)
    
    return muB*g*H+2*J-J*np.sqrt(1+Fk)

def x_func(E,T):
    
    return E/(kB*T)

def integrand(q_vec,T,H):
    '''Integrand for heat capacity integral'''
    k_vec = B@np.array(q_vec)
    xk = x_func(E_mag(k_vec,H),T)
    
    return xk**2*np.exp(xk)/(np.exp(xk)-1)**2

def Cmag(T,H):
    '''Calculate heat capacity in units of kB'''
    
    #Redefine integrand in terms of rescaled momentum q
    g = lambda qz, qy, qx: integrand([qx,qy,qz],T,H)
    print('Running')
    #Integrate over the unit cube
    res = scipy.integrate.tplquad(g, 0, 1, lambda x: 0, lambda x: 1,lambda x, y: 0, lambda x, y: 1)
    
    return res[0],res[1]
