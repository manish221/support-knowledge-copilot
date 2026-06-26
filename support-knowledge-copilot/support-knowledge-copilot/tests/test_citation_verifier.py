from app.verification.citation_verifier import verify_claim_against_chunk


def test_supported_claim():
    claim = "ERR-429 means the client exceeded the API rate limit."
    chunk = "ERR-429 means the client exceeded the API rate limit. Wait at least 60 seconds before retrying."
    result = verify_claim_against_chunk(claim, chunk)
    assert result["verdict"] == "supported"
