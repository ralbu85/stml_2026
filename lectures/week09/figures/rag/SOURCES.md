# Chapter 8 — Diagram sources

## Current chapter: the approved six-section outline

The current chapter has six course-authored HTML examples and diagrams. Their markup is in `notes.en.md` and responsive styles are in `reading-concepts.html`. No external images or diagram services are required.

| Figure | Purpose |
|---|---|
| `basic-rag-figure` | Show a complete file-format question, retrieved excerpt, and supported answer before introducing implementation details. |
| `chunking-figure` | Divide a fictional course-guide excerpt at a section boundary into two multi-sentence paragraph chunks, preserving text and sources. |
| `preparation-figure` | Connect chunking, encoding, and indexing; show that vectors remain linked to original text and metadata. The records are explanatory, not a specific index algorithm. |
| `retrieval-figure` | Use a query vector and prepared search index to select chunks and return their text and sources. |
| `model-input-figure` | Show the original question, full C1 passage, instructions, and a supported answer together. |
| `next-search-figure` | Use the reference already present in C1 to motivate retrieval of the assignment instructions. |

C1 is the final-report paragraph; C2 is the presentation paragraph. The source is fictional and is not a statement of this course's rules. The first example quotes only C1's file-format sentence, while the model-input example includes its complete text. No embedding scores, generated responses, or agent actions are presented as recorded model outputs.

The prior exact-word lookup example and its JavaScript are not used in this version. The current chapter develops embedding-based RAG first, then introduces keyword and hybrid search when discussing retrieval failures.

Concept sources:

- RAG and parametric/non-parametric knowledge: [Lewis et al.](https://arxiv.org/abs/2005.11401).
- Chunk sizes and overlap: [LangChain text splitting](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter).
- Embedding comparison and reranking: [Sentence Transformers semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) and [retrieve & rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html).
- Keyword retrieval: [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/).
- Retrieval control: [LangChain RAG architectures](https://docs.langchain.com/oss/python/deepagents/retrieval#rag-architectures).
- Self-RAG: [Asai et al.](https://arxiv.org/abs/2310.11511) and the [authors' overview](https://selfrag.github.io/).

These sources were checked during the Chapter 8 work on 2026-09-20.

## Archived artwork

The SVG and PNG files below are retained for provenance but are not displayed by the current chapter. `scripts/build_w9_rag_figures.py` regenerates those earlier SVGs, not the current HTML diagrams. Their original attribution follows.

## Earlier semantic-search illustration

`semantic-search.png` is reproduced unchanged from the **Sentence Transformers documentation**, maintained by the Sentence Transformers project.

- [Explanation and original figure](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)
- [Image at its source revision](https://github.com/huggingface/sentence-transformers/blob/fc963d6e45643fd2b32f931ecb3b6d102897e3d0/docs/img/SemanticSearch.png)
- License: Apache License 2.0; [full license](SENTENCE-TRANSFORMERS-LICENSE.txt).
- SHA-256: `2e0d6b8e97325fd312f61359e9aa12213cddaff31ce7b6df1b7bdc59902a7511`.

The image is a conceptual illustration. Its point coordinates do not report an embedding experiment, and spatial distance in the drawing is not a computed cosine score.

## Self-RAG

`self-rag.svg` is a simplified conceptual redraw based on the **Self-RAG authors' overview** by Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi.

- [Authors' overview and original diagram](https://selfrag.github.io/)
- [Research paper](https://arxiv.org/abs/2310.11511)
- The source website and this adapted diagram use [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- Changes: replaced the detailed U.S.-state examples with conceptual nodes; omitted special-token labels and candidate rankings; retained the retrieval choice, passage relevance, answer support, response utility, and continuation of generation.

The diagram shows the mechanism at an introductory level. It does not reproduce the paper's training or decoding algorithm.

## Course-authored diagrams

`knowledge-sources.svg`, `pipeline.svg`, `chunk-boundaries.svg`, `retrieval-stages.svg`, `claim-support.svg`, and `control.svg` are course-authored teaching diagrams. The policy text and candidate claims are fictional teaching examples, not measured model outputs or course regulations.

The knowledge-source distinction follows [Lewis et al., RAG](https://arxiv.org/abs/2005.11401). The retrieval and reranking diagram follows the component roles explained in [Sentence Transformers, Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html). The retrieval-control comparison follows [LangChain's RAG architecture explanation](https://docs.langchain.com/oss/python/deepagents/retrieval#rag-architectures).

The editable SVGs are generated by `scripts/build_w9_rag_figures.py`. Sources were checked on 2026-09-20.
