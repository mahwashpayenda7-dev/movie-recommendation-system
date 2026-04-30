from collections import deque
# INITIAL DATASET
initial_movies = {
    1: {"title": "The Matrix", "genres": ["Sci-Fi", "Action"], "sum_rating": 480, "count": 100},
    2: {"title": "Inception", "genres": ["Sci-Fi", "Action", "Thriller"], "sum_rating": 450, "count": 95},
    3: {"title": "Interstellar", "genres": ["Sci-Fi", "Drama"], "sum_rating": 470, "count": 100},
    4: {"title": "The Godfather", "genres": ["Crime", "Drama"], "sum_rating": 490, "count": 100},
    5: {"title": "Pulp Fiction", "genres": ["Crime", "Thriller"], "sum_rating": 430, "count": 90},
    6: {"title": "The Dark Knight", "genres": ["Action", "Crime", "Drama"], "sum_rating": 485, "count": 100},
    7: {"title": "Schindler's List", "genres": ["Drama", "History"], "sum_rating": 460, "count": 95},
    8: {"title": "Forrest Gump", "genres": ["Drama", "Romance"], "sum_rating": 440, "count": 100},
    9: {"title": "The Shawshank Redemption", "genres": ["Drama"], "sum_rating": 495, "count": 100},
    10: {"title": "Gladiator", "genres": ["Action", "Adventure", "Drama"], "sum_rating": 420, "count": 90},
    11: {"title": "Alien", "genres": ["Sci-Fi", "Horror"], "sum_rating": 380, "count": 85},
    12: {"title": "The Silence of the Lambs", "genres": ["Crime", "Horror", "Thriller"], "sum_rating": 410, "count": 90},
    13: {"title": "Seven", "genres": ["Crime", "Mystery", "Thriller"], "sum_rating": 390, "count": 85},
    14: {"title": "The Prestige", "genres": ["Drama", "Mystery", "Sci-Fi"], "sum_rating": 445, "count": 95},
    15: {"title": "Memento", "genres": ["Mystery", "Thriller"], "sum_rating": 405, "count": 90},
    16: {"title": "The Lion King", "genres": ["Animation", "Adventure", "Drama"], "sum_rating": 475, "count": 100},
    17: {"title": "Spirited Away", "genres": ["Animation", "Adventure", "Fantasy"], "sum_rating": 480, "count": 100},
    18: {"title": "Back to the Future", "genres": ["Sci-Fi", "Adventure", "Comedy"], "sum_rating": 455, "count": 100},
    19: {"title": "Blade Runner 2049", "genres": ["Sci-Fi", "Drama"], "sum_rating": 340, "count": 80},
    20: {"title": "Parasite", "genres": ["Drama", "Thriller", "Comedy"], "sum_rating": 465, "count": 100},
}

# HASH TABLE (MOVIES)

movies = {}

for mid, data in initial_movies.items():
    movies[mid] = {
        "title": data["title"],
        "genres": set(data["genres"]),
        "total_rating": data["sum_rating"],
        "rating_count": data["count"],
        "avg_rating": data["sum_rating"] / data["count"],
    }

# USER DATA

user_ratings = {}

#  Using deque for true O(1) queue
watch_history = deque(maxlen=5)

# GRAPH (ADJACENCY LIST)
graph = {i: set() for i in movies}

for i in movies:
    for j in movies:
        if i != j and movies[i]["genres"] & movies[j]["genres"]:
            graph[i].add(j)

# WATCH MOVIES

def watch_movie(movie_id):
    if movie_id not in movies:
        print(" Invalid movie ID")
        return

    watch_history.append(movie_id)
    print(f"✅ You watched: {movies[movie_id]['title']}")

# RATE MOVIE
def rate_movie(movie_id, rating):
    if movie_id not in movies:
        print("Invalid movie ID")
        return

    if rating < 1 or rating > 5:
        print(" Rating must be between 1 and 5")
        return

    m = movies[movie_id]
    m["total_rating"] += rating
    m["rating_count"] += 1
    m["avg_rating"] = m["total_rating"] / m["rating_count"]

    user_ratings[movie_id] = rating
    print(f" Rated {movies[movie_id]['title']} successfully!")


# TOP MOVIES

def top_movies():
    top = sorted(movies.items(), key=lambda x: x[1]["avg_rating"], reverse=True)[:5]
    print("\n🏆 Top 5 Movies:")
    for mid, data in top:
        print(f"{data['title']} | Rating: {round(data['avg_rating'],2)}")

# BFS RECOMMENDATION

def recommend(movie_id):
    if movie_id not in movies:
        print("Invalid movie ID")
        return

    visited = set()
    queue = deque([movie_id])
    recommendations = []

    while queue and len(recommendations) < 5:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in watch_history:
                visited.add(neighbor)
                queue.append(neighbor)
                recommendations.append(neighbor)

    print("\n Recommended Movies:")
    for mid in recommendations:
        print(movies[mid]["title"])

#  DISPLAY MOVIES
def show_movies():
    print("\n🎬 Movie List:")
    for mid, data in movies.items():
        print(f"{mid}. {data['title']} | Rating: {round(data['avg_rating'],2)}")

#  WATCH HISTORY

def show_history():
    print("\n Watch History:")
    if not watch_history:
        print("No movies watched yet.")
    for mid in watch_history:
        print(movies[mid]["title"])

# MENU SYSTEM

def menu():
    while True:
        print("\n===== MOVIE SYSTEM =====")
        print("1. Show Movies")
        print("2. Top 5 Movies")
        print("3. Watch Movie")
        print("4. Rate Movie")
        print("5. Watch History")
        print("6. Recommend Movies")
        print("0. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                show_movies()

            elif choice == "2":
                top_movies()

            elif choice == "3":
                mid = int(input("Movie ID: "))
                watch_movie(mid)

            elif choice == "4":
                mid = int(input("Movie ID: "))
                rating = float(input("Rating (1-5): "))
                rate_movie(mid, rating)

            elif choice == "5":
                show_history()

            elif choice == "6":
                mid = int(input("Movie ID: "))
                recommend(mid)

            elif choice == "0":
                print("👋 Goodbye!")
                break

            else:
                print("Invalid choice")

        except ValueError:
            print(" Please enter valid numbers only.")

# START PROGRAM

menu()
