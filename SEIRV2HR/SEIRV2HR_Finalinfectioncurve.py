import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class SEIRSV2_Model():

    def __init__(self):
        self.TotalTime          = 1000 
        self.dt                 = 1
        self.Iterations         = int(self.TotalTime/self.dt)
        self.PopulationLR       = 0.9
        self.PopulationHR       = 0.1
        self.Population         = self.PopulationLR + self.PopulationHR
        self.InitalExposuresLR  = 0.04
        self.InitalExposuresHR  = 0.01

        self.BirthRateLR        = (2.78363e-5)*0.9
        self.BirthRateHR        = (2.78363e-5)*0.1
        self.DeathRate          = 2.48321e-5
        self.DeathRateCOVID     = 8.95027e-4
        self.DeathRateCOVIDHR   = self.DeathRateCOVID * 2
        self.DeathRateCOVIDSV   = self.DeathRateCOVID * 0.19
        self.DeathRateCOVIDDV   = self.DeathRateCOVID * 0.09
        self.DeathRateCOVIDSVHR = self.DeathRateCOVIDHR * 0.19
        self.DeathRateCOVIDDVHR = self.DeathRateCOVIDHR * 0.09

        self.ContactRate        = 1/7
        self.ContactRateV1      = self.ContactRate * 0.19
        self.ContactRateV2      = self.ContactRate * 0.09
        self.ContactRateHR      = self.ContactRate * 2
        self.ContactRateHRV1    = self.ContactRateHR * 0.19
        self.ContactRateHRV2    = self.ContactRateHR * 0.09
        self.LatencyRate        = 1/3
        self.RecoveryRate       = 1/10
        self.ImmunityLossRate   = 1/210
        self.Vaccination1Rate   = 1/2000
        self.Vaccination2Rate   = 1/5000
        self.Vaccination1HRRate = 1/50
        self.Vaccination2HRRate = 1/250

    def NumInt(self):

        S = [self.PopulationLR - self.InitalExposuresLR]; E = [self.InitalExposuresLR]; I = [0]; R = [0]
        V1 = [0]; EV1 = [0]; IV1 = [0]
        V2 = [0]; EV2 = [0]; IV2 = [0]
        SHR = [self.PopulationHR - self.InitalExposuresHR]; EHR = [self.InitalExposuresHR]; IHR = [0]; RHR = [0]
        V1HR = [0]; EV1HR = [0]; IV1HR = [0]
        V2HR = [0]; EV2HR = [0]; IV2HR = [0]

        dt = self.dt

        for n in range(0,self.Iterations):

            InfectionProb = (I[n]+E[n]+IV1[n]+EV1[n]+EV2[n]+IV2[n]+EHR[n]+IHR[n]+EV1HR[n]+IV1HR[n]+EV2HR[n]+IV2HR[n])/self.Population
            
            NewInfections = self.ContactRate * InfectionProb * S[n]
            NewInfectionsV1 = self.ContactRateV1 * InfectionProb * V1[n]
            NewInfectionsV2 = self.ContactRateV2 * InfectionProb * V2[n]
            NewInfectionsHR = self.ContactRateHR * InfectionProb * SHR[n]
            NewInfectionsV1HR = self.ContactRateHRV1 * InfectionProb * V1HR[n]
            NewInfectionsV2HR = self.ContactRateHRV2 * InfectionProb * V2HR[n]

            dS = -NewInfections + self.ImmunityLossRate*R[n] - self.Vaccination1Rate*S[n] + self.Population*self.BirthRateLR - self.DeathRate*S[n]
            dE = -self.LatencyRate*E[n] + NewInfections - self.DeathRate*E[n]
            dI = self.LatencyRate*E[n] - self.RecoveryRate*I[n] - self.DeathRateCOVID*I[n]
            dR = self.RecoveryRate*I[n] - self.ImmunityLossRate*R[n] - self.Vaccination1Rate*R[n] - self.DeathRate*R[n]

            dV1 = self.Vaccination1Rate*(S[n] + R[n]) - self.Vaccination2Rate*V1[n] - NewInfectionsV1 + self.RecoveryRate*IV1[n] - self.DeathRate*V1[n]
            dEV1 = - self.LatencyRate*EV1[n] + NewInfectionsV1 - self.DeathRate*EV1[n]
            dIV1 = self.LatencyRate*EV1[n] - self.RecoveryRate*IV1[n] - self.DeathRateCOVIDSV*IV1[n]

            dV2 = self.Vaccination2Rate*V1[n] - NewInfectionsV2 + self.RecoveryRate*IV2[n] - self.DeathRate*V2[n]
            dEV2 = NewInfectionsV2 - self.LatencyRate*EV2[n] - self.DeathRate*EV2[n]
            dIV2 = self.LatencyRate*EV2[n] - self.RecoveryRate*IV2[n] - self.DeathRateCOVIDDV*IV2[n]

            dSHR = -NewInfectionsHR + self.ImmunityLossRate*RHR[n] - self.Vaccination1HRRate*SHR[n] + self.Population*self.BirthRateHR - self.DeathRate*SHR[n]
            dEHR = NewInfectionsHR - self.LatencyRate*EHR[n] - self.DeathRate*EHR[n]
            dIHR = self.LatencyRate*EHR[n] - self.RecoveryRate*IHR[n] - self.DeathRateCOVIDHR*IHR[n]
            dRHR = -self.ImmunityLossRate*RHR[n] + self.RecoveryRate*IHR[n] - self.Vaccination1HRRate*RHR[n] - self.DeathRate*RHR[n]

            dV1HR = self.Vaccination1HRRate*(SHR[n] + RHR[n]) - self.Vaccination2HRRate*V1HR[n] - NewInfectionsV1HR + self.RecoveryRate*IV1HR[n] - self.DeathRate*V1HR[n]
            dEV1HR = NewInfectionsV1HR - self.LatencyRate*EV1HR[n] - self.DeathRate*EV1HR[n]
            dIV1HR = self.LatencyRate*EV1HR[n] - self.RecoveryRate*IV1HR[n] - self.DeathRateCOVIDSVHR*V1HR[n]

            dV2HR = self.Vaccination2HRRate*V1HR[n] - NewInfectionsV2HR + self.RecoveryRate*IV2HR[n] - self.DeathRate*V2HR[n]
            dEV2HR = NewInfectionsV2HR - self.LatencyRate*EV2HR[n] - self.DeathRate*EV2HR[n]
            dIV2HR = self.LatencyRate*EV2HR[n] - self.RecoveryRate*IV2HR[n] - self.DeathRateCOVIDDVHR*IV2HR[n]

            self.Population += (dS+dE+dI+dR+dV1+dV2+dEV1+dEV2+dIV1+dIV2+dSHR+dEHR+dIHR+dRHR+dV1HR+dEV1HR+dIV1HR+dV2HR+dEV2HR+dIV2HR)*dt

            S.append(S[n] + dS*dt); E.append(E[n] + dE*dt); I.append(I[n] + dI*dt); R.append(R[n] + dR*dt)
            V1.append(V1[n] + dV1*dt); EV1.append(EV1[n] + dEV1*dt); IV1.append(IV1[n] + dIV1*dt)
            V2.append(V2[n] + dV2*dt); EV2.append(EV2[n] + dEV2*dt); IV2.append(IV2[n] + dIV2*dt)
            SHR.append(SHR[n] + dSHR*dt); EHR.append(EHR[n] + dEHR*dt); IHR.append(IHR[n] + dIHR*dt); RHR.append(RHR[n] + dRHR*dt)
            V1HR.append(V1HR[n] + dV1HR*dt); EV1HR.append(EV1HR[n] + dEV1HR*dt); IV1HR.append(IV1HR[n] + dIV1HR*dt)
            V2HR.append(V2HR[n] + dV2HR*dt); EV2HR.append(EV2HR[n] + dEV2HR*dt); IV2HR.append(IV2HR[n] + dIV2HR*dt)

        plt.plot(np.array(I) + np.array(IV1) + np.array(IV2) + np.array(IHR) + np.array(IV1HR) + np.array(IV2HR) + np.array(E) + np.array(EV1) + np.array(EV2) + np.array(EHR) + np.array(EV1HR) + np.array(EV2HR), label = "Infectious", c = '#b81111')
        plt.title("SEIRV2HR Model Lineplot")
        plt.xlabel("Time (Days)")
        plt.ylabel("Proportion of Population")
        plt.legend()
        plt.savefig("SEIRV2HRInfectioncurve.png", dpi=227) 


if __name__ == "__main__":
    SEIRSV2 = SEIRSV2_Model()
    SEIRSV2.NumInt()