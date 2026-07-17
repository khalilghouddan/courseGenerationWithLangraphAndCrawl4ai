import asyncio

from app.graphs.main_graph import main_graph


def test_main_graph_generates_a_course():
    result = asyncio.run(
        main_graph.ainvoke({"prompt": "Create a beginner course about Python"})
    )

    course = result.get("course")
    assert course is not None
    assert course.title
    assert course.description
