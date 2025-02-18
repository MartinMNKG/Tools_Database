import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import itertools
import pandas as pd 

temperatures = np.linspace(1000,2000,11)
equivalence_ratio = np.linspace(0.5,2,16)
test_cases = list(itertools.product(temperatures, equivalence_ratio))


gas = ct.Solution("./Mech_OptiSmoke_2/gen500.yaml")  # Ensure this mechanism supports NH3 and H2 combustion
dossier = "./Mech_OptiSmoke_2/Gen500"
nb = gas.n_species

for c in test_cases : 
    T, phi = c
    
    
    # Set initial temperature and pressure
    gas.TP = T, ct.one_atm # Temperature [K] and Pressure [Pa]

    # Define fuel and oxidizer composition
    fuel = {"NH3": 0.85, "H2": 0.15}
    oxidizer = {"O2": 0.21, "N2": 0.78, "AR": 0.01}

    # Set equivalence ratio (phi = 1.0 for stoichiometric conditions)
    gas.set_equivalence_ratio(phi=phi, fuel=fuel, oxidizer=oxidizer)

    # Create a constant-volume reactor
    reactor = ct.IdealGasConstPressureReactor(gas)
    reactor_network = ct.ReactorNet([reactor])

    # Compute equilibrium state for reference
    gas_equil = gas  # Copy gas state
    gas_equil.equilibrate("HP")  # Equilibrate at constant volume (H, P)
    state_equil = np.append(gas_equil.X, gas_equil.T)  # Store equilibrium state
    # print(state_equil)
    # Time integration parameters
    time = 0.0
    time_end = 1  # Total max simulation time (1 s)
    time_step = 1e-6  # 1 µs
    times = []
    temperatures = []
    residuals = []

    # Equilibrium detection parameters
    tolerance = 0.1  # Stop when residual is below 0.1%
    equilibrium_detected = False
   
    equilibrium_time = None  # Store time when equilibrium is detected
    states = ct.SolutionArray(gas, extra=["t"])
    
    # Run the simulation
    while time < time_end:
        time = reactor_network.step()  # Advance simulation
        times.append(time)
        temperatures.append(reactor.T)
        
        states.append(reactor.thermo.state, t=time)
        # Compute current state
        state_current = np.append(reactor.thermo.X, reactor.T)

        # Compute residual
        residual = (
            100
            * np.linalg.norm(state_equil - state_current, ord=np.inf)
            / np.linalg.norm(state_equil, ord=np.inf)
        )
        residuals.append(residual)
        # print(residual)
        # Check for equilibrium
        if residual < tolerance and not equilibrium_detected:
            equilibrium_detected = True
            equilibrium_time = time
            print(f"Equilibrium detected at t = {time:.6f} s, T = {reactor.T:.2f} K")
        
        # Stop simulation after extra_time past equilibrium
        if equilibrium_detected and (time - equilibrium_time) > 1 * equilibrium_time:
            break
    
    states.save(f"{dossier}/0Dreactor_{nb}S_ER{phi}_T{T}.csv",overwrite=True)   

    # df = pd.DataFrame(states[:, :])
    # df.to_csv(f"{dossier}/0Dreactor_{nb}S_ER{phi}_T{T}.csv")
    