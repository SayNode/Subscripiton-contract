


def test_edit_logo(self):
    """Test can upload logo."""
    data = {"name": "this is a name", "age": 12}
    data = {key: str(value) for key, value in data.items()}
    data["file"] = (io.BytesIO(b"abcdef"), "test.jpg")
    self.assertIn(b"Your item has been saved.", response.data)
    advert = Item.query.get(1)
    self.assertIsNotNone(item.logo)
