"""
Wide-Bandgap (GaN/SiC) Switching Device & Electro-Thermal Dynamics.
Models temperature-dependent conduction losses and transient junction heating.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class SwitchParameters:
    rds_on_nominal_mohm: float = 12.0     # 12 mOhm at 25 deg C
    temp_coefficient_alpha: float = 0.006  # +0.6% resistance increase per deg C
    r_th_jc_c_per_w: float = 1.2          # Junction-to-case thermal resistance (C/W)
    c_th_j_j_per_c: float = 0.05          # Junction thermal capacitance (J/C)


class GaNSwitchDevice:
    def __init__(self, params: SwitchParameters = SwitchParameters()):
        self.params = params
        self.t_junction_c = 25.0
        self.aging_factor = 1.0  # Multiplier representing gate-oxide/bond degradation

    def get_physical_resistance(self, t_junction_c: float) -> float:
        """Calculate true theoretical on-resistance (Ohms) at current junction temperature."""
        r_nominal = self.params.rds_on_nominal_mohm * 1e-3
        delta_t = t_junction_c - 25.0
        r_temp_comp = r_nominal * (1.0 + self.params.temp_coefficient_alpha * delta_t)
        return float(r_temp_comp * self.aging_factor)

    def step_thermal_dynamics(
        self,
        current_load_a: float,
        t_case_c: float,
        dt_seconds: float = 0.001
    ) -> float:
        """
        Integrate junction temperature differential equation:
        C_th * dTj/dt = P_loss - (Tj - Tcase) / R_th
        """
        r_eff = self.get_physical_resistance(self.t_junction_c)
        p_conduction = (current_load_a**2) * r_eff

        tau = self.params.r_th_jc_c_per_w * self.params.c_th_j_j_per_c
        dT_dt = (t_case_c - self.t_junction_c + self.params.r_th_jc_c_per_w * p_conduction) / tau

        self.t_junction_c += dT_dt * dt_seconds
        return float(self.t_junction_c)