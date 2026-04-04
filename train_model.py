from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training data
questions = [
    "hi",
    "hello",
    "capital of india",
    "prime minister of india"
]

answers = [
    "Hello 👋",
    "Hello 👋",
    "New Delhi",
    "Narendra Modi"
]

# Convert text → numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(questions)

# Train model
model = MultinomialNB()
model.fit(X, answers)

# Save model
import pickle
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained ✅")