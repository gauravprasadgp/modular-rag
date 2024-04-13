import datetime
import json

from fastapi import File
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.schema import BaseNode

from generator.llm_calls import get_embed_model
from utils.db import postgres_db


async def create_embeddings_from_file(file: File()):
    documents = await SimpleDirectoryReader(input_files=[file]).aload_data()
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text",
    )

    nodes = node_parser.get_nodes_from_documents(documents)
    for node in nodes:
        embedding = await get_embed_model().aget_text_embedding(node.get_content())
        node.embedding = embedding


def get_values_from_nodes(nodes: list[BaseNode]):
    values = []
    dt = datetime.datetime.now()
    for node in nodes:
        value = (node.embedding, node.get_content(), json.dumps(node.metadata), dt)
        values.append(value)
    return values


async def insert_documents(nodes):
    try:
        values = get_values_from_nodes(nodes)
        async with postgres_db.db_pool as conn:
            async with conn.cursor() as cur:
                await cur.executemany("""
                        INSERT INTO document_embedding (embedding, document, metadata, created_at)
                        VALUES (%s, %s, %s, %s); 
                    """, values)
                await conn.commit()
    except Exception as error:
        print(f"insert document exception {error}")
        await conn.rollback()


async def get_relevant_document(query: str):
    embedded_question = await get_embed_model().aget_query_embedding(query=query)
    try:
        async with postgres_db.db_pool as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT metadata -> 'window', 1 - (embedding <=> '{embedded_question}') AS 
                cosine_similarity from document_embedding ORDER BY cosine_similarity DESC limit 10;""")
                results = await cur.fetchall()
                docs = [row[0] for row in results]
                return docs
    except Exception as error:
        print(f"insert document exception {error}")
        await conn.rollback()
