![Converter Health Telemetry Guard CI](https://github.com/Haidriyam/converter-health-telemetry-guard/actions/workflows/devsecops-ci.yml/badge.svg)

# Wide-Bandgap GaN/SiC Inverter Degradation Sentinel

A prognostic health monitoring (PHM) and electro-thermal telemetry guard for wide-bandgap (GaN/SiC) semiconductors in high-density DC-DC converters (48V-to-POL data center power stages). By decoupling non-linear junction temperature dynamics ($T_j$) from electrical conduction losses, it isolates genuine on-state drain-source resistance drift ($\Delta R_{ds(on)}$) caused by lattice aging or bond-wire degradation, triggering autonomous preventative alarms before flashover failure.

```text
[ Sensor Telemetry: V_drop, I_load, T_case ]
                     │
                     ▼
       [ Foster Electro-Thermal Model ]
       (Decouples Reversible Thermal Drift)
                     │
                     ▼
  [ Temperature-Compensated Rds(on) Observer ]
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 [ Healthy Operating Band ]  [ Failure Warning (ΔR > 15%) ]