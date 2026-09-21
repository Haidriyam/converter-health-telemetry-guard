import unittest
from converter.switch_model import GaNSwitchDevice, SwitchParameters
from converter.degradation_sentinel import ConverterHealthSentinel


class TestConverterHealthMonitoring(unittest.TestCase):

    def setUp(self):
        self.params = SwitchParameters(
            rds_on_nominal_mohm=12.0,
            temp_coefficient_alpha=0.006,
            r_th_jc_c_per_w=1.2,
            c_th_j_j_per_c=0.05
        )
        self.switch = GaNSwitchDevice(self.params)
        self.sentinel = ConverterHealthSentinel(self.params)

    def test_thermal_dynamics_without_degradation(self):
        # Healthy switch under sustained 20A load at 60 deg C case temp
        i_load = 20.0
        t_case = 60.0

        for _ in range(100):
            self.switch.step_thermal_dynamics(i_load, t_case, dt_seconds=0.01)

        # Measure simulated terminal voltage drop
        r_actual = self.switch.get_physical_resistance(self.switch.t_junction_c)
        v_drop = i_load * r_actual

        metrics = self.sentinel.evaluate_switch_health(
            v_drop_measured_v=v_drop,
            i_load_measured_a=i_load,
            t_case_c=t_case
        )

        # Baseline healthy switch must NOT raise degradation alarms despite high Tj
        self.assertEqual(metrics["alarm_state"], 0.0)
        self.assertLess(abs(metrics["aging_deviation_pct"]), 3.0)

    def test_aged_device_alarm_trigger(self):
        # Simulate an aged switch (20% degradation over nominal)
        self.switch.aging_factor = 1.20
        i_load = 20.0
        t_case = 50.0

        for _ in range(50):
            self.switch.step_thermal_dynamics(i_load, t_case, dt_seconds=0.01)

        r_aged = self.switch.get_physical_resistance(self.switch.t_junction_c)
        v_drop = i_load * r_aged

        metrics = self.sentinel.evaluate_switch_health(
            v_drop_measured_v=v_drop,
            i_load_measured_a=i_load,
            t_case_c=t_case
        )

        # Must flag alarm state (1.0) because degradation exceeds 15%
        self.assertEqual(metrics["alarm_state"], 1.0)
        self.assertAlmostEqual(metrics["aging_deviation_pct"], 20.0, delta=2.5)

    def test_low_current_idling_condition(self):
        metrics = self.sentinel.evaluate_switch_health(0.001, 0.2, 25.0)
        self.assertEqual(metrics["alarm_state"], 0.0)
        self.assertEqual(metrics["aging_deviation_pct"], 0.0)


if __name__ == "__main__":
    unittest.main()