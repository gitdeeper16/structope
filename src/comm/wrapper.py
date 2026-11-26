"""
CommWrapper — Wrapper for C1-C4 communication mechanisms in HeMAC.
This wrapper allows testing communication faults without modifying HeMAC itself.
"""

import numpy as np
from gymnasium.utils import seeding
from hemac.helpers.helper import world_ref_to_game_ref


class CommWrapper:
    """Wrapper لآليات الاتصال C1-C4."""
    
    def __init__(self, env, comm_mode="C0", loss_rate=0.3, delay_steps=5):
        """
        Args:
            env: HeMAC environment (PettingZoo AEC)
            comm_mode: "C0", "C1", "C2", "C3", "C4"
            loss_rate: for C1 (packet loss probability)
            delay_steps: for C2 (delay in steps)
        """
        self.env = env
        self.comm_mode = comm_mode
        self.loss_rate = loss_rate
        self.delay_steps = delay_steps
        self.rng = np.random.default_rng(42)
        self.current_step = 0
        self.last_known_comm = None
        self.delayed_buffer = []
        
        raw = env.unwrapped
        self.core = raw.env
        self.world = self.core.world
    
    def apply_comm_effect(self):
        """Apply the communication effect based on comm_mode."""
        if not hasattr(self.world, 'observer_communication'):
            return
        
        current_comm = list(self.world.observer_communication)
        if current_comm is None or any(c is None for c in current_comm):
            return
        
        if self.comm_mode == "C0":
            # Baseline: no effect
            self.last_known_comm = current_comm
        
        elif self.comm_mode == "C1":
            # Random packet loss
            if self.rng.random() < self.loss_rate:
                if self.last_known_comm is not None:
                    self.world.observer_communication = self.last_known_comm
            else:
                self.last_known_comm = current_comm
        
        elif self.comm_mode == "C2":
            # Communication delay
            self.delayed_buffer.append(current_comm)
            if len(self.delayed_buffer) > self.delay_steps:
                old_comm = self.delayed_buffer.pop(0)
                self.world.observer_communication = old_comm
            else:
                if self.last_known_comm is not None:
                    self.world.observer_communication = self.last_known_comm
        
        elif self.comm_mode == "C3":
            # Partial partition: keep last known
            if self.last_known_comm is not None:
                self.world.observer_communication = self.last_known_comm
            else:
                self.last_known_comm = current_comm
        
        elif self.comm_mode == "C4":
            # Topology change: reduce sensing_range
            for agent in self.core.agents_list:
                if agent.__class__.__name__ == "Observer":
                    if hasattr(agent, 'sensor') and hasattr(agent.sensor, 'sensing_range'):
                        agent.sensor.sensing_range = 30
    
    def reset(self, seed=42):
        """Reset environment and wrapper."""
        raw = self.env.unwrapped
        core = raw.env
        
        # Fix randomizer before reset
        rng, _ = seeding.np_random(seed)
        core.randomizer = rng
        if hasattr(core, 'world'):
            core.world.randomizer = rng
        
        result = self.env.reset(seed=seed)
        
        # Place Observer directly above POI to ensure detection
        if core.goals:
            goal_x = core.goals[0].x
            goal_y = core.goals[0].y
            for agent in core.agents_list:
                if agent.__class__.__name__ == "Observer":
                    agent.x = goal_x
                    agent.y = goal_y
                    rect_pos = world_ref_to_game_ref([agent.x, agent.y], core.world.area)
                    agent.rect.centerx = rect_pos[0]
                    agent.rect.centery = rect_pos[1]
                    break
        
        self.current_step = 0
        self.last_known_comm = None
        self.delayed_buffer = []
        
        return result
    
    def step(self, action):
        """Step environment and apply comm effect."""
        result = self.env.step(action)
        self.current_step += 1
        self.apply_comm_effect()
        return result
    
    def close(self):
        self.env.close()
    
    def __getattr__(self, name):
        """Forward other attributes to env."""
        return getattr(self.env, name)
