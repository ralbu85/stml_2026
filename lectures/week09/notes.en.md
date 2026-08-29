# Chapter 8. Retrieval-Augmented Generation

Some material never appears in a model's training data: a lab's internal documents, the papers of this course, a file updated yesterday. A model's knowledge is exactly what was stored in its parameters during training, so questions about such material cannot be answered from the model alone. The agent of Chapter 4 is in the same position, because its search tool reaches only Wikipedia — a store that someone else has already made searchable. Answering requires making our own documents searchable: building a store from the documents and, for each question, selecting the relevant parts into the prompt. That construction is RAG, and the construction that delegates the retrieval decisions to the agent is agentic RAG.

## 8.1 The Problem — Knowledge Confined to Parameters

Knowledge stored in the weights is called **parametric knowledge**. Parametric knowledge contains no facts from after training, and no private material that was absent from the training data; the boundary of training is called the **knowledge cutoff**. The model also cannot mark what it does not contain. This last deficiency makes the first two dangerous: prediction does not stop for lack of a stored fact but produces the most plausible next token anyway (→ 2.2), so asked for this course's week-8 presentation paper, the model invents a plausible paper title instead of answering that it does not know.

There are two routes for supplying knowledge. The first is to put it into the weights — fine-tuning on the documents. This route requires retraining whenever the documents change, is expensive, and cannot point to the source of an answer. The second is to put it into the input. Text placed in the prompt conditions the next generation (in-context learning → 2.3), so a document placed in the prompt is read and used. There is no retraining, a replaced document takes effect immediately, and the answer can cite the passage it rests on.

The problem with the input route is capacity. The entire document pile cannot be placed in the prompt for every question: input length has a ceiling, input tokens are billed, and injecting more text has been measured to make answers worse (→ Ch. 9). Only the parts relevant to the question should therefore be selected, and the act of selecting is retrieval. The construction that retrieves question-relevant document fragments from an external store, attaches them to the prompt, and generates is called **RAG (retrieval-augmented generation)** (Lewis et al., 2020). The original paper named a model architecture that trains retriever and generator jointly; the name has since widened to any construction that composes retrieval and generation without training. The correspondence to the original is examined in the presentation.

## 8.2 Judging Relevance — Embeddings and Cosine Similarity

The central problem of retrieval is the judgment of "relevant." The naive judgment is string matching: find the fragments that contain the question's words. This judgment fails whenever the wording differs. The question "the part about models cheating the reward" and the document passage "reward hacking is the phenomenon of optimizing an unstated objective" share not a single content word, yet they are about the same thing. What is needed is a comparison of meaning, not of wording.

An **embedding** is a function that maps text to a fixed-dimension real vector, trained so that texts closer in meaning become closer vectors. The model that computes embeddings is separate from the generative LLM and usually far smaller. Closeness between vectors is measured by cosine similarity:

$$\text{sim}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\lVert \mathbf{u} \rVert \, \lVert \mathbf{v} \rVert}$$

This is the cosine of the angle between the two vectors — the dot product divided by the two lengths. It approaches 1 as the directions align and 0 as they become unrelated. Because length is divided out, what is compared is the direction of the content, not the amount of text. On this measure, retrieval is sorting: order the fragments by cosine similarity to the question vector and take the top k.

The property that embeddings translate closeness of meaning into closeness of vectors comes from the training objective. **Contrastive learning** trains the vectors of related pairs (a question and a passage containing its answer, adjacent sentences of one document) to be close and the vectors of unrelated pairs to be far. A retrieval embedding model is an encoder trained with this objective, and it vectorizes questions and documents independently of each other. This structure is called a bi-encoder. Document vectors are precomputed at indexing time and only one question vector is computed per query, which makes it fast; but because question and document are each compressed without seeing the other, precise mutual comparison is beyond it. That limit is compensated by re-ranking, which re-scores candidates (→ 8.5).

Two practical details. Storing vectors normalized to unit length makes cosine similarity equal the dot product, simplifying computation. And once chunks number in the hundreds of thousands, exhaustive comparison of the question against every chunk gives way to an approximate nearest-neighbor index (ANN; HNSW and peers) — a trade of a little recall for logarithmic search time.

## 8.3 The Pipeline — Indexing and Query

The RAG procedure divides into an indexing stage that prepares documents and a query stage that handles questions. Indexing runs once when documents arrive; the query stage runs per question. The implementation of this procedure is the subject of the Week 9 lab.

Indexing:

