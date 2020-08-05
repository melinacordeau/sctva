from sctva.pipelines.main import create_main_pipeline


def test_create_main_pipeline():
    test_subject = ['sub-04']
    pipeline = create_main_pipeline(test_subject)
    pipeline.base_dir = '/home/alex/recherche/data/sctva' # to be changed to adapt
    # frioul
    pipeline.write_graph(
        dotfilename="main_graph", graph2use="colored", format="png",
    )
    pipeline.run()

    pass


if __name__ == "__main__":
    test_create_main_pipeline()
