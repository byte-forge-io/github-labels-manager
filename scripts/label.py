from dataclasses import (dataclass, asdict)

@dataclass
class Label:
    name: str
    description: str
    color: str

    def as_dict(self):
        """Convert the `Label` to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """Create a `Label` from a dictionary."""

        allowed = {"name", "color", "description"}
        filtered = { 
            key: value 

            for key, value in data.items() 
            if key in allowed 
        }

        return cls(**filtered)
