from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# 🔥 Expanded training data with multiple questions and answers
questions = [
    # Greetings
    "hi", "hello", "hey", "good morning", "good evening",
    "how are you", "how do you do", "what's up",

    # Basic Info
    "what is your name", "who are you", "what are you",
    "what can you do", "help me", "what is vedastra",

    # India Facts
    "capital of india", "india capital", "what is capital", "tell me capital of india",
    "prime minister of india", "pm of india", "who is pm", "india pm", "who is prime minister",
    "first pm of india", "first prime minister of india", "who was the first prime minister of india", "who was the first pm of india",
    "father of nation", "father of india", "who is father of nation",
    "president of india", "who is president", "india president",

    # Math
    "2+2", "calculate 2+2", "what is 2+2", "solve 2+2",
    "5*5", "what is 5 times 5", "calculate 5*5",

    # Environment & Ecology (based on PDF topic)
    "what is environment", "define environment", "what is environmental science",
    "what is ecology", "define ecology", "what is ecological system",
    "what is pollution", "types of pollution", "what are pollutants",
    "what is air pollution", "causes of air pollution", "effects of air pollution",
    "what is water pollution", "causes of water pollution", "effects of water pollution",
    "what is soil pollution", "causes of soil pollution", "effects of soil pollution",
    "what is climate change", "what causes climate change", "effects of climate change",
    "what is global warming", "causes of global warming", "effects of global warming",
    "what is biodiversity", "importance of biodiversity", "what is biodiversity loss",
    "what is deforestation", "causes of deforestation", "effects of deforestation",
    "what is sustainable development", "what is green energy", "renewable energy sources",
    "what is ozone layer", "what is ozone depletion", "causes of ozone depletion",
    "what is acid rain", "causes of acid rain", "effects of acid rain",
    "what is greenhouse effect", "what are greenhouse gases", "examples of greenhouse gases",
    "what is carbon footprint", "how to reduce carbon footprint",
    "what is environmental impact assessment", "what is eia",
    "what is wildlife conservation", "importance of wildlife",
    "what is national park", "what is biosphere reserve", "what is wildlife sanctuary",

    # More variations
    "explain environment", "tell me about ecology", "what do you know about pollution",
    "how to prevent pollution", "what is environmental protection",
    "what is natural resources", "types of natural resources",
    "what is renewable resources", "what is non-renewable resources",
    "what is forest conservation", "what is water conservation",
    "what is energy conservation", "what is waste management",
    "what is recycling", "importance of recycling",
    "what is composting", "what is biodegradable waste",
    "what is non-biodegradable waste", "what is e-waste",
    "what is plastic pollution", "effects of plastic pollution",
    "what is marine pollution", "what is coral bleaching",
    "what is endangered species", "what is extinct species",
    "what is conservation biology", "what is ecosystem services",
    "what is food chain", "what is food web", "what is trophic level",
    "what is photosynthesis", "what is respiration in plants",
    "what is carbon cycle", "what is nitrogen cycle", "what is water cycle",
    "what is population ecology", "what is community ecology",
    "what is biome", "types of biomes", "what is desert biome",
    "what is forest biome", "what is grassland biome", "what is aquatic biome",
]