1. **Chunking** — cut documents into retrieval-unit fragments (chunks). The cutting criterion is treated in 8.4. Output: a list of chunks.
2. **Embedding** — convert each chunk to a vector.
3. **Storage** — store the (chunk, vector) pairs in an index.

Query:

4. **Question embedding** — convert the question to a vector with the same embedding function used for indexing. A different function would place it in a different coordinate system, making similarity meaningless.
5. **Retrieval** — compute cosine similarity between the question vector and the chunk vectors; take the top-k chunks.
6. **Assembly** — attach the selected chunks to the prompt as evidence, with the instruction to answer from the evidence.
7. **Generation** — the model reads the evidence and generates the answer.

> **[Figure 8.1]** A two-lane pipeline sharing one index. The upper indexing lane (documents → chunking → embedding → index storage) runs once when documents arrive; the lower query lane (question → question embedding → top-k retrieval from the index → prompt assembly → generation) runs per question. Drawn so that two facts are visible at a glance: both lanes map into the same vector space through the same embedding function, and indexing is offline while querying is online.

The assembled prompt takes the following form.

> Answer the question using only the evidence below. If the evidence does not contain the answer, say you do not know.
>
> [Evidence 1] Reflexion summarizes the cause of a failure in language and injects it into the next attempt's input …
> [Evidence 2] …
>
> Question: How does Reflexion obtain improvement without weight updates?

The instruction "say you do not know if it is not in the evidence" does its work when retrieval misses and irrelevant chunks arrive. Without it, the model does not stop predicting for lack of a stored fact and fills the gap from parametric knowledge and hallucination (→ 8.1). The instruction enforces grounding — keeping the premises of reasoning on externally verified fact (→ 4.3) — and the evidence markers double as source citations.

## 8.4 Chunking and top-k

The choices that decide the pipeline's accuracy are not code but the granularity of chunking and the value of k.

The need for chunking lies in the nature of embeddings. An embedding compresses the meaning of one fragment into one vector. Embedding a whole document as one fragment averages several topics into a vector distinctly close to no question; cutting into single sentences sharpens each vector but strips the retrieved fragment of context, leaving it too thin to serve as evidence. The practical starting point is a natural boundary such as the paragraph, with adjacent chunks overlapping slightly to soften context loss at the cut.

k is a trade of the same structure. A small k cuts off needed evidence; a large k admits noise chunks, raises cost, and invites the long-input degradation (→ Ch. 9). Neither choice has a predetermined correct value, so both are set by measurement: vary the setting and score it on the small evaluation set built earlier (→ Ch. 5).

## 8.5 Improving Retrieval — Hybrid Search and Re-ranking

Embedding retrieval has its own blind spot. Where keyword matching failed on differences of wording (→ 8.2), embeddings fail from the opposite side: proper nouns, function and model names, and exact quoted strings (the literal string "ReWOO") blur into their neighbors in meaning space, and the chunk containing exactly that string can fail to reach the top. Classical word-match retrieval — BM25, a score combining a word's frequency within a document with its rarity across documents — is strong in exactly this case. The two are complementary, so practical retrievers run both and merge the results; this is **hybrid search**. The standard merging method is **RRF (reciprocal rank fusion)**. The two retrievers' scores are on different scales and cannot be added directly, so only ranks are used:

$$\text{RRF}(d) = \sum_{r \in \text{retrievers}} \frac{1}{k_0 + \text{rank}_r(d)}$$

A document adds a larger term the higher it ranks (the smaller $\text{rank}_r(d)$ is) in each retriever, and the constant $k_0$ (conventionally 60) flattens the gap between first place and the lower ranks.

When more precision is needed, retrieval splits into two stages. **Re-ranking** is the stage in which the few dozen candidates from stage one are re-scored by a model that reads question and chunk together in one input (a cross-encoder), selecting the final k. A cross-encoder compares question and document mutually and is therefore more precise than the bi-encoder (→ 8.2), but each pair costs a model call, so it cannot be used for exhaustive search. The result is a division of labor: stage one (bi-encoder, BM25) is responsible for not missing (recall); stage two (cross-encoder) is responsible for choosing exactly (precision).

> **[Figure 8.2]** Two-stage retrieval drawn as a funnel, wide at the top and narrow at the bottom. From the full chunk pile at the top, stage one (bi-encoder + BM25, recall-oriented) narrows to a few dozen candidates, and stage two (cross-encoder re-ranking, precision-oriented) narrows to the final k. On the stage-one arrow, question and document are vectorized separately; on the stage-two arrow, question and chunk enter as one input — contrasted so the order of the recall/precision division is visible.

