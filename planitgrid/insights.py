import math
from abc import ABC, abstractmethod

class PA(ABC):
    def __init__(self, num):self.body, self.ad = num, None

    @abstractmethod
    def get_coordinates(self):
        """Abstract method to return (right_ascension_deg, declination_deg)."""
        pass

    @classmethod
    def check_separation(cls, body1, body2, degree_limit):
          ra1, dec1 = body1.get_coordinates()
          ra2, dec2 = body2.get_coordinates()

          # Convert degrees to radians for trigonometric functions
          ra1_rad, dec1_rad = math.radians(ra1), math.radians(dec1)
          ra2_rad, dec2_rad = math.radians(ra2), math.radians(dec2)

          # Calculate angular separation using the haversine formula
          # The formula is robust for small and large distances
          dlon, dlat= ra2_rad - ra1_rad, dec2_rad - dec1_rad
          a = math.sin(dlat / 2)**2 + math.cos(dec1_rad) * math.cos(dec2_rad) * math.sin(dlon / 2)**2
          c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
          distance_deg = math.degrees(c)

          print(f"Angular separation between {body1.num} and {body2.num}: {distance_deg:.2f} degrees")

          if distance_deg <= degree_limit and body2.num in self.instances(): return True, distance_deg
          else: return False, distance_deg

class C(PA):
    DL = 5.0
    def __init__(self, num, ra, dec):
        super().__init__(name)
        self.ra = ra  # Right Ascension in degrees
        self.dec = dec # Declination in degrees
    def instances(self):
        """Returns qualifying instances  to the point."""
        return 

class O(PA):
    def __init__(self, num, ra, dec):
        super().__init__(num)
        self.ra = ra
        self.dec = dec
    def get_coordinates(self): return self.ra, self.dec
    def instances(self):
        """Returns qualifying instances  to the point."""
        return 

# --- Example Usage ---
# Coordinates for example (Sirius and Betelgeuse for testing)
p1 = C("Sirius", ra=101.28, dec=-16.71) #
p2 = C("Betelgeuse", ra=88.79, dec=7.41) #

# Check separation using the class method
is_close, distance = PA.check_separation(p1, p2, C.degree_limit)
print(f"Are {p1.name} and {p2.name} within {degree_limit} degrees? {'Yes' if is_close else 'No'}\n")