answers = [
    # Greetings (5 answers)
    "Hello 👋", "Hello 👋", "Hello 👋", "Good morning! 🌅", "Good evening! 🌙",
    "I am fine 😊", "I am doing well, thank you!", "All good here!",

    # Basic Info (5 answers)
    "I am Vedastra AI 🤖", "I am Vedastra AI 🤖", "I am Vedastra AI 🤖", "I am Vedastra AI 🤖", "I am Vedastra AI 🤖",

    # India Facts
    "New Delhi", "New Delhi", "New Delhi", "New Delhi",
    "Narendra Modi", "Narendra Modi", "Narendra Modi", "Narendra Modi", "Narendra Modi",
    "Jawaharlal Nehru", "Jawaharlal Nehru", "Jawaharlal Nehru", "Jawaharlal Nehru",
    "Mahatma Gandhi", "Mahatma Gandhi", "Mahatma Gandhi",
    "Droupadi Murmu", "Droupadi Murmu", "Droupadi Murmu",

    # Math (7 answers)
    "4", "4", "4", "4",
    "25", "25", "25",

    # Environment & Ecology (many answers)
    "Environment refers to the surroundings in which organisms live, including air, water, land, and living organisms.",
    "Environment refers to the surroundings in which organisms live, including air, water, land, and living organisms.",
    "Environment refers to the surroundings in which organisms live, including air, water, land, and living organisms.",
    "Ecology is the study of relationships between organisms and their environment.",
    "Ecology is the study of relationships between organisms and their environment.",
    "Ecology is the study of relationships between organisms and their environment.",
    "Pollution is the introduction of harmful substances into the environment.",
    "Types of pollution include air, water, soil, noise, and light pollution.",
    "Types of pollution include air, water, soil, noise, and light pollution.",
    "Air pollution is the contamination of air by harmful gases, dust, and smoke.",
    "Causes include vehicle emissions, industrial activities, and burning of fossil fuels.",
    "Effects include respiratory problems, climate change, and acid rain.",
    "Water pollution is the contamination of water bodies by harmful substances.",
    "Causes include industrial waste, sewage, and agricultural runoff.",
    "Effects include waterborne diseases and death of aquatic life.",
    "Soil pollution is the contamination of soil by harmful chemicals and waste.",
    "Causes include pesticides, industrial waste, and improper disposal of garbage.",
    "Effects include reduced soil fertility and health problems.",
    "Climate change is the long-term change in temperature and weather patterns.",
    "Causes include greenhouse gas emissions and deforestation.",
    "Effects include rising sea levels, extreme weather, and biodiversity loss.",
    "Global warming is the increase in Earth's average temperature due to greenhouse gases.",
    "Causes include burning of fossil fuels and deforestation.",
    "Effects include melting ice caps and rising sea levels.",
    "Biodiversity is the variety of life on Earth, including plants, animals, and microorganisms.",
    "It provides ecosystem services, food, medicine, and maintains ecological balance.",
    "Biodiversity loss occurs due to habitat destruction, pollution, and climate change.",
    "Deforestation is the large-scale removal of forests.",
    "Causes include agriculture, logging, and urbanization.",
    "Effects include soil erosion, climate change, and loss of biodiversity.",
    "Sustainable development meets present needs without compromising future generations.",
    "Green energy comes from renewable sources like solar, wind, and hydro power.",
    "Sources include solar, wind, hydro, geothermal, and biomass energy.",
    "Ozone layer is a protective layer in the stratosphere that absorbs UV radiation.",
    "Ozone depletion is the thinning of the ozone layer due to CFCs and other chemicals.",
    "Causes include chlorofluorocarbons (CFCs) and halons.",
    "Acid rain is rain with high acidity due to sulfur and nitrogen oxides.",
    "Causes include fossil fuel combustion and industrial emissions.",
    "Effects include damage to forests, lakes, and buildings.",
    "Greenhouse effect is the trapping of heat by greenhouse gases in the atmosphere.",
    "Greenhouse gases include CO2, methane, and water vapor.",
    "Examples include carbon dioxide, methane, nitrous oxide, and fluorinated gases.",
    "Carbon footprint is the total greenhouse gas emissions caused by an individual or organization.",
    "Ways include using renewable energy, reducing waste, and sustainable transportation.",
    "EIA assesses the environmental impact of proposed projects.",
    "EIA assesses the environmental impact of proposed projects.",
    "Wildlife conservation protects endangered species and habitats.",
    "It maintains ecological balance and provides economic benefits.",
    "A national park is a protected area for conservation of wildlife and natural beauty.",
    "A biosphere reserve is an area for conservation of biodiversity and sustainable development.",
    "A wildlife sanctuary is a protected area for wildlife conservation.",

    # More variations
    "Environment refers to the surroundings in which organisms live, including air, water, land, and living organisms.",
    "Ecology is the study of relationships between organisms and their environment.",
    "Pollution is the introduction of harmful substances into the environment.",
    "Prevent pollution by reducing waste, using clean energy, and proper disposal.",
    "Environmental protection involves conservation and sustainable use of resources.",
    "Natural resources are materials from nature used for economic purposes.",
    "Types include renewable (solar, wind) and non-renewable (coal, oil).",
    "Renewable resources can be replenished naturally, like solar and wind energy.",
    "Non-renewable resources cannot be replenished, like fossil fuels.",
    "Forest conservation protects forests from degradation and deforestation.",
    "Water conservation involves efficient use and protection of water resources.",
    "Energy conservation reduces energy consumption through efficient practices.",
    "Waste management involves collection, disposal, and recycling of waste.",
    "Recycling converts waste materials into reusable products.",
    "Recycling reduces waste, conserves resources, and reduces pollution.",
    "Composting is the decomposition of organic waste into nutrient-rich soil.",
    "Biodegradable waste can be broken down by microorganisms.",
    "Non-biodegradable waste does not decompose naturally.",
    "E-waste is electronic waste from discarded electronic devices.",
    "Plastic pollution is the accumulation of plastic waste in the environment.",
    "Effects include harm to wildlife, ocean pollution, and microplastics.",
    "Marine pollution is the contamination of oceans by pollutants.",
    "Coral bleaching is the loss of color in corals due to stress from pollution and warming.",
    "Endangered species are at risk of extinction.",
    "Extinct species have completely disappeared.",
    "Conservation biology studies biodiversity conservation and management.",
    "Ecosystem services are benefits humans get from ecosystems.",
    "Food chain shows how energy flows from producers to consumers.",
    "Food web is a network of interconnected food chains.",
    "Trophic level is the position in the food chain.",
    "Photosynthesis is the process by which plants make food using sunlight.",
    "Respiration in plants is the process of releasing energy from food.",
    "Carbon cycle is the movement of carbon through Earth's systems.",
    "Nitrogen cycle is the movement of nitrogen through ecosystems.",
    "Water cycle is the continuous movement of water on Earth.",
    "Population ecology studies populations of organisms.",
    "Community ecology studies interactions between species in a community.",
    "Biome is a large ecological area with distinct climate and vegetation.",
    "Types include forest, desert, grassland, tundra, and aquatic.",
    "Desert biome has low rainfall and extreme temperatures.",
    "Forest biome has dense tree cover and high biodiversity.",
    "Grassland biome has grasses and few trees, like prairies.",
    "Aquatic biome includes oceans, lakes, and rivers.",
    "Aquatic biomes include oceans, lakes, rivers, and wetlands.",
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