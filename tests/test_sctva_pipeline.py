from sctva.pipelines.main import create_study_pipeline


def test_create_study_pipeline():
    sctva_pipeline = create_study_pipeline()
    sctva_pipeline.sctva_pipeline.write_graph(graph2use="colored")
    pass