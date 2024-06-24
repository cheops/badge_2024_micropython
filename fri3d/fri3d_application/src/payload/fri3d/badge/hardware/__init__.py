from p0tat0.badge import *

if badge_type == FRI3D_BADGE_2022:
    from .badge_2022 import *

elif badge_type == FRI3D_BADGE_2024:
    from .badge_2024 import *

else:
    raise(OSError("Unknown badge type"))
