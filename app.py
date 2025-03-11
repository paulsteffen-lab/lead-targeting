import chainlit as cl
import pandas as pd
from src.config import settings
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer(settings.model_name)
collection_name = f"linkedin_profiles_{settings.model_name.split('/')[-1]}_{model.get_sentence_embedding_dimension()}"
client = QdrantClient(path=settings.vector_db_path)

DISPLAYED_INFO: list[str] = [
    "id",
    "full_name",
    "location",
    "workplace",
    "experiences",
    "educations",
    "about",
]


@cl.step(type="tool")
async def encode_message(message: str):
    """
    This function encodes the input message into a vector.

    Args:
        message: The input message.

    Returns:
        The encoded vector.
    """
    return model.encode(message.content)


@cl.step(type="tool")
async def retrieval(query_embedding, top_k: int = 5) -> list:
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_embedding.tolist(),
        limit=top_k,
    )
    return search_result


def _format_result(search_result: list) -> str:
    """
    Formats a list of search results into a markdown table.

    This function takes a list of search results, each containing a payload and a score,
    and formats them into a markdown table string. The table includes specific fields
    defined in DISPLAYED_INFO along with the score for each result.

    Args:
        search_result (list): A list of search result objects, each with a payload and score.

    Returns:
        str: A markdown-formatted string representing the search results as a table.
    """
    table_md = pd.DataFrame(
        [result.payload | {"score": result.score} for result in search_result]
    )[DISPLAYED_INFO + ["score"]].to_markdown(index=False)
    return f"```markdown\n{table_md}\n```"


@cl.on_message
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """

    query_embedding = await encode_message(message)

    search_result = await retrieval(query_embedding)

    content = _format_result(search_result)

    await cl.Message(content=content).send()
