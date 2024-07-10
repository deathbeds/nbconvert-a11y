async def test_axe_tester():
    from nbconvert_a11y.axe import async_axe

    results = await async_axe.validate_axe("")
    assert {x["id"] for x in results["violations"]} == {
        "document-title",
        "html-has-lang",
        "landmark-one-main",
        "page-has-heading-one",
    }
