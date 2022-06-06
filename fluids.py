#!/usr/bin/python3

class System:
    g = -9.81;
    def __init__(self,material,U,Lc,Tbulk=None,Tsurf=None):
        self.material = material;
        self.U = U;
        self.Lc = Lc;
        if Tbulk:
            self.Tbulk = Tbulk;
        if Tsurf:
            self.Tsurf = Tsurf;
    def Re(self):
        return self.material.rho * self.U * self.Lc / self.material.mu;

    ## Thermal ##
    def Pr(self):
        assert self.material.thermal_properties, f'Thermal properties missing from material data';
        return self.material.Cp * self.material.mu / self.material.k;
    def Gr(self):
        assert self.material.thermal_properties, f'Thermal properties missing from material data';
        assert self.Tbulk*self.Tsurf, f'Missing either Tbulk or Tsurf';
        return g*self.material.Beta * (Tsurf-Tbulk) * self.Lc**3 / (self.material.nu);
    def Ra(self):
        return self.Pr()*self.Gr();
    


class Material:
    '''
    Initialize with rho,mu or with coolprop using CP={'air':{'T':298.15,'P':101325}}
    '''
    def __init__(self,rho=None,mu=None,CP=None):
        if CP:
            from CoolProp.CoolProp import PropsSI as props
            from itertools import chain
            fluid = list(CP.keys())[0]
            state = list(chain(*list(CP.values())[0].items()))
            keys = ['D','V','C','L','isobaric_expansion_coefficient']
            rho,mu,Cp,k,Beta = [props(key,*state,fluid) for key in keys]
            self.rho = rho;
            self.mu  = mu;
            self.thermal(Cp,k,Beta)
        else:
            self.rho = rho;
            self.mu  = mu;
        self.nu = self.mu/self.rho;
    def thermal(self,Cp,k,Beta):
        self.Cp = Cp;
        self.k = k;
        self.alpha = k/(self.rho * Cp);
        self.α = self.alpha;
        self.Beta = Beta;
        self.β = Beta;
        self.thermal_properties = True;
