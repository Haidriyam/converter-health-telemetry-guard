"""
Wide-Bandgap Converter Health Monitoring & Degradation Analytics Module.
"""
from converter.switch_model import GaNSwitchDevice, SwitchParameters
from converter.degradation_sentinel import ConverterHealthSentinel

__all__ = ["GaNSwitchDevice", "SwitchParameters", "ConverterHealthSentinel"]