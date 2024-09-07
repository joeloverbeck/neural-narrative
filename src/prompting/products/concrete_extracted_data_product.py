from src.prompting.abstracts.factory_products import ExtractedDataProduct


class ConcreteExtractedDataProduct(ExtractedDataProduct):

    def __init__(self, extracted_data):
        # The extracted data shouldn't be none or empty at this point.
        assert extracted_data

        self._extracted_data = extracted_data

    def get(self):
        return self._extracted_data
