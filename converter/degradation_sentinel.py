"""
Online On-State Resistance (Rds_on) Degradation Sentinel.
Decouples thermal effects from physical device wear to isolate impending failure.
"""
from typing import Dict
from converter.switch_model import SwitchParameters


class ConverterHealthSentinel:
    def __init__(self, params: SwitchParameters = SwitchParameters()):
        self.params = params
        self.r_nominal = self.params.rds_on_nominal_mohm * 1e-3
        self.degradation_threshold_pct = 15.0  # Industry standard warning boundary

    def evaluate_switch_health(
        self,
        v_drop_measured_v: float,
        i_load_measured_a: float,
        t_case_c: float
    ) -> Dict[str, float]:
        """
        Extract temperature-compensated degradation metric from real-time telemetry:
        1. Calculate raw apparent resistance: R_app = V_drop / I_load
        2. Estimate junction temperature Tj based on steady-state thermal model
        3. Normalize back to 25 deg C reference resistance
        4. Compute aging percentage deviation against factory baseline
        """
        if abs(i_load_measured_a) < 1.0:
            return {
                "aging_deviation_pct": 0.0,
                "alarm_state": 0.0,
                "r_extracted_25c_mohm": self.params.rds_on_nominal_mohm,
            }

        # 1. Raw apparent resistance
        r_raw = v_drop_measured_v / i_load_measured_a

        # 2. Steady-state junction temperature estimate: Tj = Tcase + P_loss * Rth
        p_loss_est = v_drop_measured_v * i_load_measured_a
        t_j_est = t_case_c + p_loss_est * self.params.r_th_jc_c_per_w

        # 3. Normalize resistance back to 25 deg C baseline
        delta_t = t_j_est - 25.0
        thermal_scaling = 1.0 + self.params.temp_coefficient_alpha * delta_t
        r_25c_est = r_raw / thermal_scaling

        # 4. Degradation deviation percentage
        delta_pct = ((r_25c_est - self.r_nominal) / self.r_nominal) * 100.0
        alarm_active = 1.0 if delta_pct >= self.degradation_threshold_pct else 0.0

        return {
            "aging_deviation_pct": float(delta_pct),
            "alarm_state": float(alarm_active),
            "r_extracted_25c_mohm": float(r_25c_est * 1000.0),
        }