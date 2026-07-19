"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs

taste_profile = {
    "favorite_genre": "Pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": True
}

def main() -> None:
    songs = load_songs("data/songs.csv")

    recommendations = recommend_songs(taste_profile, songs, k=5)

    print("\n" + "=" * 45)
    print("   Top 5 Recommendations For You")
    print("=" * 45)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} — {song['artist']}")
        print(f"    Score : {score:.2f} / 5.00")
        print(f"    Why   : {explanation}")
    print("\n" + "=" * 45)


if __name__ == "__main__":
    main()
