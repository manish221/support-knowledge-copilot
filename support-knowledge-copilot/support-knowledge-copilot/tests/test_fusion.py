from app.retrieval.fusion import reciprocal_rank_fusion


def test_rrf_prefers_repeated_chunk():
    a = [{"chunk_id": "x", "rank": 1, "score": 1, "retriever": "dense"}]
    b = [{"chunk_id": "x", "rank": 2, "score": 1, "retriever": "bm25"}, {"chunk_id": "y", "rank": 1, "score": 1, "retriever": "bm25"}]
    result = reciprocal_rank_fusion([a, b])
    assert result[0]["chunk_id"] == "x"
