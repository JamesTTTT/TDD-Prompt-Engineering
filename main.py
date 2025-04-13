"""
Concert Itinerary Builder
This module provides functionality to build an itinerary of upcoming concerts.
"""

class Concert:
    """
    Represents a concert event.
   
    Attributes:
        artist (str): The name of the artist performing.
        date (str): The date of the concert in 'YYYY-MM-DD' format.
        location (str): The location where the concert will take place.
        latitude (float): Latitude coordinate of the concert location.
        longitude (float): Longitude coordinate of the concert location.
    """
   
    def __init__(self, artist, date, location, latitude, longitude):
        self.artist = artist
        self.date = date
        self.location = location
        self.latitude = latitude
        self.longitude = longitude


class ItineraryBuilder:
    """
    A class to build concert itineraries.
    """
    def __init__(self):
        self.available_artists = set()
    
    def build_itinerary(self, concerts):
        """
        Build an optimized concert itinerary from the given list of concerts.
        
        The itinerary will:
        - Include only one concert per artist
        - Have no more than one concert per date
        - Prioritize artists with only one concert opportunity
        - Be sorted by date
        
        Args:
            concerts (list): List of Concert objects
            
        Returns:
            list: Optimized list of Concert objects representing the itinerary
        """
        self.available_artists = set(concert.artist for concert in concerts)

        artist_concert_count = {}
        for concert in concerts:
            artist_concert_count[concert.artist] = artist_concert_count.get(concert.artist, 0) + 1
        
        concerts_by_date = {}
        for concert in concerts:
            if concert.date not in concerts_by_date:
                concerts_by_date[concert.date] = []
            concerts_by_date[concert.date].append(concert)
        
        selected_concerts = []
        selected_artists = set()
        sorted_dates = sorted(concerts_by_date.keys())
        
        for date in sorted_dates:
            date_concerts = concerts_by_date[date]
            
            if any(concert.date == date for concert in selected_concerts):
                continue
            
            single_concert_options = [c for c in date_concerts 
                                      if artist_concert_count[c.artist] == 1 
                                      and c.artist not in selected_artists]
            
            if single_concert_options:
                selected_concerts.append(single_concert_options[0])
                selected_artists.add(single_concert_options[0].artist)
            else:
                multi_concert_options = [c for c in date_concerts 
                                        if c.artist not in selected_artists]
                
                if multi_concert_options:
                    selected_concerts.append(multi_concert_options[0])
                    selected_artists.add(multi_concert_options[0].artist)
        
        return sorted(selected_concerts, key=lambda x: x.date)
   
    def is_artist_missing(self, artist_name):
        """
        Check if an artist is missing from the available artists.
        """
        if not self.available_artists:
            return True
       
        return artist_name not in self.available_artists


if __name__ == "__main__":
    from concerts_data import get_all_concerts
   
    all_concerts = get_all_concerts()
    builder = ItineraryBuilder()
    itinerary = builder.build_itinerary(all_concerts)
    
    print(f"Itinerary contains {len(itinerary)} concerts:")
    for concert in itinerary:
        print(f"{concert.date}: {concert.artist} at {concert.location}")