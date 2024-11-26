import os

from openai import OpenAI

from model.db import DB
from model.preprocessing import Preprocessing


class Gpt(object):
    def __init__(self, db: DB, preprocessor: Preprocessing):
        self.__client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )
        self.__db = db
        self.__preprocessor = preprocessor

    def build_prompt(self, question, previousConversation, article) -> list[str]:
        retrieved_data = previousConversation + article
        messages = [
            {"role": "system",
             "content": "I want you to act as a question-answering bot that uses the provided articles, answers concisely, and do not make stuff up. "
                        "You will answer psoriasis-related questions based on the articles. "
                        "Future questions will be related to these articles. "
                        "Please focus on these articles for any subsequent inquiries and refrain from generating responses outside these specified articles. "
                        "Answer concisely and do not make stuff up. "
                        "{0}"

             },
            {"role": "user", "content": "Answer this question: {0} and tell me what articles are used to provide the answer."},
        ]

        messages[0]['content'] = messages[0]['content'].format(retrieved_data)
        messages[1]['content'] = messages[1]['content'].format(question)
        return messages

    def retrieve_output(self, messages) -> str:
        """
        Calling the ChatGPT API to retrieve response.

        :param messages:
        :return:
        """
        chat_completion = self.__client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            timeout=440, max_tokens=2000, n=1, stop=None, temperature=0.5
        )
        print(chat_completion)
        return chat_completion.choices[0].message.content

    def build_context_from_previous_conversation(self, user) -> str:
        """
        Providing additional messages as parameters to text generation request.

        messages: [
            {
                "role": "user",
                "content": [{ "type": "text", "text": "knock knock." }]
            },
            {
                "role": "assistant",
                "content": [{ "type": "text", "text": "Who's there?" }]
            },
            {
                "role": "user",
                "content": [{ "type": "text", "text": "Orange." }]
            }
        ]

        :return:
        """
        return ""

    def build_context_from_article(self, limit=50) -> str:
        """
        Loading article context from database.

        :param db:
        :return:
        """
        # @todo CHANGE THIS - use vector database
        query = "SELECT \"Abstract\", \"ArticleTitle\" FROM Articles WHERE \"Abstract\" IS NOT NULL and \"Subject\" ILIKE '%psoriasis%'limit {0}".format(
            limit)

        data = self.__db.cursor(query)
        summary = "Each article presented below has an Article Title and abstract. It is delimited by three `. Articles: "

        for row in data:
            title = self.__preprocessor.clean_text(row["ArticleTitle"])
            article_abstract = self.__preprocessor.clean_text(row["Abstract"])
            summary += f"Article Title: {title}. "
            summary += f"Abstract: {article_abstract}. ```"
        return summary