Retriever quality is measured separately, without going through generation. The standard metric is **recall@k** — the fraction of questions for which a correct evidence chunk appears in the top k. If retrieval fails to bring the correct evidence at all, the generation stage cannot repair it (errors propagate downstream), so pipeline improvement starts from measuring recall@k. Query-transformation techniques such as HyDE — generating a hypothetical answer and embedding that for retrieval instead of the question — are directed to optional reading.

## 8.6 Retrieval as a Tool — Agentic RAG

By the distinction of Chapter 1, the pipeline of 8.3 is a workflow: whether to retrieve, with what query, and how many times are all fixed in code. This fixing produces three failures. First, it retrieves on every input: a greeting or an arithmetic question still triggers retrieval, spending cost and attaching noise evidence. Second, it uses the question sentence verbatim as the query: when the question's wording is far from the document's wording, even the embeddings of 8.2 miss, and nothing exists to rewrite the query. Third, it retrieves exactly once: a multi-hop question — one whose next query is determined only by reading the first retrieval's result (the structure of the Apple Remote question → 4.2) — cannot be answered by a single retrieval.

The common cause of the three failures is that the retrieval decisions sit in code that cannot read execution results, and the prescription is that of Chapter 4: delegate the decisions to the model. Concretely, the query stage of 8.3 is detached from the pipeline and registered as a tool in the registry of Chapter 3. The search_papers tool used in 3.4 as the example of a good schema is this tool. Its schema description ("do not use for general knowledge or arithmetic; the input is one sentence describing what to find") supplies the basis for routing — judging whether to retrieve — and for query writing, and the loop of Chapter 4 makes re-retrieval, and with it multi-hop search, possible. The construction in which an agent holding retrieval as a tool decides the timing, query, and count of retrieval is called **agentic RAG**. The question closing 2.6 — which questions deserve more compute — appears here as which questions deserve retrieval, and the prompt and the schema carry that selection.

> **[Figure 8.3]** Fixed pipeline and agentic RAG contrasted side by side. On the left, a straight flow fixed in code (every input → always retrieve once → generate). On the right, a loop with the model at the center: the model judges whether retrieval is needed and calls the search_papers tool (not calling it for greetings or arithmetic), and a returning arrow shows it reading the result and re-calling with a rewritten query. The difference to expose: the authority over whether/what/how many times has moved from code to model.

Putting this judgment into the weights instead of the prompt is this week's presentation paper. **Self-RAG** (Asai et al., 2023) trains the model to judge for itself — with special tokens called reflection tokens — whether retrieval is needed, whether a retrieved passage is relevant to the question, and whether the generated answer is supported by the passage. It is the prompt-versus-weights framing again (→ 3.8); critic training and the generation procedure are detailed in the presentation.

## 8.7 Summary

The deficiencies of parametric knowledge (cutoff, private material, hallucination) are compensated by putting knowledge into the input, and the capacity limit makes retrieval — selecting only the relevant parts — necessary. Relevance is judged by cosine similarity in embedding space, and the procedure standardizes into indexing (chunking → embedding → storage) and query (embedding → top-k → assembly → generation). Quality is set by measuring chunk granularity and k; the embedding blind spot (proper nouns, identifiers) is covered by hybrid search with keyword retrieval, the bi-encoder's precision limit by cross-encoder re-ranking, and the retriever itself is measured apart from generation with recall@k. The failures of the fixed pipeline (always retrieving, rigid queries, single-shot retrieval) are prescribed agentic RAG — registering the query stage as a tool and delegating the retrieval decisions to the model — and the learned form of that judgment is Self-RAG.

With this chapter the agent has a standing ingress for external input: documents. That retrieved chunks are attached verbatim to the prompt means instructions written inside documents also enter as prompt text; this ingress becoming an attack path is treated in Chapter 14 (indirect prompt injection). Multi-hop questions that no single retrieval settles are taken up as planning in Chapter 7.

**Presentation.** RAG (Lewis et al., 2020) — the original combination of parametric and non-parametric knowledge, with jointly trained retriever. Self-RAG (Asai et al., 2023) — internalizing the retrieval judgment via reflection tokens. Both are heard through one question: where does the retrieval decision (whether to retrieve, whether to trust) reside? Optional reading: HyDE (Gao et al., 2022), Adaptive-RAG (Jeong et al., 2024).

**Lab.** Retriever for the final project (planned): build the search index over the course's paper corpus that the final research-assistant agent will use — chunking, embedding, and top-k retrieval as in 8.3–8.4. Details are finalized in the post-midterm lab rework.
