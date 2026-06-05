import chromadb
import re

from modules.embeddings import (
    generate_embedding
)

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="requirements"
)


def clear_collection():

    global collection

    try:
        client.delete_collection(
            "requirements"
        )
    except Exception:
        pass

    collection = (
        client.get_or_create_collection(
            name="requirements"
        )
    )


def split_requirements(
    requirements_text,
    chunk_size=800
):

    text = re.sub(
        r"\n\s*\n",
        "\n",
        requirements_text
    )

    paragraphs = text.split("\n")

    chunks = []

    current_chunk = ""

    for para in paragraphs:

        if (
            len(current_chunk)
            + len(para)
            < chunk_size
        ):

            current_chunk += (
                para + "\n"
            )

        else:

            chunks.append(
                current_chunk.strip()
            )

            current_chunk = (
                para + "\n"
            )

    if current_chunk.strip():

        chunks.append(
            current_chunk.strip()
        )

    return chunks


def index_requirements(
    requirements_text
):

    clear_collection()

    chunks = split_requirements(
        requirements_text
    )

    for idx, chunk in enumerate(
        chunks
    ):

        embedding = (
            generate_embedding(
                chunk
            )
        )

        collection.add(
            ids=[
                str(idx)
            ],
            documents=[
                chunk
            ],
            embeddings=[
                embedding
            ],
            metadatas=[
                {
                    "chunk_id": idx
                }
            ]
        )

    return len(chunks)


def retrieve_context(
    query,
    top_k=5
):

    embedding = (
        generate_embedding(
            str(query)
        )
    )

    results = (
        collection.query(
            query_embeddings=[
                embedding
            ],
            n_results=top_k
        )
    )

    docs = (
        results["documents"][0]
        if results["documents"]
        else []
    )

    return "\n\n".join(
        docs
    )


def retrieve_matches(
    query,
    top_k=5
):

    embedding = (
        generate_embedding(
            str(query)
        )
    )

    results = (
        collection.query(
            query_embeddings=[
                embedding
            ],
            n_results=top_k
        )
    )

    documents = (
        results["documents"][0]
        if results["documents"]
        else []
    )

    distances = (
        results["distances"][0]
        if "distances" in results
        else []
    )

    output = []

    for doc, distance in zip(
        documents,
        distances
    ):

        similarity = round(
            (1 - distance) * 100,
            2
        )

        output.append(
            {
                "requirement": doc,
                "similarity": similarity
            }
        )

    return output