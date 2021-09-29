class Page:
    def __init__(self, address: str, content: str, datalayer: dict):
        self._address = address
        self._content = content
        self._datalayer = datalayer

    @property
    def address(self):
        return
