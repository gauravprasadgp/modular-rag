from FlagEmbedding import FlagReranker

reranker = FlagReranker('BAAI/bge-reranker-large', use_fp16=True)


def rerank_documents(question: str, documents: list[str]):
    sentences = []
    for doc in documents:
        sentences.append((question, doc))
    score = reranker.compute_score(sentences)
    print(score)
    sorted_elements = []
    for score, doc in zip(score, documents):
        elem = {score: score, doc: doc}
        sorted_elements.append(elem)
    sorted_docs = sorted(sorted_elements, key=lambda x: x.score, reverse=True)
    return sorted_docs[:7]
