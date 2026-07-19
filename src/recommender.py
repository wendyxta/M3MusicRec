from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load and return all songs from a CSV file as a list of dicts."""
    print(f"Loading songs from {csv_path}...")

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
            
    print("Loaded songs: 20")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return the score with reasons."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song.get("genre", "").lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match: +1.5 points
    if song.get("mood", "").lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.5
        reasons.append(f"mood match (+1.5)")

    # Energy proximity: up to +1.0 point based on how close energy is to target
    # Score = 1.0 - |song_energy - target_energy|, clamped to [0, 1]
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_diff = abs(song.get("energy", 0.5) - target_energy)
    energy_score = round(max(0.0, 1.0 - energy_diff), 2)
    if energy_score > 0:
        score += energy_score
        reasons.append(f"energy proximity (+{energy_score})")

    # Acousticness bonus: +0.5 if user likes acoustic and song is acoustic (acousticness > 0.5)
    if user_prefs.get("likes_acoustic", False) and song.get("acousticness", 0.0) > 0.5:
        score += 0.5
        reasons.append(f"acoustic match (+0.5)")

    return (round(score, 2), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top-k results with scores and reasons."""
    # Score every song in the catalog using score_song as the judge
    scored = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # sorted() returns a NEW list sorted highest-to-lowest score; the original
    # `songs` list is left untouched (unlike .sort(), which mutates in place)
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # Take the top k results and format the reasons list into a readable string
    return [
        (song, score, ", ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in ranked[:k]
    ]
