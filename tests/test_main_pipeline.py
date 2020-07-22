from sctva.pipelines.main import create_main_pipeline


def test_create_main_pipeline():
    pipeline = create_main_pipeline()
    pipeline.write_graph(dotfilename="main_graph", graph2use="colored", format="png",)
    pass


if __name__ == "__main__":
    test_create_main_pipeline()
