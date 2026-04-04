from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# 🔥 More training data
questions = [
    "hi", "hello", "hey",
    "how are you",

    # Capital
    "capital of india",
    "india capital",
    "what is capital",
    "tell me capital of india",

    # PM
    "prime minister of india",
    "pm of india",
    "who is pm",
    "india pm",
    "who is prime minister",

    # Father of nation
    "father of nation",
    "father of india",
    "who is father of nation",

    # Math
    "2+2",
    "calculate 2+2",
    "what is 2+2"
]

answers = [
    "Hello 👋", "Hello 👋", "Hello 👋",
    "I am fine 😊",

    # Capital (4 answers)
    "New Delhi",
    "New Delhi",
    "New Delhi",
    "New Delhi",

    # PM (5 answers)
    "Narendra Modi",
    "Narendra Modi",
    "Narendra Modi",
    "Narendra Modi",
    "Narendra Modi",

    # Father of nation (3 answers)
    "Mahatma Gandhi",
    "Mahatma Gandhi",
    "Mahatma Gandhi",

    # Math (3 answers)
    "4",
    "4",
    "4"
]
# Vectorize
vectorizer = CountVectorizer(ngram_range=(1,2))
X = vectorizer.fit_transform(questions)

# Train
model = MultinomialNB()
model.fit(X, answers)

# Save
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Improved model trained ✅")