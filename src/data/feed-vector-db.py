from loguru import logger
from pathlib import Path
from sqlmodel import create_engine, select, Session
from src.data.models import LinkedinProfile
from src.config import settings

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

engine = create_engine(settings.structured_db_url, echo=True)
model = SentenceTransformer(settings.model_name)

vector_size = model.get_sentence_embedding_dimension()
collection_name = f"linkedin_profiles_{settings.model_name}_{vector_size}"


def get_profiles(engine) -> list[LinkedinProfile]:
    """
    Retrieve all LinkedinProfile records from the database.

    Args:
        engine: The database engine used to establish a session.

    Returns:
        A list of LinkedinProfile objects representing all profiles in the database.
    """
    with Session(engine) as session:
        profiles = session.exec(select(LinkedinProfile)).all()
    return profiles


def create_db_and_collections(
    db_path: Path, collection_name: str, vector_size: int, distance: Distance
) -> QdrantClient:
    """
    Create a Qdrant database client and create a collection with specified parameters if needed.

    Args:
        db_path (Path): The path to the database.
        collection_name (str): The name of the collection to be recreated.
        vector_size (int): The size of the vectors in the collection.
        distance (Distance): The distance metric to be used for the vectors.

    Returns:
        QdrantClient: An instance of the Qdrant client connected to the specified database.
    """
    client = QdrantClient(path=settings.vector_db_path)
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )
    return client


def feed_collection(
    client: QdrantClient,
    collection_name: str,
    profiles: list[LinkedinProfile],
    embeddings: list[list[float]],
) -> None:
    """
    Feeds a collection in Qdrant with profile data and corresponding embeddings.

    This function takes a list of LinkedinProfile instances and their corresponding
    embeddings, constructs PointStruct objects, and upserts them into a specified
    collection in Qdrant.

    Args:
        client (QdrantClient): The Qdrant client used to interact with the database.
        collection_name (str): The name of the collection to upsert the points into.
        profiles (list[LinkedinProfile]): A list of LinkedinProfile instances containing
            the profile data to be stored.
        embeddings (list[list[float]]): A list of embeddings corresponding to each profile.

    Returns:
        None
    """
    points = [
        PointStruct(id=str(profile.id), vector=embedding, payload=profile.model_dump())
        for profile, embedding in zip(profiles, embeddings)
    ]

    client.upsert(collection_name=collection_name, points=points)


def main() -> None:
    """
    Main function to initialize the database, retrieve profiles, compute embeddings,
    and store them in a Qdrant collection.

    This function orchestrates the process of setting up a Qdrant client,
    retrieving LinkedinProfile records, computing their embeddings using a model,
    and feeding the data into a specified Qdrant collection.

    Returns:
        None
    """
    client = create_db_and_collections(
        settings.vector_db_path, collection_name, vector_size, Distance.COSINE
    )

    profiles = get_profiles(engine)

    logger.info(f"Computing profile embeddings using {settings.model_name} ...")
    embeddings = model.encode([str(profile) for profile in profiles])

    feed_collection(client, collection_name, profiles, embeddings)

    logger.success("Vectors stored successfully !")


if __name__ == "__main__":
    main()
