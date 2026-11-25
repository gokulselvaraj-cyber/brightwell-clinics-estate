from brightwell_visit_summary.prompt_builder import PromptBuilder


def test_system_prompt_first():
    msgs = PromptBuilder().build("Knee pain, physio booked.", "BWP-01400")
    assert msgs[0]["role"] == "system"
    assert "fit for discharge" in msgs[0]["content"]


def test_procedure_label_default():
    msgs = PromptBuilder().build("notes", None)
    assert "not recorded" in msgs[1]["content"]
