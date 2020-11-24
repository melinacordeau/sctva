from sctva.pipelines.full import create_study_pipeline


def test_create_study_pipeline():
    sctva_pipeline = create_study_pipeline()
    sctva_pipeline.write_graph(graph2use="colored", format="png")
    pass


if __name__ == "__main__":
    test_create_study_pipeline()
