from dataclasses import dataclass

@dataclass
class ProgressStatus:
    total_steps: int = 0
    completed_steps: int = 0

    def get_progress_quotient(self) -> float:
        if self.total_steps == 0:
            return 0.0
        return self.completed_steps / self.total_steps
    
    def get_progress_percentage(self) -> float:
        return self.get_progress_quotient() * 100
    
    def get_progress_fraction(self) -> tuple[int, int]:
        return (self.completed_steps, self.total_steps)
