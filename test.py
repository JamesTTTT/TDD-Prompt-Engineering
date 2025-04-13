"""
Unit tests for the Concert Itinerary Builder.

This file contains unit tests for the ItineraryBuilder class in main.py.
Participants will implement tests based on the system specifications.
"""

import unittest
from main import Concert, ItineraryBuilder
from concerts_data import get_all_concerts

class ItineraryBuilderTest(unittest.TestCase):
    """Test cases for the ItineraryBuilder class."""
    
    def setUp(self):
        """Set up for the tests."""
        self.builder = ItineraryBuilder()
        
        self.all_concerts = get_all_concerts()
    
    # ----- Manual Test Cases -----
    # Participants will implement their manual test cases here. 
    
    def test_sorted_by_date(self):
        """Verify that the concerts are sorted by date"""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        itinerary_dates = [concert.date for concert in itinerary]
        self.assertEqual(itinerary_dates,sorted(itinerary_dates))
        

    def test_single_concert_per_artist(self):
        """Verify single concert per artist"""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        def countArtist(artist_name):
            count = 0
            for artist in itinerary:
                if(artist.artist == artist_name):
                    count+=1
            return count
        select_artist = itinerary[0].artist
        self.assertEqual(countArtist(select_artist), 1)

    def test_artist_with_no_concert(self):
        """Verify artists with no concerts"""
        specific_artist = "AC/DC"
        self.assertTrue(self.builder.is_artist_missing(specific_artist))

    def test_available_artists_initialization(self):
        """Verify that available_artists is populated during build_itinerary"""
        self.assertEqual(self.builder.available_artists, set())
    
    def test_available_artists_populated(self):
        """Verify that available_artists is populated during build_itinerary"""
        self.builder.build_itinerary(self.all_concerts)
        expected_artists = set(concert.artist for concert in self.all_concerts)
        self.assertEqual(self.builder.available_artists, expected_artists)
    
    def test_single_concert_per_date(self):
        """Verify no duplicate dates in itinerary"""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        dates = [concert.date for concert in itinerary]
        self.assertEqual(len(dates), len(set(dates)), "Itinerary contains duplicate dates")
    # ----- AI-Assisted Test Cases -----
    # Participants will implement their AI-assisted test cases here.
    # Please name your test in a way which indicates that these are AI-assisted test cases.
    def test_unique_dates(self):
        """Verify Unique dates"""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        dates = [concert.date for concert in itinerary]
        unique = set(dates)
        self.assertEqual(len(dates), len(unique))

    def test_itinerary_content_format(self):
        """Verify that the itinerary contains the required information for each concert"""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        
        self.assertTrue(len(itinerary) > 0, "Itinerary should not be empty")

        for concert in itinerary:
            self.assertTrue(hasattr(concert, 'artist'), "Concert should have artist attribute")
            self.assertIsNotNone(concert.artist, "Artist should not be None")
            self.assertNotEqual(concert.artist, "", "Artist should not be empty")
            
            self.assertTrue(hasattr(concert, 'date'), "Concert should have date attribute")
            self.assertIsNotNone(concert.date, "Date should not be None")
            self.assertNotEqual(concert.date, "", "Date should not be empty")
            self.assertTrue(hasattr(concert, 'location'), "Concert should have location attribute")
            self.assertIsNotNone(concert.location, "Location should not be None")
            self.assertNotEqual(concert.location, "", "Location should not be empty")

    def test_prioritize_single_concert_artists(self):
        """Verify artists with only one concert are prioritized over artists with multiple concerts"""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        
        artist_concert_count = {}
        for concert in self.all_concerts:
            artist_concert_count[concert.artist] = artist_concert_count.get(concert.artist, 0) + 1

        single_concert_artists = [artist for artist, count in artist_concert_count.items() if count == 1]

        multi_concert_artists = [artist for artist, count in artist_concert_count.items() if count > 1]
        
        itinerary_dates = [concert.date for concert in itinerary]
        
        for artist in single_concert_artists:
            artist_concert = next((c for c in self.all_concerts if c.artist == artist), None)
            if artist_concert:
                self.assertIn(artist_concert.date, itinerary_dates, 
                            f"Single-concert artist {artist} should be prioritized in the itinerary")
        
        for single_artist_concert in [c for c in self.all_concerts if c.artist in single_concert_artists]:
            same_date_multi_concerts = [c for c in self.all_concerts 
                                    if c.date == single_artist_concert.date 
                                    and c.artist in multi_concert_artists]
            
            if same_date_multi_concerts:
                chosen_artist_for_date = next((c.artist for c in itinerary if c.date == single_artist_concert.date), None)
                self.assertEqual(chosen_artist_for_date, single_artist_concert.artist,
                            f"Single-concert artist {single_artist_concert.artist} should be chosen over {same_date_multi_concerts[0].artist} on {single_artist_concert.date}")
if __name__ == "__main__":
    unittest.main()