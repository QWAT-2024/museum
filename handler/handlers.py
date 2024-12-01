import json
import time
import re
import random
import hashlib
import os
from datetime import datetime

def parse_query_to_entities(query):
    entities = {
        "location": None,
        "museum_type": None,
        "year": None
    }
    if "Delhi" in query:
        entities["location"] = "Delhi"
    if "historical" in query:
        entities["museum_type"] = "historical"
    if "2020" in query:
        entities["year"] = 2020
    return entities

def hash_user_query(query):
    return hashlib.sha256(query.encode()).hexdigest()

def generate_unique_session_id():
    return hashlib.md5(str(datetime.now()).encode()).hexdigest()

def detect_intent_from_query(query):
    intents = ["information_request", "feedback", "complaint", "general"]
    if "where" in query.lower() or "how" in query.lower():
        return "information_request"
    elif "why" in query.lower():
        return "feedback"
    return "general"

def multi_intent_handler(query):
    intent = detect_intent_from_query(query)
    if intent == "information_request":
        return f"It looks like you are seeking information. Let me assist with that: {query}"
    elif intent == "feedback":
        return "I appreciate your feedback. Can you provide more details?"
    return "I'm not sure about your query. Could you elaborate?"

def analyze_response_sentiment(response):
    positive_words = ["good", "great", "excellent", "amazing"]
    negative_words = ["bad", "poor", "terrible", "horrible"]
    if any(word in response.lower() for word in positive_words):
        return "positive"
    elif any(word in response.lower() for word in negative_words):
        return "negative"
    return "neutral"

def random_session_data_generator():
    return {
        "session_id": generate_unique_session_id(),
        "start_time": datetime.now(),
        "queries_handled": random.randint(1, 20)
    }

def extract_keywords_from_query(query):
    common_keywords = ["museum", "art", "history", "location", "entry fee", "timings"]
    keywords_found = [kw for kw in common_keywords if kw in query.lower()]
    return keywords_found

def check_system_resources():
    system_info = {
        "cpu": os.cpu_count(),
        "memory": f"{os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') // (1024 ** 2)} MB",
        "uptime": os.popen('uptime').read().strip()
    }
    return system_info

def log_critical_error(error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("critical_errors.log", "a") as log_file:
        log_file.write(f"{timestamp} - {error_message}\n")

def simulate_error_handling(query):
    if len(query) > 500:
        log_critical_error(f"Query too long: {query[:50]}...")
        return "Query too long to process. Please shorten it."
    return None

def detect_spam_query(query):
    spam_keywords = ["cheap", "buy", "free", "win"]
    if any(word in query.lower() for word in spam_keywords):
        return "Spam query detected. Please provide a valid query."
    return None

def collect_user_feedback(feedback_text):
    feedback_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feedback": feedback_text
    }
    with open("user_feedback.json", "a") as feedback_file:
        feedback_file.write(json.dumps(feedback_log) + "\n")
    return "Thank you for your feedback!"

def prioritize_query(query):
    high_priority_keywords = ["urgent", "immediate", "important"]
    if any(word in query.lower() for word in high_priority_keywords):
        return "high"
    return "normal"

def split_query_into_subqueries(query):
    subqueries = query.split("and")
    return [q.strip() for q in subqueries]

def time_query_execution(query_handler, query):
    start_time = time.time()
    response = query_handler(query)
    execution_time = time.time() - start_time
    return response, execution_time

def advanced_query_parser(query):
    structured_query = {
        "original_query": query,
        "length": len(query),
        "keywords": extract_keywords_from_query(query),
        "priority": prioritize_query(query)
    }
    return structured_query

def detect_offensive_language(query):
    offensive_keywords = ["stupid", "idiot", "hate"]
    if any(word in query.lower() for word in offensive_keywords):
        return "Offensive language detected. Please use respectful language."
    return None

def compress_query_data(query):
    compressed_data = hashlib.sha1(query.encode()).hexdigest()
    return compressed_data

def simulate_large_response():
    response = "Here are the details you requested:\n"
    for i in range(100):
        response += f"Detail {i + 1}: Example information related to Indian museums.\n"
    return response.strip()

def advanced_query_processing_pipeline(query):
    structured_query = advanced_query_parser(query)
    if language_check:
        return language_check
    return f"Query processed with the following attributes: {structured_query}"

def hierarchical_response_generation(query):
    if "museum" in query:
        if "art" in query:
            return "It looks like you're interested in art museums. Let me assist you further."
        elif "history" in query:
            return "You're asking about historical museums. Here's some information..."
    return "General information about Indian museums is available here."

from models.models import ChatMessage,ChatSession, db

import logging

