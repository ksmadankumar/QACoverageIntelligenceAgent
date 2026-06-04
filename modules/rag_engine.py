import chromadb

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

    try:
        client.delete_collection(
            "requirements"
        )
    except:
        pass

    global collection

    collection = (
        client.get_or_create_collection(
            name="requirements"
        )
    )


def index_requirements(
    requirements_text
):

    clear_collection()

    chunk_size = 1000

    chunks = []

    for i in range(
        0,
        len(requirements_text),
        chunk_size
    ):

        chunks.append(
            requirements_text[
                i:i + chunk_size
            ]
        )

    for idx, chunk in enumerate(
        chunks
    ):

        collection.add(
            ids=[str(idx)],
            documents=[chunk],
            embeddings=[
                generate_embedding(
                    chunk
                )
            ]
        )

    return len(chunks)


def retrieve_context(
    query,
    top_k=3
):

    result = collection.query(
        query_embeddings=[
            generate_embedding(
                str(query)
            )
        ],
        n_results=top_k
    )

    docs = result["documents"][0]

    return "\n".join(docs)