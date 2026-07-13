import importlib


def test_graph_modules_import():
    modules = [
        "app.graphs.course_graph",
        "app.graphs.main_graph",
        "app.graphs.metadata_graph",
        "app.graphs.template_graph",
    ]

    for module_name in modules:
        module = importlib.import_module(module_name)
        assert module is not None
