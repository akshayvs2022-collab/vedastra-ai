# Vedastra AI Study Assistant - What to Build Next

If your goal is to build a **best-in-class AI for study and learning**, focus on this order:

## 1) Build a real learning loop (must-have)

Your current app answers questions, but next-level learning products improve with every session.

### Add these features first
- **User profiles**: grade, exam target, language preference, weak topics.
- **Session memory**: what the learner asked, what they got wrong, time spent.
- **Feedback capture**: "helpful/not helpful", "too easy/hard", "explain again".
- **Correction capture**: allow user/teacher to submit better answer.

### Why this matters
Without learning signals, the model cannot personalize or improve quality per student.

---

## 2) Upgrade from static Q&A to a tutor workflow

Use a structured response format instead of one-shot answers.

### Tutor response template
1. Direct answer (short)
2. Simple explanation
3. Example
4. Quick quiz (1-2 questions)
5. Next-step recommendation

### Add difficulty control
- Beginner / Intermediate / Advanced mode.
- Auto-adapt difficulty based on quiz performance.

---

## 3) Add retrieval over quality study content (RAG)

Right now the app uses exact sentence matching from a PDF. Upgrade this.

### Better pipeline
- Split documents into chunks.
- Compute embeddings for chunks.
- Store in vector DB (FAISS/Chroma/Pinecone).
- Retrieve top-k chunks per question.
- Generate answer with citations.

### Minimum quality bar
- Every long answer should cite source chunk/page.
- If confidence is low: say "I am not sure" and ask clarifying question.

---

## 4) Add exam-focused capabilities

For a study product, this is what makes users stay.

### Features
- Topic-wise test generator.
- Timed mock tests.
- Automatic evaluation and rubric.
- Performance analytics dashboard.
- Weak-topic revision planner.

### Output examples
- "You improved in Ecology by 18% this week."
- "Revise Biodiversity and Food Chain tomorrow (30 min)."

---

## 5) Personalization engine (core differentiator)

Build a recommendation layer using learner data.

### Personalization signals
- Accuracy by topic
- Average response time
- Mistake patterns
- Preferred explanation style
- Study streak

### Actions
- Recommend next best topic.
- Predict forget curve and schedule revision (spaced repetition).
- Adjust complexity and examples to learner profile.

---

## 6) Safety and quality for education

If this is for students, quality control is mandatory.

### Guardrails
- Refuse harmful/off-topic requests.
- Detect hallucinations via retrieval + confidence checks.
- Add moderation and age-appropriate filters.
- Add teacher review mode for generated content.

### Quality measurement
Track these metrics every week:
- Answer correctness rate
- Helpful feedback rate
- Quiz completion rate
- Learning gain (pre-test vs post-test)
- Retention (D1, D7, D30)

---

## 7) Technical architecture next steps

### Near-term stack
- **Backend**: Flask/FastAPI + PostgreSQL
- **Vector Store**: FAISS/Chroma
- **Queue**: Celery/RQ for background indexing
- **Model layer**: hybrid (rules + retrieval + ML classifier)
- **Observability**: structured logs + trace IDs + error dashboard

### API additions
- `POST /api/feedback`
- `POST /api/learn`
- `GET /api/progress/<user_id>`
- `POST /api/quiz/generate`
- `POST /api/quiz/submit`

---

## 8) 30-60-90 day execution plan

## Day 0-30 (Foundation)
- Add user accounts and history storage.
- Add feedback/correction APIs.
- Improve inference logging.
- Build admin page to inspect wrong answers.

## Day 31-60 (Learning quality)
- Add RAG with embeddings and citations.
- Add quiz generation and grading.
- Add weak-topic tracking and progress graphs.

## Day 61-90 (Scale + differentiation)
- Add personalization engine.
- Add spaced repetition planner.
- Add teacher dashboard and classroom mode.
- Run A/B experiments on learning outcomes.

---

## 9) Product strategy tips

- Start with one niche (e.g., UPSC, NEET, JEE, CBSE 10th science).
- Win by outcomes, not just chat quality.
- Measure "score improvement" and "hours saved".
- Build community features: group tests, peer challenges, mentor sessions.

---

## 10) Immediate next coding task in this repo

If you want a concrete next commit, implement this first:

1. Add `POST /api/feedback` endpoint that stores:
   - user message
   - AI answer
   - expected answer
   - helpful (true/false)
2. Save feedback in a structured file or SQLite.
3. Add a daily retraining script that merges feedback into training data.
4. Show a simple "confidence" badge in UI response.

This gives you a true self-improving loop and is the fastest path toward a better study AI.