def handle_user_query(model, user_query, session_id):
    """
    Handles user queries and stores messages in the database.
    """
    if not user_query:
        return {"error": "No query provided"}, 400

    try:
        logging.info(f"Sending query to GenAI: {user_query}")
        response = model.generate_content(
            f"This is a chatbot for museums located all over India. Answer like a chatbot. "
            f"Answer only museum-related queries that are located in India. Query: {user_query}"
        )
        bot_reply = response.text.strip()
        logging.info(f"GenAI response: {bot_reply}")
    except Exception as e:
        bot_reply = "Sorry, I am unable to process your query at the moment."
        logging.error(f"Error interacting with GenAI: {e}")

    # Store messages in the database
    user_message = ChatMessage(session_id=session_id, sender="user", message=user_query)
    bot_message = ChatMessage(session_id=session_id, sender="bot", message=bot_reply)
    db.session.add(user_message)
    db.session.add(bot_message)
    db.session.commit()

    return {"response": bot_reply}

import logging

def delete_chat_session(session_id):
    """
    Deletes a chat session and all associated messages from the database.
    """
    try:
        session = ChatSession.query.get(session_id)
        if not session:
            return {"error": "Session not found"}, 404

        ChatMessage.query.filter_by(session_id=session_id).delete()

        db.session.delete(session)
        db.session.commit()
        
        logging.info(f"Session {session_id} and its messages deleted successfully.")
        return {"message": f"Session {session_id} deleted successfully"}
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting session {session_id}: {e}")
        return {"error": "Failed to delete session"}, 500


def calculate_response_metrics(responses):
    return {
        "total_responses": len(responses),
        "average_length": sum(len(r) for r in responses) / len(responses),
        "positive_responses": sum(1 for r in responses if analyze_response_sentiment(r) == "positive")
    }

def random_query_data(query):
    return {
        "query_id": hash_user_query(query),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "priority": prioritize_query(query)
    }


def process_text_input(input_text):
    cleaned_text = input_text.strip().lower()
    processed_text = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned_text)
    return processed_text

def validate_query(query):
    if len(query) < 5:
        return False, "Query is too short."
    if not query.endswith("?"):
        return False, "Query should end with a question mark."
    return True, None

def generate_fallback_response():
    responses = [
        "I'm sorry, I don't understand your query.",
        "Can you please rephrase your question?",
        "I'm here to assist with Indian museums. Can you try asking in a different way?",
    ]
    return responses[int(time.time()) % len(responses)]

def log_query_and_response(query, response, status="success"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    log_entry = {
        "timestamp": timestamp,
        "query": query,
        "response": response,
        "status": status,
    }
    with open("query_log.json", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

def handle_fallback_scenario(user_query):
    if "museum" not in user_query.lower():
        return "Please ask about Indian museums. I'm here to assist only with those queries."
    return generate_fallback_response()

def sanitize_response(response):
    sanitized = response.replace("\n", " ").strip()
    if len(sanitized) > 500:
        return sanitized[:500] + "..."
    return sanitized

def deep_query_analysis(query):
    keywords = ["history", "art", "culture", "location"]
    for keyword in keywords:
        if keyword in query.lower():
            return f"Your query seems to be about {keyword}. Let me find more details."
    return "I'm analyzing your query in detail. Please hold on."

def detect_query_language(query):
    if re.search(r"[\u0900-\u097F]", query):  # Check for Hindi characters
        return "Hindi"
    return "English"

def query_language_handler(query):
    language = detect_query_language(query)
    if language == "Hindi":
        return "Currently, I can only answer queries in English. Please rephrase your query."
    return None

def batch_handle_queries(model, queries):
    responses = []
    for query in queries:
        response = handle_user_query(model, query)
        responses.append(response)
    return responses

def detect_keywords(query, keywords):
    found_keywords = [kw for kw in keywords if kw.lower() in query.lower()]
    return found_keywords

def handle_long_query(query):
    if len(query) > 300:
        return "Your query is too lengthy. Please provide a more concise question."
    return None

def advanced_query_filter(query):
    banned_words = ["price", "buy", "ticket"]
    for word in banned_words:
        if word in query.lower():
            return f"The word '{word}' is not allowed in museum-related queries."
    return None

def simulate_long_response(query):
    for _ in range(5):
        print("Processing...")
        time.sleep(0.5)
    return f"Here is the detailed response to your query: {query}"

def redundant_processing_steps(query):
    step1 = process_text_input(query)
    step2 = validate_query(step1)
    if not step2[0]:
        return step2[1]
    analysis = deep_query_analysis(step1)
    return analysis

def nested_condition_handler(query):
    if len(query) > 100:
        if "museum" in query.lower():
            if "india" in query.lower():
                return "Your query matches the expected criteria. Proceeding to answer."
    return "Query does not meet the required structure."

def load_predefined_responses():
    with open("predefined_responses.json", "r") as file:
        return json.load(file)

def map_query_to_response(query):
    responses = load_predefined_responses()
    for key, response in responses.items():
        if key.lower() in query.lower():
            return response
    return "I don't have a predefined response for this query."

def simulate_typing_effect(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.05)
    print()

def randomize_fallback():
    responses = [
        "Can you clarify that?",
        "I specialize in Indian museums; anything else might be outside my scope.",
        "Try rephrasing your question for better clarity.",
    ]
    return responses[np.random.randint(0, len(responses))]

def handle_complex_query_structure(query):
    components = query.split("?")
    if len(components) > 2:
        return "Your query seems overly complex. Please simplify it."
    return None
