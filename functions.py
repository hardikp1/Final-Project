import time
from config import BING_API_KEY
import uuid
import openai
import requests
import numpy as np
from bs4 import BeautifulSoup
from typing import List

""" 
Breakdown of pipeline:
1. User provides input text.
2. generate_questions(input_text) -> [question1, question2, ..., questionN]
3. for each question in [question1, question2, ..., questionN]:
     4. bing_search(question) -> [result1, result2, ..., resultM]
        5. for each result in [result1, result2, ..., resultM]:
            6. Extract and clean text from the web page.
7. summarize(original_question, [cleaned_text1, cleaned_text2, ..., cleaned_textM]) -> summary
8. Display or use the summary in your application.
"""


def bing_search(query, top_n=3):
    # This function takes as input a query and
    # return a list containing Bing search results (top n) for the query.
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    return_list = []
    response = requests.get(
        "https://api.bing.microsoft.com/v7.0/search",
        headers=headers,
        params={"q": query, "textDecorations": True, "textFormat": "HTML"},
    )
    response.raise_for_status()
    search_results = response.json()
    # Fetch the web document content for each relevant URL
    for result in search_results["webPages"]["value"]:
        result_response = requests.get(result["url"])
        try:
            soup = BeautifulSoup(result_response.content, "html.parser")
            text = soup.find("body").get_text()
            clean_text = ""
            for line in text.split("\n"):
                clean_line = line.strip()
                if len(clean_line.split(" ")) > 3:
                    clean_text += f"{clean_line}\n"
        except AttributeError as e:
            print(f'[INFO] Skipped one URL [{result["url"]}] with error {e}.')
            continue
        return_list.append([result["url"], clean_text])
        if len(return_list) >= top_n:
            break
    return return_list


def generate_questions(input_text: str, provider="openai"):
    # This function calls OpenAI APIs to generate a list of questions
    # based on the input text given by the user.
    messages = [
        {
            "role": "system",
            "content": "You are an informative and helpful assistant designed to assist users in the lateral reading task."
            "Your goal is to analyze a given segment of text (labeled as Text:) and generate three thought-provoking questions."
            "These questions should be important, insightful, diverse, and fact-based. Ensure that the questions are not explicitly"
            "answered in the provided text. Label your questions as Question1:, Question2:, and Question3:. Craft each question to"
            "be a meaningful query, using explicit entities that are fully resolved and not dependent on the provided text."
            "Imagine these questions as prompts for a search engine like Bing. Your objective is to prompt users to search for "
            "relevant documents, aiding them in determining whether the given text may contain misinformation.",
        },
        {
            "role": "user",
            "content": f"Text: {input_text}\n------\nCarefully choose insightful and atomic lateral "
            f"reading questions not answered by the above text, ensuring that the queries are "
            f"self-sufficient (Do not have pronouns or attributes relying on the text, "
            f"they should be fully resolved and make complete sense independently).",
        },
    
    ]
    if provider == "openai":
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
            max_tokens = 3854
        )
    else:
        raise Exception(f"[ERROR] Unidentified ChatGPT Provider: {provider}")
    response = completion["choices"][0]["message"]["content"]
    responses = [line for line in response.split("\n") if line.strip() != ""]
    questions = []
    for ind, line in enumerate(responses):
        question = line.strip()
        questions.append(question.removeprefix(f"Question{ind + 1}:").strip())
    return questions


def summarize(question: str, documents: List[str], provider="openai"):
    # This function takes as input a pair of question and document to produce
    # a short summary to answer the question using the information in the document.

    # Use embeddings to find relevant chunks.
    concatenated_input = ""
    for doc_id, document in enumerate(documents):
        concatenated_input += f"Document {doc_id + 1}:\n{document[:40000]}"

    # Define conversation messages for OpenAI API
    messages = [
        {
            "role": "system", 
            "content": "You are a factual and helpful assistant tasked with cohesively summarizing segments from various relevant "
            "documents to address a specific question. Craft your answer to be informative, yet concise, limiting it to 100 words." 
            "Ensure clarity and coherence by using information solely from the provided segments, combining search results into a cohesive response."
            "Avoid redundancy and irrelevant details. Maintain an unbiased and journalistic tone throughout your summary. Present your output in plaintext format."
            "Each sentence should be properly attributed with citations, using the [${doc_number}] notation" 
            "(e.g., 'Recent advancements in renewable energy technologies show promise for sustainable urban development [2][4]')." 
            "Remember to cite each document at least once. If different results refer to entities with the same name, cite them separately."

        },
        {
            "role": "user",
            "content": f'My question is "{question}" Cohesively and factually summarize the following documents to '
            f"answer my question.\n------\n{concatenated_input}",
        },
    ]

    # Ask ChatGPT to summarize the extracted chunks.
    retry_count = 0
    while retry_count < 3:
        try:
            if provider == "openai":
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.2,
                )

        except Exception as e:
            print(f"[INFO] Exception: {e}. Retry in five seconds.")
            time.sleep(10)
            retry_count += 1
            continue
        break

    if retry_count < 3:
        return completion["choices"][0]["message"]["content"]
    else:
        return ""


def run_temporary():
    input_text = "COVID-19 originated in the United States of America."

    # Step 1: Generate questions
    generated_questions = generate_questions(input_text, provider="openai")

    # Step 2: Use questions as queries for Bing search
    for question in generated_questions:
        search_results = bing_search(question, top_n=3)

        # Step 3: Summarize the content of each search result
        for result in search_results:
            url, clean_text = result
            summary = summarize(question, [clean_text], provider="openai")

            # Display or use the summary in your application
            print(f"Question: {question}")
            print(f"URL: {url}")
            print(f"Summary: {summary}\n")


if __name__ == "__main__":
    run_temporary()
