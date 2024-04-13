
# Modular RAG

A hybrid approach to implement RAG inspired by Advance RAG.
Usually implemeted with modules acting as plug and play.

## Documentation

#### Generator: 
Core component of RAG, responsible for transforming the retrieved information into natural and human sense.

#### Retriever: 
The word "R" in RAG, serving the purpose of retrieving the top K element from knowledge base.

#### ReRank: 
As the name suggest a model used to re-rank the relevant documents. It indexes the documents based on the similariy score between question and the retrieved documents post vector search.

## Run Locally

Clone the project

```bash
  git clone https://github.com/gauravprasadgp/modular-rag
```

Go to the project directory

```bash
  cd modular-rag
```

Install dependencies

```bash
pip install -r requirements.txt
```
Run postgres locally
```bash
cd pgvector
```
```bash
docker compose -d up
```

Start the server

```bash
  python main.py
```

## API Reference

#### Upload file to create embedding

```http
  POST /create
```

| Parameter | Type   | Description                  |
|:----------|:-------|:-----------------------------|
| `file`    | `file` | **Required**. File to upload |

#### Get answer from user query

```http
  POST /answer
```

| Parameter | Type     | Description              |
|:----------| :------- |:-------------------------|
| `query`   | `string` | **Required**. user query |



## License

[MIT](https://choosealicense.com/licenses/mit/)