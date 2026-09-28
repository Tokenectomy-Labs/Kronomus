"""
Unit tests for IssueDeNoiser and ZeroLLMMutationBracket.
"""

from scripts.issue_denoiser import IssueDeNoiser
from scripts.mutation_bracket import ZeroLLMMutationBracket


def test_issue_denoiser_removes_human_chaff():
    raw_issue = (
        "Hi team,\n"
        "Thanks for the awesome project!\n"
        "> on May 12 @alice wrote:\n"
        "> maybe this is related to #123\n\n"
        "When calling django.db.models.QuerySet.filter with an empty tuple, it crashes:\n\n"
        "Traceback (most recent call last):\n"
        "  File \"django/db/models/sql/query.py\", line 140, in build_filter\n"
        "    return self.where.add(clause)\n"
        "TypeError: 'NoneType' object is not subscriptable\n\n"
        "Expected behavior: It should return empty QuerySet.\n\n"
        "As a temporary workaround, I monkey patched settings.py.\n"
        "Cheers,\nBob"
    )

    res = IssueDeNoiser.denoise_issue(raw_issue, repo="django/django")
    cleaned = res["cleaned_text"]
    triad = res["triad"]

    # Verify greetings and sign-offs are gone
    assert "Hi team," not in cleaned
    assert "Thanks for the awesome project!" not in cleaned
    assert "Cheers," not in cleaned
    assert "As a temporary workaround" not in cleaned

    # Verify core signals were extracted
    assert "TypeError" in triad["exceptions"]
    assert "django.db.models.QuerySet.filter" in triad["symbols"]
    assert any("empty QuerySet" in exp for exp in triad["expected_behavior"])
    assert res["token_reduction_pct"] > 20.0
    print(f"✅ IssueDeNoiser test passed (Reduced token bloat by {res['token_reduction_pct']}%)")


def test_issue_denoiser_tags_user_reproduction_code():
    raw_issue = (
        "The following script crashes:\n"
        "```python\n"
        "class DummyModel(models.Model):\n"
        "    name = models.CharField(max_length=50)\n"
        "```\n"
        "Please fix!"
    )
    res = IssueDeNoiser.denoise_issue(raw_issue, repo="django/django")
    cleaned = res["cleaned_text"]
    assert "[USER_REPRODUCTION_SNIPPET - REFERENCE ONLY, NEVER PATCH THIS]" in cleaned
    print("✅ Reproduction snippet tagging test passed!")


def test_mutation_bracket_generates_boundary_and_type_flips():
    code_boundary = "    if amount > 100:\n        return True\n"
    mutations = ZeroLLMMutationBracket.generate_candidate_mutations(code_boundary)
    names = [op for op, _ in mutations]
    assert "boundary_flip" in names
    mutated_code = [c for op, c in mutations if op == "boundary_flip"][0]
    assert "if amount >= 100:" in mutated_code

    code_type = "    return list(results)\n"
    mutations_type = ZeroLLMMutationBracket.generate_candidate_mutations(code_type)
    names_type = [op for op, _ in mutations_type]
    assert "list_to_tuple" in names_type
    mutated_type = [c for op, c in mutations_type if op == "list_to_tuple"][0]
    assert "return tuple(results)" in mutated_type

    print(f"✅ Mutation bracket test passed! Generated {len(mutations)} deterministic variations.")


if __name__ == "__main__":
    test_issue_denoiser_removes_human_chaff()
    test_issue_denoiser_tags_user_reproduction_code()
    test_mutation_bracket_generates_boundary_and_type_flips()
    print("\n🎉 ALL SUBCORTEX ENHANCEMENT TESTS PASSED 100%!")
