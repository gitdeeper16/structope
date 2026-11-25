from structope import FaultType, Severity, Timing, inject_fault


def test_all_cells_count():
    from structope.fault_injection import all_cells
    cells = all_cells()
    assert len(cells) == 8 * 3


def test_fault_type_values():
    assert FaultType.AGENT_DROPOUT.value == "agent_dropout"
    assert FaultType.TOPOLOGY_CHANGE.value == "topology_change"
    assert len(list(FaultType)) == 8
