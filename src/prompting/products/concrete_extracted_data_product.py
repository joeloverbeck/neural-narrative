from src.prompting.abstracts.factory_products import ExtractedDataProduct


class ConcreteExtractedDataProduct(ExtractedDataProduct):

    def __init__(self, extracted_data):
        assert extracted_data
        self._extracted_data = extracted_data

    def get(self):
        return self._extracted_data
